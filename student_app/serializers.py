from rest_framework.serializers import ModelSerializer 
from .models import Student, Subject, Grade 

class StudentSerializer(ModelSerializer):
  class Meta:
    model = Student
    fields = ['name', 'student_email','locker_number']

class StudentAllSerializer(ModelSerializer):
  class Meta:
    model = Student
    fields = ['name', 'student_email', 'personal_email', 
            'locker_number', 'locker_combination', 'good_student']

class SubjectSerializer(ModelSerializer):
  class Meta:
    model = Subject 
    fields = ['subject_name', 'professor', 'students']
  
class SubjectAllSerializer(ModelSerializer):
  class Meta:
    model = Subject
    fields = ['subject_name', 'professor', 'students']
  
class GradeSerializer(ModelSerializer):
  class Meta:
    model = Grade 
    fields = ['grade', 'a_subject', 'student']
