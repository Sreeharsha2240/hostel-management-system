"""Remaining allocation query and HTML endpoint contracts with data access mocked."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.db.models import F, OuterRef, Q, Subquery
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from accounts.models import User
from hostels.models import Bed, Room
from students.models import Student

from .models import Allocation
from .views import allocation_history, allocation_list, available_beds


class RemainingAllocationViewUnitTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.actor = SimpleNamespace(is_authenticated=True, role=User.Role.WARDEN)

    def request(self, method="get", data=None):
        request = getattr(self.factory, method)("/allocations/", data or {})
        request.user = self.actor
        return request

    def test_available_beds_excludes_active_allocations_and_inactive_hostels(self):
        with patch("allocations.views.Bed.objects.select_related") as related:
            actual = available_beds()
        related.assert_called_once_with("room__hostel")
        related.return_value.filter.assert_called_once_with(
            status=Bed.BedStatus.AVAILABLE, room__hostel__is_active=True
        )
        filtered = related.return_value.filter.return_value
        filtered.exclude.assert_called_once_with(
            allocations__status=Allocation.AllocationStatus.ACTIVE
        )
        eligible = filtered.exclude.return_value
        eligible.alias.assert_called_once()
        room_count = eligible.alias.call_args.kwargs["room_active_count"]
        self.assertIsInstance(room_count, Coalesce)
        subquery, empty_count = room_count.get_source_expressions()
        self.assertIsInstance(subquery, Subquery)
        self.assertEqual(empty_count.value, 0)
        self.assertEqual(subquery.query.high_mark, 1)
        self.assertEqual(subquery.query.order_by, ())
        eligible.alias.return_value.filter.assert_called_once_with(
            room_active_count__lt=F("room__capacity")
        )
        self.assertIs(actual, eligible.alias.return_value.filter.return_value)

    def test_transfer_capacity_query_omits_only_the_departing_allocation(self):
        active = Allocation.objects.filter(
            bed__room_id=OuterRef("room_id"),
            status=Allocation.AllocationStatus.ACTIVE,
        )
        with (
            patch(
                "allocations.views.Allocation.objects.filter", return_value=active
            ) as allocations,
            patch.object(active, "exclude", wraps=active.exclude) as exclude,
        ):
            beds = available_beds(exclude_allocation_id=8)

        allocations.assert_called_once_with(
            bed__room_id=OuterRef("room_id"),
            status=Allocation.AllocationStatus.ACTIVE,
        )
        exclude.assert_called_once_with(pk=8)
        self.assertIsNone(beds._result_cache)
        capacity_limit = beds.query.where.children[-1]
        self.assertEqual(capacity_limit.lookup_name, "lt")
        self.assertIs(capacity_limit.rhs.target.model, Room)
        self.assertEqual(capacity_limit.rhs.target.name, "capacity")

    def test_post_to_list_passes_same_request_to_creation_without_reading_history(self):
        request = self.request("post", {"student": "3", "bed": "4"})
        response = HttpResponse("invalid allocation", status=422)
        with (
            patch(
                "allocations.views.allocation_create", return_value=response
            ) as create,
            patch("allocations.views.Allocation.objects.select_related") as query,
        ):
            self.assertIs(allocation_list(request), response)
        create.assert_called_once_with(request)
        query.assert_not_called()

    def test_html_list_has_real_empty_page_and_trimmed_search_context(self):
        request = self.request(data={"q": "  Alice  ", "page": "999"})
        with (
            patch("allocations.views.Allocation.objects.select_related") as query,
            patch(
                "allocations.views.render", return_value=HttpResponse("allocations")
            ) as render,
        ):
            query.return_value.filter.return_value = []
            self.assertEqual(allocation_list(request).content, b"allocations")
        query.assert_called_once_with("student", "bed__room__hostel")
        query.return_value.filter.assert_called_once_with(
            Q(student__student_id__icontains="Alice")
            | Q(student__name__icontains="Alice")
            | Q(bed__label__icontains="Alice")
            | Q(bed__room__hostel__name__icontains="Alice")
        )
        context = render.call_args.args[2]
        self.assertEqual(render.call_args.args[1], "allocations/allocation_list.html")
        self.assertEqual(context["query"], "Alice")
        self.assertIs(context["allocations"], context["page_obj"])
        self.assertEqual(context["page_obj"].number, 1)
        self.assertEqual(list(context["page_obj"]), [])

    def test_html_history_retains_selected_student_and_related_records(self):
        request = self.request()
        student = Mock(student_id="STUDENT000003")
        records = ["selected student's history"]
        student.allocations.select_related.return_value = records
        with (
            patch(
                "allocations.views.get_object_or_404", return_value=student
            ) as lookup,
            patch(
                "allocations.views.render", return_value=HttpResponse("history")
            ) as render,
        ):
            self.assertEqual(allocation_history(request, 3).content, b"history")
        lookup.assert_called_once_with(Student, pk=3)
        student.allocations.select_related.assert_called_once_with(
            "student", "bed__room__hostel"
        )
        render.assert_called_once_with(
            request,
            "allocations/allocation_list.html",
            {"allocations": records, "student": student},
        )
