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
