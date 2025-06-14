from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import RecruiterProfile

class CandidateSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'candidate'
        if commit:
            user.save()
        return user

class CandidateSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'candidate'
        if commit:
            user.save()
        return user

class RecruiterSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=255, required=True, label="Tên công ty")
    phone = forms.CharField(max_length=20, required=True, label="Số điện thoại")
    company_address = forms.CharField(max_length=255, required=True, label="Địa chỉ công ty")
    company_website = forms.URLField(required=False, label="Website công ty")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {field: '' for field in fields}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'recruiter'
        if commit:
            user.save()
            RecruiterProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                phone=self.cleaned_data['phone'],
                company_address=self.cleaned_data['company_address'],
                company_website=self.cleaned_data['company_website'],
            )
        return user

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['company_name', 'phone', 'company_address', 'company_website']