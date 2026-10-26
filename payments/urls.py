from django.urls import path

from . import views

urlpatterns = [
    path("payments/", views.payment_list, name="payment-list"),
    path("payments/create/", views.payment_create, name="payment-create"),
    path(
        "payments/<str:receipt_no>/adjust/", views.payment_adjust, name="payment-adjust"
    ),
    path(
        "payments/<str:receipt_no>/receipt/",
        views.payment_receipt,
        name="payment-receipt",
    ),
    path(
        "payments/<str:receipt_no>/receipt.pdf",
        views.payment_receipt_pdf,
        name="payment-receipt-pdf",
    ),
    path(
        "students/<int:pk>/payment-status/",
        views.student_payment_status,
        name="student-payment-status",
    ),
]
