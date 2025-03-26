from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.postgres.fields import ArrayField
import re

class Student(models.Model):
    name = models.CharField(max_length=100, validators=[RegexValidator(r'^[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+$', message= 'Name must be in the format "First Middle Initial. Last"')])
    student_email = models.EmailField(unique=True, validators=[RegexValidator(r'^[a-zA-Z0-9._%+-]+@school\.com$', message= 'Invalid school email format. Please use an email ending with "@school.com".')])
    personal_email = models.EmailField(blank=True, null= True, unique=True)
    locker_number = models.IntegerField(default=110, unique= True, validators=[MinValueValidator(1), MaxValueValidator(200)])
    locker_combination = models.CharField(max_length=20, default = "12-12-12", blank=True, validators=[RegexValidator(r'^\d{2}-\d{2}-\d{2}$', message= 'Combination must be in the format "12-12-12"')] )
    good_student= models.BooleanField(default=True)
    subjects = ArrayField(
        models.IntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(8)
        ]),
        blank=True,
        default=list
        )

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

    def add_subject(self, subject_id):
        if len(self.subjects) == 8:
            raise Exception("This student's class schedule is full!")
        else:
            self.subjects.append(subject_id)
            self.full_clean()
            self.save()

    def remove_subject(self, subject_id):
        if not len(self.subjects): 
            raise Exception("This students class schedule is empty!")
        else:
            self.subjects.remove(subject_id)
            self.full_clean()
            self.save()
