from django.urls import path
from . import views

urlpatterns = [
    path('page/', views.page, name='page'),
    path('profiles/upload/', views.upload_profile_image, name='upload_profile'),
    path('list/',views.course_student_list, name='course_student_list'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/panel/', views.teacher_panel, name='teacher_panel'),
    path('schedule/', views.course_schedule, name='course_schedule'),


]
