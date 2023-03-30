import os
from datetime import datetime
from django.db import models
from django.conf import settings


def get_image_path(instance, filename):
    return os.path.join('images', 'school', str(instance.id), filename)


class School(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return f'Nom de l\'école : {self.name} - Adresse : {self.address}'


def get_course_image_path(instance, filename):
    return os.path.join('images', 'courses', str(instance.id), filename)

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to=get_course_image_path, blank=True, null=True)

    def __str__(self):
        return self.title


class Reservation(models.Model):
    TIME_CHOICES = (
        ("8h", "8h-9h"),
        ("9h", "9h-10h"),
        ("10h", "10h-11h"),
        ("11h", "11h-12h"),
        ("14h", "14h-15h"),
        ("15h", "15h-16h"),
        ("16h", "16h-17h"),
        ("17h", "17h-18h"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now, blank=True)
    time = models.CharField(max_length=50, choices=TIME_CHOICES, default="8h")

    def __str__(self):
        return f'{self.user} a réservé un créneau le {self.date} pour le cours {self.course.title} à l\'école {self.school}'
