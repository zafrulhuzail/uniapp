from django import forms
from django.contrib.auth.models import User
from .models import Student, Professor

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('student', 'Student'), ('professor', 'Professor')])
    student_id = forms.IntegerField(required=False)
    employee_id = forms.IntegerField(required=False)

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )

        if self.cleaned_data['role'] == 'student':
            Student.objects.create(
                user=user,
                student_id=self.cleaned_data['student_id'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
        else:
            Professor.objects.create(
                user=user,
                employee_id=self.cleaned_data['employee_id'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )

        return user