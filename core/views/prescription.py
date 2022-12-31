from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from ..serializers.prescription import PrescriptionSerializer, MedicineSerializer
from ..models import UserProfile,Prescription
from django.db.models import Q

# Permissions
# 
# Permission to for doctor only
class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type=="3"

# Permission to read the prescription
class canReadThePrescription(BasePermission):
    def has_object_permission(self, request, view, obj):
        profile = UserProfile.objects.get(user=request.user)
        return obj.doctor == profile or obj.patient == profile

#Views 
# 
# Create prescription
class PrescriptionCreate(CreateAPIView):
    permission_classes = [IsAuthenticated,IsDoctor]
    serializer_class = PrescriptionSerializer

# Get list prescriptions
class PrescriptionList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrescriptionSerializer
    def get_queryset(self):
        profile = UserProfile.objects.get(user=self.request.user)
        return Prescription.objects.filter(Q(doctor=profile) | Q(patient=profile))

# Get prescription by id
class PrescriptionDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated,canReadThePrescription]
    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all()
