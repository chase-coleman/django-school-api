from rest_framework.serializers import ModelSerializer 
from .models import Student, Subject, Grade 
from rest_framework import serializers

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
  # students = serializers.PrimaryKeyRelatedField(
  #   queryset=Student.objects.all(),
  #   many=True,
  #   required=False)
  
  # read_only tells django to ignore 'students' in a POST or PUT request
  students = StudentAllSerializer(many=True, read_only=True)

  class Meta:
    model = Subject 
    fields = ['subject_name', 'professor', 'students']
  
  def create(self, validated_data):
    # self.initial_data is the raw input data that was passed to 
    # the serializer BEFORE the input data gets validated
    students_data = self.initial_data.pop("new_students_ids") # students that we want to put in the new subject 
    # creating a new subject after the data is validated by the serializer
    new_subject = Subject.objects.create(**validated_data)
    # loop through the initial_data and call the add_a_student method that adds that student
    # to the subject's students and saves it
    for s in students_data:
      new_subject.add_a_student(s)
    return new_subject

class GradeSerializer(ModelSerializer):
  class Meta:
    model = Grade 
    fields = ['grade', 'a_subject', 'student']
