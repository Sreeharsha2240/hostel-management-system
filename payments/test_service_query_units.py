"""Inspect lazy billing expressions without executing a database query."""

from decimal import Decimal

from django.db.models import Case, DecimalField, Subquery, Sum, Value
from django.db.models.expressions import Col
from django.db.models.functions import Coalesce
from django.test import SimpleTestCase

from allocations.models import Allocation
from students.models import Student

from .models import Payment
from .services import payment_status_queryset


class PaymentStatusQueryUnitTests(SimpleTestCase):
    def test_default_scope_is_all_students_with_independent_billing_annotations(self):
        result = payment_status_queryset()

        self.assertIs(result.model, Student)
        self.assertEqual(result.query.where.children, [])
        self.assertEqual(
            set(result.query.annotations),
            {
                "fee_amount",
                "amount_paid",
                "billing_hostel_id",
                "billing_hostel",
                "billing_room",
                "billing_bed",
            },
        )
        # Related tables belong in scalar subqueries, avoiding outer join totals.
        self.assertEqual(
            {table.table_name for table in result.query.alias_map.values()},
            {Student._meta.db_table},
        )
        self.assertIsNone(result._result_cache)

    def test_supplied_scope_and_ordering_are_preserved_without_mutating_caller(self):
        students = Student.objects.filter(
            status=Student.Status.ACTIVE, student_id__startswith="BATCH"
        ).order_by("-name", "pk")
        original_where = students.query.where.clone()

        result = payment_status_queryset(students)

        self.assertIsNot(result, students)
        self.assertEqual(result.query.where, original_where)
        self.assertEqual(result.query.order_by, ("-name", "pk"))
        self.assertEqual(students.query.annotations, {})
        self.assertEqual(students.query.where, original_where)
        self.assertIsNone(students._result_cache)
        self.assertIsNone(result._result_cache)

    def test_explicit_empty_scope_is_not_replaced_with_all_students(self):
        students = Student.objects.none()

        result = payment_status_queryset(students)

        self.assertTrue(result.query.is_empty())
        self.assertIn("amount_paid", result.query.annotations)
        self.assertEqual(students.query.annotations, {})

    def test_money_annotations_use_decimal_zero_and_wide_decimal_output(self):
        annotations = payment_status_queryset().query.annotations

        for name in ("fee_amount", "amount_paid"):
            with self.subTest(annotation=name):
                expression = annotations[name]
                self.assertIsInstance(expression, Coalesce)
                subquery, fallback = expression.get_source_expressions()
                self.assertIsInstance(subquery, Subquery)
                self.assertIsInstance(fallback, Value)
                self.assertIsInstance(fallback.value, Decimal)
                self.assertEqual(fallback.value, Decimal("0.00"))
                self.assertIsInstance(expression.output_field, DecimalField)
                self.assertEqual(expression.output_field.max_digits, 20)
                self.assertEqual(expression.output_field.decimal_places, 2)

    def test_each_billing_field_selects_one_consistently_ranked_allocation(self):
        annotations = payment_status_queryset().query.annotations
        paths = {
            "fee_amount": "bed__room__fee_amount",
            "billing_hostel_id": "bed__room__hostel_id",
            "billing_hostel": "bed__room__hostel__name",
            "billing_room": "bed__room__room_number",
            "billing_bed": "bed__label",
        }

        for name, path in paths.items():
            with self.subTest(annotation=name):
                expression = annotations[name]
                if name == "fee_amount":
                    expression = expression.get_source_expressions()[0]
                self.assertIsInstance(expression, Subquery)
                query = expression.query
                self.assertIs(query.model, Allocation)
                self.assertEqual(query.values_select, (path,))
                self.assertEqual(len(query.select), 1)
                self.assertEqual((query.low_mark, query.high_mark), (0, 1))
                self.assertEqual(query.order_by, ("priority", "-allocated_on", "-pk"))
                self.assertEqual(query.where.connector, "AND")
                self.assertFalse(query.where.negated)
                correlation, excluded = query.where.children
                self.assertEqual(correlation.lookup_name, "exact")
                self.assertIs(
                    correlation.lhs.target, Allocation._meta.get_field("student")
                )
                self.assertIsInstance(correlation.rhs, Col)
                self.assertIs(correlation.rhs.target, Student._meta.pk)
                self.assertEqual(correlation.rhs.alias, Student._meta.db_table)
                self.assertTrue(excluded.negated)
                (cancelled,) = excluded.children
                self.assertEqual(cancelled.lookup_name, "exact")
                self.assertIs(
                    cancelled.lhs.target, Allocation._meta.get_field("status")
                )
                self.assertEqual(cancelled.rhs, Allocation.AllocationStatus.CANCELLED)

                priority = query.annotations["priority"]
                self.assertIsInstance(priority, Case)
                (active_case,) = priority.cases
                (active,) = active_case.condition.children
                self.assertEqual(active.lookup_name, "exact")
                self.assertIs(active.lhs.target, Allocation._meta.get_field("status"))
                self.assertEqual(active.rhs, Allocation.AllocationStatus.ACTIVE)
                self.assertEqual(active_case.result.value, 0)
                self.assertEqual(priority.default.value, 1)

    def test_payment_total_is_a_correlated_sum_without_payment_default_ordering(self):
        amount_paid = payment_status_queryset().query.annotations["amount_paid"]
        query = amount_paid.get_source_expressions()[0].query

        self.assertIs(query.model, Payment)
        self.assertEqual(query.order_by, ())
        self.assertFalse(query.default_ordering)
        self.assertEqual((query.low_mark, query.high_mark), (0, None))
        self.assertEqual(set(query.annotation_select), {"total"})
        total = query.annotation_select["total"]
        self.assertIsInstance(total, Sum)
        self.assertFalse(total.distinct)
        self.assertIsNone(total.filter)
        self.assertIs(
            total.get_source_expressions()[0].target, Payment._meta.get_field("amount")
        )
        (group,) = query.group_by
        self.assertIs(group.target, Payment._meta.get_field("student"))
        (correlation,) = query.where.children
        self.assertEqual(correlation.lookup_name, "exact")
        self.assertIs(correlation.lhs.target, Payment._meta.get_field("student"))
        self.assertIsInstance(correlation.rhs, Col)
        self.assertIs(correlation.rhs.target, Student._meta.pk)
        self.assertEqual(correlation.rhs.alias, Student._meta.db_table)
