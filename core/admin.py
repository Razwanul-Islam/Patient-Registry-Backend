from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Notification,Appointment
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import PatientRecord
class CustomUserAdmin(UserAdmin):
    list_display=['first_name','last_name','email','user_type']
class PatientRecordAdmin(admin.ModelAdmin):
    list_display=['created_at','user']
class NotificationAdmin(admin.ModelAdmin):
    list_display=['title']
class AppointmentAdmin(admin.ModelAdmin):
    list_display=['status']
admin.site.register(Appointment,AppointmentAdmin)
admin.site.register(Notification,NotificationAdmin)
admin.site.register(User,CustomUserAdmin)
admin.site.register(PatientRecord,PatientRecordAdmin)

# Register your models here.
