from django.core.exceptions import ValidationError
import re 

def validate_professor(professor):
  error_msg = 'Professor name must be in the format "Professor Adam".'
  regex = r'^([A-Z][a-z]+ [A-Z][a-z]+)$'

  valid_prof = re.match(regex, professor)
  if valid_prof:
    return professor
  else:
    raise ValidationError(error_msg, params={"professor": professor})
  
def validate_subject(subject_name):
  error_msg = "Subject must be in title case format."
  regex = r'^([A-Z][a-z]+(\s[A-Z][a-z]+)*)$'

  valid_subject = re.match(regex, subject_name)
  if valid_subject:
    return subject_name
  else:
    raise ValidationError(error_msg, params={"subject_name": subject_name})
  
def validate_grade(grade):
  high_val_error_msg = "Ensure this value is less than or equal to 100.0."
  low_val_error_msg = "Ensure this value is equal or higher than 0.00"
  decimal_val_error_msg = "numeric field overflow"
  grade_str = str(grade).replace('.', '')
  if len(grade_str) > 5:
    raise ValidationError(decimal_val_error_msg)
  elif grade > 100.00:
    raise ValidationError(high_val_error_msg)
  elif grade < 0.00:
    raise ValidationError(low_val_error_msg)

