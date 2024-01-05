# students/forms.py
from django import forms
from checkassignment.models import Student
from django import forms
from checkassignment.models import Assignment

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_name', 'student_roll_no', 'student_password']
        widgets = {
            'student_password': forms.PasswordInput(),
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'file']
        

    title = forms.CharField(
        label='Assignment Title',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    file = forms.FileField(
        label='Choose a file',
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
