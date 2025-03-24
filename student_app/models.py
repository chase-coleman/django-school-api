from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.

# student model needs to have name, student email, personal email, locker number, locker combination, good student value
class Student(models.Model):
  name = models.CharField(max_length=75, blank=False)
  student_email = models.EmailField(unique=True, null=False)
  personal_email = models.EmailField(unique=True, null=False)
  locker_number = models.IntegerField(unique=True,validators=[MaxValueValidator(500), MinValueValidator(1)], default=110)
  locker_combination = models.CharField(max_length=8, default="12-12-12")
  good_student = models.BooleanField(null=False, default=False)

  def __repr__(self):
    return f"{self.name} - {self.student_email} - {self.locker_number}"
  
  def locker_reassignment(self, new_locker_num):
    self.locker_number = new_locker_num 
    self.save()

  def student_status(self, new_student_rating):
    self.good_student = new_student_rating
    self.save()
