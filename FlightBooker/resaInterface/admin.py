from django.contrib import admin
from .models import School,Course, Reservation

# Register your models here.

admin.site.register(School)
admin.site.register(Course)
admin.site.register(Reservation)
