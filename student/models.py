from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class studentt(models.Model):
    name=models.CharField(max_length=200,help_text="Enter your name")
    number=models.CharField(max_length=20,help_text="Enter your student number",unique=True)
    major=models.CharField(max_length=50,help_text="Enter your major")
    year=models.CharField(max_length=2,help_text="Enter your year")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def __str__ (self):
       return f"{self.number}-{self.name}"
 
class teacher(models.Model):
    name=models.CharField(max_length=200,help_text="Enter your name")
    department=models.CharField(max_length=200,help_text="Enter your departmnet")
    email=models.EmailField(help_text="Enter your email",unique=True)
    def __str__(self):
        return self.name
class course(models.Model):
    name=models.CharField(max_length=50,help_text="Enter course name")
    credit=models.PositiveSmallIntegerField()
    teacher=models.ForeignKey(teacher,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return(self.name)
class enrollments(models.Model):
    student=models.ForeignKey(studentt,on_delete=models.CASCADE)
    course=models.ForeignKey(course,on_delete=models.CASCADE)
    status=models.CharField(max_length=20,choices=[('Active', 'Active'), ('Completed', 'Completed'), ('Withdrawn', 'Withdrawn')], default='Active')
    enrollment_date=models.DateTimeField(default=timezone.now)
    grade = models.IntegerField(null=True, blank=True)
    class Meta:
        unique_together=('student','course')
    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.name}"

class Profiles(models.Model):
    student = models.OneToOneField(studentt, on_delete=models.CASCADE,null=False, related_name='profile')
    image = models.ImageField(upload_to='profiles/', default='profiles/default.jpg')

    def __str__(self):
        return f"{self.student.name} Profiles"
DAYS_OF_WEEK = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]
class LessonSchedule(models.Model):
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.day} - {self.course.name} ({self.start_time} - {self.end_time})"

