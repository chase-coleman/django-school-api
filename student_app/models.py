from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
import re
# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100, validators=[RegexValidator(r'^[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+$', message= 'Name must be in the format "First Middle Initial. Last"')])
    student_email = models.EmailField(unique=True, validators=[RegexValidator(r'^[a-zA-Z0-9._%+-]+@school\.com$', message= 'Invalid school email format. Please use an email ending with "@school.com".')])
    personal_email = models.EmailField(blank=True, null= True, unique=True)
    locker_number = models.IntegerField(default=110, unique= True, validators=[MinValueValidator(1), MaxValueValidator(200)])
    locker_combination = models.CharField(max_length=20, default = "12-12-12", blank=True, validators=[RegexValidator(r'^\d{2}-\d{2}-\d{2}$', message= 'Combination must be in the format "12-12-12"')] )
    good_student= models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.student_email} - {self.locker_number}"
    
    def locker_reassignment(self, new_locker_number):
        self.locker_number = new_locker_number
        self.save()
        return f"Student: {self.student.name}'s locker has been changed to {self.locker_number}"
    
    def student_status(self, is_good_student):
        self.good_student = is_good_student
        self.save()
