from django.urls import path 
from .views import *

urlpatterns = [
  # api/v1/all_students
  path('students/', All_students.as_view(), name="all_students"),
  path('subjects/', All_subjects.as_view(), name="all_subjects")
]