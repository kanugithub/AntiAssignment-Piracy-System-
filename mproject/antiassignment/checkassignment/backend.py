# students/backends.py
from django.contrib.auth.backends import ModelBackend
from checkassignment.models import Student

class CustomRollNoBackend(ModelBackend):
    def authenticate(self, request, roll_no=None, password=None, **kwargs):
        try:
            student = Student.objects.get(roll_no=roll_no)
            if student.check_password(password):
                return student
        except Student.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            return None
