from django.shortcuts import render
from django.http import JsonResponse
from student_app.serializers import *
from rest_framework.views import Response, APIView
# Create your views here.

# class-based views
class All_students(APIView):
  # create methods for all http verbs (get, post, put, delete)
  def get(self, request):
    students = StudentAllSerializer(Student.objects.all(), many=True)
    return Response(students.data)

class All_subjects(APIView):
  def get(self, request):
    subjects = SubjectAllSerializer(Subject.objects.all(), many=True)
    return Response(subjects.data)

# function-based views
# def all_students(request):
#   all = Student.objects.all()
# # print(all)
#   all_ser = StudentSerializer(all, many=True)
# # print(all_ser.data)
#   return JsonResponse({"json": all_ser.data})