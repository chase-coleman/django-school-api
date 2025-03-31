from django.shortcuts import render
from django.http import JsonResponse
from student_app.serializers import *
from rest_framework.views import Response, APIView
from rest_framework.status import HTTP_404_NOT_FOUND
from decimal import Decimal
from django.shortcuts import get_object_or_404

# Create your views here.

class A_student(APIView):
   def get(self, request, id):
        all_subjects = get_subjects()
        all_students = get_students_subjects(all_subjects)
        try:
            student_answer = Student.objects.get(id=id)
            student_ser = StudentIDSerializer(student_answer).data

            student_return = next((student for student in all_students if student['name'] == student_ser['name']))
                # print(student_return)
            return Response(student_return)
        except Student.DoesNotExist:
            return Response('Student does not exist', status=HTTP_404_NOT_FOUND)
    #   print(student_ser)

class A_subject(APIView):
   def get(self, request, subject):
    #   print(name.title())
        all_subjects = get_subjects()
        try:
            subject_return = next((sub for sub in all_subjects if sub['subject_name'] == subject.title()))
            # print(subject_return)
            return Response(subject_return)
        except StopIteration:
           return Response('Subject not found', status=HTTP_404_NOT_FOUND)
        


# class-based views
class All_students(APIView):
    # create methods for all http verbs (get, post, put, delete)
  def get(self, request):
    all_subjects = get_subjects()
    students = get_students_subjects(all_subjects)
    return Response(students)


class All_subjects(APIView):
    def get(self, request):
      # grabs the list of all subjects in proper formatting 
      all_subjects = get_subjects()
      # print(answer)
      return Response(all_subjects)

def get_students_subjects(all_subjects):
    students = StudentAllSerializer(Student.objects.all(), many=True).data
    # loops through each student
    for student in students:
        # empty variable that we will store each students subjects in
        student_subjects = [] 
        # loop through each subject in each student's initial subjects attribute (initially they are foreign keys)
        for sub in student['subjects']:
            # grab the correct subject using the foreign keys 
            subject_obj = SubjectSerializer(Subject.objects.get(id=sub))
            # grab the subjects name only 
            subject_name = subject_obj.data['subject_name']
            # use list comprehension to find the correct subject dictionary in the all_subjects list
            subject_to_add = next((subject for subject in all_subjects if subject['subject_name'] == subject_name), None)
            # add that subject dictionary into the student_subjects list
            student_subjects.append(subject_to_add)
        # reassign the student['subject'] list as the list of subject dictionaries         
        student['subjects'] = student_subjects
    return students

def get_subjects():
  # grab all subjects 
  subjects = SubjectSerializer(Subject.objects.all(), many=True)
  answer = []
  for subject in subjects.data:
      # grabs the subject's id from the database table
      subject_id = Subject.objects.get(subject_name=subject["subject_name"]).id
      # grabs the correct grade object that matches with the subject
      subject_grades = Grade.objects.filter(a_subject=subject_id)
      avg_grade = 0
      if subject_grades.exists():
          # using list comprehension to loop through each students grade in that subject and sum it up
          total_grade = sum(Decimal(grade.grade) for grade in subject_grades)
          # rounds by dividing the total grade by amount of students in the class
          avg_grade = round(total_grade / Decimal(subject_grades.count()), 2)
          # reassigns the subject.students to a count of how many students are in the class
          subject["students"] = len(subject["students"])
          # creates a new key:value pair in each subject 
          subject["grade_average"] = float(avg_grade)
          answer.append(subject)
  return answer


# function-based views
# def all_students(request):
#   all = Student.objects.all()
# # print(all)
#   all_ser = StudentSerializer(all, many=True)
# # print(all_ser.data)
#   return JsonResponse({"json": all_ser.data})
