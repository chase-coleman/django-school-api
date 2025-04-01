from django.shortcuts import render
from student_app.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT
from decimal import Decimal
from django.shortcuts import get_object_or_404

# Create your views here.


class All_grades(APIView):
    def get(self, request):
        all_grades = GradeSerializer(Grade.objects.all(), many=True).data 
        return Response(all_grades)
    
    def put(self, request, id):
        # gets the searched subject, or returns a 404 status
        grabbed_grade = get_object_or_404(Grade, id=id)
        # serializes grade obj w/ new data input
        grade_ser = GradeSerializer(grabbed_grade, data=request.data, partial=True)
        # checks if the serialized grade data is valid
        if grade_ser.is_valid():
            grade_ser.save() # saves it 
            return Response({'MESSAGE': "Grade was successfully updated!"}, status=HTTP_200_OK) # returns a 200 status
        # if not valid, returns 400 status
        return Response(grade_ser.errors, status=HTTP_400_BAD_REQUEST) 

    def post(self, request):
        new_grade = GradeSerializer(data=request.data)
         # checks if new_student has valid data entry
        if new_grade.is_valid(): 
            saved_grade = new_grade.save() # saves it
            return Response(GradeSerializer(saved_grade).data, status=HTTP_201_CREATED) # returns 201 status
        return Response(new_grade.errors, status=HTTP_400_BAD_REQUEST) # if not valid data entry, returns 400 status

    def delete(self, request, id):
        grade_to_delete = get_object_or_404(Grade, id=id) # gets the searched subject, or returns a 404 status
        grade_to_delete.delete() # deletes it if found 
        return Response({"MESSAGE": "Grade was successfully deleted"}, status=HTTP_204_NO_CONTENT) # returns a 204 status



class A_student(APIView):
    def get(self, request, id):
        all_subjects = get_subjects()
        all_students = get_students_subjects(all_subjects)
        try:  # getting the correct student from the database
            student_instance = Student.objects.get(id=id)
            student_ser = StudentIDSerializer(student_instance).data
            # list comprehension searching for a student w/ matching name
            student = next(
                (stud for stud in all_students if stud["name"] == student_ser["name"])
            )
            return Response(student)
        except Student.DoesNotExist:
            return Response("Student does not exist", status=HTTP_404_NOT_FOUND)

# class-based views
class All_students(APIView):

    # need to make a method to be able to add subjects into the student list of subjects

    def get(self, request):
        # calls helper function to get all the subjects
        all_subjects = get_subjects() 
        # calls helper function to get all students w/ their subjects
        students = get_students_subjects(all_subjects) 
        return Response(students)
    
    def put(self, request, id):
         # gets the searched student, or returns a 404 status
        grabbed_student = get_object_or_404(Student, id=id)
        # serializes student obj
        student_ser = StudentAllSerializer(grabbed_student, data=request.data, partial=True) 
        # checks if serialized student is valid w/ new data 
        if student_ser.is_valid(): 
            # if yes -> saves it 
            student_ser.save() 
            # returns 200 status
            return Response({"MESSAGE": "Student info was successfully updated!"}, status=HTTP_200_OK) 
        # if not valid, returns 400 status
        return Response(student_ser.errors, status=HTTP_400_BAD_REQUEST) 

    def post(self, request):
        # serializes new_student info
        new_student = StudentAllSerializer(data=request.data) 
        # checks if new_student has valid data entry
        if new_student.is_valid(): 
            saved_student = new_student.save() # saves it
            # returns 201 status
            return Response(StudentAllSerializer(saved_student).data, status=HTTP_201_CREATED) 
         # if not valid data entry, returns 400 status
        return Response(new_student.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        student_to_delete = get_object_or_404(Student, id=id) # gets the searched student, or returns a 404 status
        student_to_delete.delete() # deletes student record 
        return Response({"MESSAGE": "Student was removed successfully"}, status=HTTP_204_NO_CONTENT) # returns 204 status


class A_subject(APIView):
    def get(self, request, subject):
        all_subjects = get_subjects()
        try:  # list comprehension searching for a subject w/ matching name
            subject_return = next(
                (sub for sub in all_subjects if sub["subject_name"] == subject.title())
            )
            print(subject_return)
            return Response(subject_return)
        except StopIteration:
            return Response("Subject not found", status=HTTP_404_NOT_FOUND)



class All_subjects(APIView):
    def get(self, request):
        all_subjects = get_subjects() # calls helper function to get all the subjects
        return Response(all_subjects)

    def put(self, request, subject):
        # gets the searched subject, or returns a 404 status
        grabbed_subject = get_object_or_404(Subject, subject_name=subject.title())  
        # serializes subject obj w/ new data input
        subject_ser = SubjectSerializer(grabbed_subject, data=request.data, partial=True)  
        # checks if new_student has valid data entry
        if subject_ser.is_valid(): 
            subject_ser.save() # if yes -> saves it 
            return Response({"MESSAGE": "Subject was successfully updated."}, status=HTTP_200_OK) # returns 200 status
        return Response(subject_ser.errors, status=HTTP_400_BAD_REQUEST) # if not valid data input, returns 400 status
    
    def post(self, request):
        # serializes new_subject info 
        new_subject = SubjectSerializer(data=request.data) 
        # checks if new_subject has valid data entry
        if new_subject.is_valid(): 
            # if yes -> saves new subject into db
            saved_subject = new_subject.save() 
            return Response(SubjectSerializer(saved_subject).data, status=HTTP_201_CREATED) # returns 201 status
        return Response(new_subject.errors, status=HTTP_400_BAD_REQUEST) # if not valid data input, returns 400 status
    
    def delete(self, request, subject): 
        subject_to_delete = get_object_or_404(Subject, subject_name=subject.title()) # gets the searched subject, or returns a 404 status
        subject_to_delete.delete() # deletes student record 
        return Response({"MESSAGE": "Subject was removed successfully"}, status=HTTP_204_NO_CONTENT) # returns 204 status

"""
HELPER FUNCTIONS 
"""

def get_students_subjects(all_subjects):
    students = StudentAllSerializer(Student.objects.all(), many=True).data
    # loops through each student
    for student in students:
        # empty variable that we will store each students subjects in
        student_subjects = []
        # loop through each subject in each student's initial subjects attribute (initially they are foreign keys)
        for sub in student["subjects"]:
            # grab the correct subject using the foreign keys
            subject_obj = SubjectSerializer(Subject.objects.get(id=sub))
            # grab the subjects name only
            subject_name = subject_obj.data["subject_name"]
            # use list comprehension to find the correct subject dictionary in the all_subjects list
            subject_to_add = next(
                (
                    subject
                    for subject in all_subjects
                    if subject["subject_name"] == subject_name
                ),
                None,
            )
            # add that subject dictionary into the student_subjects list
            student_subjects.append(subject_to_add)
        # reassign the student['subject'] list as the list of subject dictionaries
        student["subjects"] = student_subjects
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
            # print(subject['students'])
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
