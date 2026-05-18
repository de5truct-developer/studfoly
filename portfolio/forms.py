from django import forms
from .models import Project, ProjectImage, Skill, Education, Experience


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'slug', 'description', 'image', 'technologies',
            'demo_url', 'github_url', 'is_featured'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Название проекта'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'url-адрес-проекта'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 6,
                'placeholder': 'Подробное описание проекта...'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'technologies': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Python, Django, JavaScript, React'
            }),
            'demo_url': forms.URLInput(attrs={
                'class': 'form-control', 'placeholder': 'https://demo.example.com'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control', 'placeholder': 'https://github.com/user/repo'
            }),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image', 'caption', 'order']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Подпись к изображению'
            }),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'icon_class', 'percentage', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Название навыка'
            }),
            'icon_class': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fa-brands fa-python'
            }),
            'percentage': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 0, 'max': 100
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'description']
        widgets = {
            'institution': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Название учебного заведения'
            }),
            'degree': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Бакалавр, Магистр и т.д.'
            }),
            'field_of_study': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Направление обучения'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Описание...'
            }),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'position', 'start_date', 'end_date', 'description']
        widgets = {
            'company': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Название компании'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Должность'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Описание обязанностей...'
            }),
        }
