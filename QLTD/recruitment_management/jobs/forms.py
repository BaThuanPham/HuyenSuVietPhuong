from django import forms
from .models import JobPosting, Application, Interview, Test
class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'description', 'requirements', 'job_type', 'location', 'category','is_active']
        labels = {
            'title': 'Tiêu đề công việc',
            'description': 'Mô tả công việc',
            'requirements': 'Yêu cầu công việc',
            'job_type': 'Loại công việc',
            'location': 'Khu vực làm việc',
            'category': 'Danh mục công việc',
            'is_active': 'Hiển thị công việc',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 7}),
            'requirements': forms.Textarea(attrs={'rows': 7}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = []

class InterviewForm(forms.ModelForm):
    schelduled_time = forms.DateTimeField(
       widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
       label='Thời gian phỏng vấn',
    )
    class Meta:
        model = Interview
        fields = ['scheduled_time', 'round_number', 'status', 'notes']
        labels = {
            'scheduled_time': 'Thời gian phỏng vấn',
            'round_number': 'Vòng phỏng vấn',
            'status': 'Trạng thái',
            'notes': 'Ghi chú',
        }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 5}),
        }
    
class TestForm(forms.ModelForm):
    class Meta:
        fields = ['test_name', 'description', 'test_url']
        labels = {
            'test_name': 'Tên bài kiểm tra',
            'description': 'Mô tả bài kiểm tra',
            'test_url': 'URL bài kiểm tra',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
    