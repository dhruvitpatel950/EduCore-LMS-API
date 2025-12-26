from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True,null = True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
class Lesson(models.Model):
    module = models.ForeignKey(Module,on_delete=models.CASCADE,related_name="lessons")
    title = models.CharField(max_length=100)
    content = models.TextField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.title



