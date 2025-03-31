from rest_framework.serializers import ModelSerializer 
from .models import Student, Subject, Grade 

class StudentIDSerializer(ModelSerializer):
  class Meta:
    model = Student
    fields = ['id', 'name', 'student_email','locker_number']

class StudentAllSerializer(ModelSerializer):
  class Meta:
    model = Student
    fields = ['name', 'student_email', 'personal_email', 
            'locker_number', 'locker_combination', 'good_student', 'subjects']



class SubjectSerializer(ModelSerializer):
  students = StudentAllSerializer(many=True)

  class Meta:
    model = Subject 
    fields = ['subject_name', 'professor', 'students']


class GradeSerializer(ModelSerializer):
  class Meta:
    model = Grade 
    fields = ['grade', 'a_subject', 'student']
