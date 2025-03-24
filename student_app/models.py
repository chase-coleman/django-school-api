from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.

# student model needs to have name, student email, personal email, locker number, locker combination, good student value
class Student(models.Model):
  name = models.CharField(max_length=75, blank=False)
  student_email = models.EmailField(unique=True, null=False)
  personal_email = models.EmailField(unique=True, null=False)
  locker_number = models.IntegerField(validators=[MaxValueValidator(500), MinValueValidator(1)])
  locker_combination = models.CharField(max_length=8)
  good_student = models.BooleanField(null=False, default=False)

  def __repr__(self):
    return f"{self.id}, {self.name}, {self.student_email}, {self.personal_email}, {self.locker_number}, {self.locker_combination}, {self.good_student}"
  
