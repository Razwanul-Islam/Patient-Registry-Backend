from django.db import models
from django.db.models import fields
from rest_framework import serializers
from core.models import Notification,Appointment,Meeting
from uuid import uuid4

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
      model = Notification
      fields ="__all__"
      depth = 1

class MeetingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Meeting
    fields = "__all__"

class AppointmentSerializer(serializers.ModelSerializer):
  class Meta:
      model = Appointment
      fields = "__all__"
      depth = 1
  
  def update(self, instance, validated_data):
    if validated_data.get("status")=="confirmed":
      meeting = Meeting.objects.get_or_create(appointment=instance,token=uuid4())
    return super().update(instance, validated_data)

class AppointmentMeetingSerializer(serializers.ModelSerializer):
  meeting = MeetingSerializer(source='meeting_set',many=True)
  class Meta:
      model = Appointment
      fields = ("doctor","patient","status","payment_method","transaction_id","patient_payment_number","payment_number","appointment_time","created_at","update_at","meeting")
      depth = 1

