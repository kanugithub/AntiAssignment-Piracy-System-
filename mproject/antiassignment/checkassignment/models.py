from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# students/models.py
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User

# Custom validator for roll number format
validate_roll_number = RegexValidator(
    regex=r'^[A-Z]{3}\d{6}$',
    message='Roll number must be in the format: AAA123456',
)

# Custom validator for password format
validate_password_format = RegexValidator(
    regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$',
    message='The password must contain at least one uppercase letter, one lowercase letter, and one digit.',
)



class Student(models.Model):
    student_name = models.CharField(max_length=100)
    student_roll_no = models.CharField(max_length=15, unique=True,validators=[validate_roll_number])
    student_password = models.CharField(max_length=128,validators=[validate_password_format])  # Store hashed passwords
    def __str__(self):
        return self.student_roll_no

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)  # Adding a title field
    file = models.FileField(upload_to='assignments/')
    extracted_text = models.TextField(blank=True, null=True)

class DWMAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='math_assignments/')

class CGMAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='science_assignments/')

class MLAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='history_assignments/')

class BIGDATAAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='history_assignments/')

class TOCAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='history_assignments/')    