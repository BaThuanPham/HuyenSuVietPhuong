from django import forms
from .models import CandidateProfile
class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['full_name', 'email', 'phone_number','address','cv_file', 'skills', 'experience', 'education']
        labels = {
            'full_name': 'Họ và Tên',
            'email': 'Email',
            'phone_number': 'Số Điện Thoại',
            'address': 'Địa Chỉ',
            'cv_file': 'Tải Lên CV',
            'skills': 'Kỹ Năng',
            'experience': 'Kinh Nghiệm Làm Việc',
            'education': 'Trình Độ Học Vấn',
        }
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
            'experience': forms.Textarea(attrs={'rows': 5}),
            'education': forms.Textarea(attrs={'rows': 5}),
        }
    def clean_cv_file(self):
        cv_file = self.cleaned_data.get('cv_file')
        if cv_file:
            if not cv_file.name.endswith(('.pdf', '.doc', '.docx')):
                raise forms.ValidationError("File CV phải là định dạng PDF hoặc DOC/DOCX.")
            if cv_file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Kích thước file CV không được vượt quá 5MB.")
        return cv_file