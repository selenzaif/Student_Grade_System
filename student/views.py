from django.shortcuts import render
from django.shortcuts import redirect
from .models import studentt,course,teacher,enrollments,Profiles
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ProfileImageForm
from django.contrib import messages
from .models import LessonSchedule


def page(request):
    num_student=studentt.objects.all().count()
    num_teacher=teacher.objects.all().count()
    num_course=course.objects.all().count()
    num_enrollments=enrollments.objects.all().count()

    context={
        'numberofstudent':num_student,
        'numberofteacher':num_teacher,
        'numberofcourse':num_course,
        'numberofenrollments':num_enrollments,
    }
    return render(request,'page.html',context=context)
    
@login_required
def upload_profile_image(request):
   
    student = studentt.objects.filter(user=request.user)
    if not student.exists():
        # Öğrenci yoksa hata mesajı veya yönlendirme yap
        return HttpResponse("Öğrenci bulunamadı.")
    student = student.first()  
    profile = student.profile
    
   
    try:
        profile = student.profile
    except Profiles.DoesNotExist:
        profile = Profiles.objects.create(student=student)
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('page')  # Veya başka bir sayfaya yönlendir
    else:
        form = ProfileImageForm(instance=profile)
    
    return render(request, 'uploadprofile.html', {'form': form})
def home(request):
    return render(request, 'student/home.html')

def course_student_list(request):
    enrollment_list = enrollments.objects.select_related('student', 'course', 'course__teacher')
    return render(request, 'course_student_list.html', {'enrollments': enrollment_list})

def statistic_list(request):
    return render(request,'page.html')

#for teacher register
def teacher_login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        try:
            current_teacher = teacher.objects.get(name=name, email=email)
            request.session['teacher_email'] = current_teacher.email
            return redirect('teacher_panel')
        except teacher.DoesNotExist:
            return render(request, 'teacher_login.html', {'error': 'No teacher found.'})

    return render(request, 'teacher_login.html')

from django.views.decorators.csrf import csrf_exempt
#for note inputs
@csrf_exempt
def teacher_panel(request):
    teacher_email = request.session.get('teacher_email')
    if not teacher_email:
        return redirect('teacher_login')
    try:
        current_teacher = teacher.objects.get(email=teacher_email)
    except teacher.DoesNotExist:
        messages.error(request, "No teacher found.")
        return redirect('teacher_login')

    current_teacher = teacher.objects.get(email=teacher_email)
    courses = course.objects.filter(teacher=current_teacher)
    enrolled_students = enrollments.objects.filter(course__in=courses).select_related('student', 'course')
    submitted_grades = []  # kaydı tutmak için


    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('grade_'):
                enrollment_id = key.split('_')[1]
                try:
                    enrollment = enrollments.objects.get(id=enrollment_id)
                except (ValueError, enrollments.DoesNotExist):
                    continue  
                try:
                    new_grade = int(value)

                except ValueError:
                 continue  
                if 0 <= new_grade <= 5:
                    # Eğer not zaten varsa güncelleme isteği sor
                    if enrollment.grade is not None:
                        confirm_key = f'confirm_update_{enrollment_id}'
                        confirm_value = request.POST.get(confirm_key, 'no')

                        if confirm_value == 'yes':
                            if enrollment.grade != new_grade:
                                enrollment.grade = new_grade
                                enrollment.save()
                                submitted_grades.append(enrollment)
                                messages.success(request, f"{enrollment.student.name} for the grade is updated")
                            else:
                                messages.info(request, f"{enrollment.student.name} for the grade is already at this value.")
                        else:
                            messages.info(request, f"{enrollment.student.name} for the grade is not updated.")
                    else:
                        # Not yoksa direkt kaydet
                        enrollment.grade = new_grade
                        enrollment.save()
                        submitted_grades.append(enrollment)
                        messages.success(request, f"{enrollment.student.name} 'grade is recorded")
                else:
                    messages.error(request, f"Grade should between 0 and 5: {new_grade}")
             
    submitted_grades = enrollments.objects.filter(course__in=courses).exclude(grade__isnull=True).select_related('student', 'course')        
    context = {
        'teacher': current_teacher,
        'enrollments': enrolled_students,
        'submitted_grades': submitted_grades,
        'messages': messages.get_messages(request),
    }

    return render(request, 'teacher_panel.html', context)
def course_schedule(request):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    schedule_by_day = {}

    for day in days:
        schedule_by_day[day] = LessonSchedule.objects.filter(day=day).order_by('start_time')

    return render(request, 'course_schedule.html', {'schedule_by_day': schedule_by_day})
                 
