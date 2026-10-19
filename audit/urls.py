from django.urls import path

from .views import event_list

urlpatterns = [path('audit/events/', event_list, name='audit-events')]
