from rest_framework import serializers
from ..models import Medicine,Prescription, UserProfile
from .auth_serializers import UserProfileSeriaLizers
from .appointment_notification import AppointmentSerializer

# Medicine serializer
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ["id","name","rule"]

# Prescription serializer
class PrescriptionSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)
    medicines = MedicineSerializer(many=True,write_only = True)
    medicine_set = MedicineSerializer("medicine_set",many=True,read_only=True)
    class Meta:
        model = Prescription
        fields = ['id','medicines','medicine_set','appointment','doctor','patient','patient_name','patient_age','patient_sex','created_at','update_at']
        
    def create(self, validated_data):
        medicines_data = validated_data.pop("medicines")
        doctorProfile = UserProfile.objects.get(user=self.context['request'].user)
        prescription = Prescription.objects.create(doctor=doctorProfile,**validated_data)
        for field in medicines_data:
            Medicine.objects.create(prescription=prescription,**field)
        return prescription
        


