from django.shortcuts import render
from django.http import JsonResponse
from student_app.serializers import *
from rest_framework.views import Response, APIView
import pprint
from decimal import Decimal

# Create your views here.


# class-based views
class All_students(APIView):
    # create methods for all http verbs (get, post, put, delete)
    def get(self, request):
        students = StudentAllSerializer(Student.objects.all(), many=True)
        all_subjects = get_subjects()
        # print(all_subjects)
        all_students = []
        for student in students.data:
          #  print(student['subjects'])
          student_subjects = []
          for sub in student['subjects']:
            subject_obj = SubjectSerializer(Subject.objects.get(id=sub))
            # print(subject_obj.data['subject_name'])
            subject_name = subject_obj.data['subject_name']
            subject_to_add = next((subject for subject in all_subjects if subject['subject_name'] == subject_name), None)
            student_subjects.append(subject_to_add)
          stu = {
            "name": student['name'],
            "student_email": student['student_email'],
            "personal_email": student['personal_email'],
            "locker_number": student['locker_number'],
            "locker_combination": student['locker_combination'],
            "good_student": student['good_student'],
            "subjects": student_subjects
            }
          all_students.append(stu)
        # print(all_students)
        return Response(all_students)


class All_subjects(APIView):
    def get(self, request):
      all_subjects = get_subjects()
      # print(answer)
      return Response(all_subjects)


def get_subjects():
  subjects = SubjectSerializer(Subject.objects.all(), many=True)
  answer = []
  for subject in subjects.data:
      subject_id = Subject.objects.get(subject_name=subject["subject_name"]).id
      subject_grades = Grade.objects.filter(a_subject=subject_id)
      avg_grade = 0
      if subject_grades.exists():
          total_grade = sum(Decimal(grade.grade) for grade in subject_grades)
          avg_grade = round(total_grade / Decimal(subject_grades.count()), 2)
      answer.append(
          {
              "subject_name": subject["subject_name"],
              "professor": subject["professor"],
              "students": len(subject["students"]),
              "grade_average": float(avg_grade),
          }
      )
  return answer


# function-based views
# def all_students(request):
#   all = Student.objects.all()
# # print(all)
#   all_ser = StudentSerializer(all, many=True)
# # print(all_ser.data)
#   return JsonResponse({"json": all_ser.data})
