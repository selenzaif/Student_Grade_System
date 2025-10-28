from django import forms
from .models import Profiles

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ['image']

from django import forms
from .models import LessonSchedule, course, teacher

class LessonScheduleAdminForm(forms.ModelForm):
    class Meta:
        model = LessonSchedule
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Form POST edilmişse (yeni course seçilmiş olabilir)
        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                selected_course = course.objects.get(id=course_id)
                self.fields['teacher'].queryset = teacher.objects.filter(id=selected_course.teacher.id)
            except (ValueError, course.DoesNotExist):
                self.fields['teacher'].queryset = teacher.objects.none()
        
        # Mevcut instance düzenleniyorsa
        elif self.instance.pk:
            selected_course = self.instance.course
            self.fields['teacher'].queryset = teacher.objects.filter(id=selected_course.teacher.id)
        
        # Yeni kayıt ve course henüz seçilmemişse
        else:
            self.fields['teacher'].queryset = teacher.objects.none()


