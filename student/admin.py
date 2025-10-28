from django.contrib import admin
from django.shortcuts import render
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import studentt, teacher, course, enrollments, Profiles
from .models import LessonSchedule


admin.site.register(course)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'year','go_to_statistic')
    search_fields = ('name',)
    list_filter = ('year',)
    ordering = ('name',)
    def go_to_statistic(self, obj):
     url = reverse('page')  # bu URL name ile eşleşmeli
     return format_html('<a class="button" href="{}">Statistics</a>', url)
    go_to_statistic.short_description = "Statistic"
admin.site.register(studentt,StudentAdmin)

class TeacherAdmin(admin.ModelAdmin):
    list_display=('name','department','go_to_grade')
    list_filter=('department',)
    search_fields=('name',)
    def go_to_grade(self, obj):
     url = reverse('teacher_login')  # bu URL name ile eşleşmeli
     return format_html('<a class="button" href="{}">Add Grade</a>', url)
    go_to_grade.short_description = "Add Grade"
admin.site.register(teacher,TeacherAdmin)
class CourseAdmin(admin.ModelAdmin):
    list_display=('name','credit','teacher')
    list_filter=('name')
    ordering=('creadit')
class EnrollmentsAdmin(admin.ModelAdmin):
    list_display=('student','course','status','enrollment_date')
    list_filter=('status')
    search_fields=('student__name','course__name')
    ordering=('enrollment_date')
class ProfileAdmin(admin.ModelAdmin):
    list_display=('student','image','upload_link')
    search_fields=('student_name',)
    def upload_link(self, obj):
        url = reverse('upload_profile')  # urls.py'de tanımladığın isimli url olmalı
        return format_html('<a class="button" href="{}">Upload</a>', url)
    upload_link.short_description = 'Upload Profile Image'
    upload_link.allow_tags = True
admin.site.register(Profiles, ProfileAdmin)
# Register your models here.
class EnrollmentsAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'enrollment_date', 'go_to_course_list')
    list_filter = ('status',)
    search_fields = ('student__name', 'course__name')
    ordering = ('enrollment_date',)

    def go_to_course_list(self, obj):
     url = reverse('course_student_list')  # bu URL name ile eşleşmeli
     return format_html('<a class="button" href="{}">Course List</a>', url)
    go_to_course_list.short_description = "Course List"


admin.site.register(enrollments, EnrollmentsAdmin)
from .forms import LessonScheduleAdminForm
class LessonScheduleAdmin(admin.ModelAdmin):
    form = LessonScheduleAdminForm
    list_display = ('day', 'start_time', 'end_time', 'course', 'teacher','go_to_schedule')
    list_filter = ('day', 'teacher', 'course')
    search_fields = ('course__name', 'teacher__name')
    def go_to_schedule(self, obj):
     url = reverse('course_schedule')  # bu URL name ile eşleşmeli
     return format_html('<a class="button" href="{}">Show Schedule</a>', url)

admin.site.register(LessonSchedule, LessonScheduleAdmin)
