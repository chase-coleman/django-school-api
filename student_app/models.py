from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from decimal import Decimal
import re
from .validators import validate_professor, validate_subject, validate_grade

# create subject class here
class Subject(models.Model):
    subject_name = models.CharField(
        unique=True, default="Unknown", null=False,
        validators=[validate_subject])
    professor = models.CharField(
        unique=False, default="Mr. Cahan", null=False,
        validators=[validate_professor])
    # the related_name="students" in the Student class will create an attribute of Subject that contains all the students in that subject
    
    def add_a_student(self, student_id):
        if self.students.count() == 31:
            raise Exception("This subject is full!")
        else:
            stud_inst = Student.objects.get(id=student_id)
            self.students.add(stud_inst)
    
    def drop_a_student(self, student_id):
        if not self.students.exists():
            raise Exception("This subject is empty!")
        else:
            self.students.remove(student_id)


class Student(models.Model):
    name = models.CharField(max_length=100, validators=[RegexValidator(r'^[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+$', message= 'Name must be in the format "First Middle Initial. Last"')])
    student_email = models.EmailField(unique=True, validators=[RegexValidator(r'^[a-zA-Z0-9._%+-]+@school\.com$', message= 'Invalid school email format. Please use an email ending with "@school.com".')])
    personal_email = models.EmailField(blank=True, null= True, unique=True)
    locker_number = models.IntegerField(default=110, unique= True, validators=[MinValueValidator(1), MaxValueValidator(200)])
    locker_combination = models.CharField(max_length=20, default = "12-12-12", blank=True, validators=[RegexValidator(r'^\d{2}-\d{2}-\d{2}$', message= 'Combination must be in the format "12-12-12"')] )
    good_student= models.BooleanField(default=True)
    subjects = models.ManyToManyField(Subject, related_name="students")

    def __str__(self):
        return f"{self.name} - {self.student_email} - {self.locker_number}"
    
    def locker_reassignment(self, new_locker_number):
        self.locker_number = new_locker_number
        self.full_clean()
        self.save()
        return f"Student: {self.name}'s locker has been changed to {self.locker_number}"
    
    def student_status(self, is_good_student):
        self.good_student = is_good_student
        self.full_clean()
        self.save()
    
    def remove_subject(self, subject_id):
        if not self.subjects.exists():
            raise Exception("This students class schedule is empty!")
        else:
            self.subjects.remove(subject_id)

    def add_subject(self, subject_id):
        if self.subjects.count() == 8:
            raise Exception("This students class schedule is full!")
        else:
            self.subjects.add(subject_id)

# create grade class here 
# Decimal("0.00") is represented as a string ensures exactly 0.00 or 100.00 as the max
class Grade(models.Model):
    grade = models.DecimalField(
        max_digits=5, decimal_places=2, 
        validators=[validate_grade])
    a_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="grades")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
