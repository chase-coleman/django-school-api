from django.urls import path 
from .views import *

urlpatterns = [
  # api/v1/all_students
  path('students/', All_students.as_view(), name="all_students"),
  path('subjects/', All_subjects.as_view(), name="all_subjects"),
  path('students/<int:id>/', A_student.as_view(), name="a_student"),
  path('subjects/<str:subject>/', A_subject.as_view(), name="a_subject")
]