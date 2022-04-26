from rest_framework import status
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView,ListAPIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.status import HTTP_404_NOT_FOUND
from core.models import Notification,UserProfile,Appointment,Meeting
from core.serializers.appointment_notification import *
from django.core.paginator import Paginator
from django.db.models import Q, query
from uuid import uuid4

#Get notification for a user with pagination
class GetNotification(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    def get_queryset(self):
        queryset = Notification.objects.filter(user=UserProfile.objects.get(user=self.request.user)).order_by("-created_at")
        return queryset
    def list(self, request, *args, **kwargs):
        response= super().list(request, *args, **kwargs)
        non_viewed = self.get_queryset().filter(is_viewed=False).count()
        response.data["non_viewed"] = non_viewed
        return response
# Update notification pertially
class UpdateNotification(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    models=Notification
    serializer_class = NotificationSerializer
    queryset=Notification.objects.all()
    def partial_update(self, request, *args, **kwargs):
        return super(UpdateNotification,self).partial_update(request, *args, **kwargs)

class AppointmentRequest(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,**kwargs):
        id=kwargs.get("id")
        doctorProfile = UserProfile.objects.get(id=id)
        user=UserProfile.objects.get(user=request.user)
        existAppointment = Appointment.objects.filter(doctor=doctorProfile,patient=user).exclude(Q(status="finished")|Q(status="cancelled")).count()
        if user.id == id :
            return Response({"error":"You cannot appointment yourself"},status=HTTP_404_NOT_FOUND)
        elif doctorProfile.user.user_type!='3':
            return Response({"error":"Appointment only doctor"},status=HTTP_404_NOT_FOUND)
        elif existAppointment:
            return Response({"error":"Already a appointment exist"},status=HTTP_404_NOT_FOUND)
        else:
            appointment_request = Appointment.objects.create(doctor=doctorProfile,patient=user)
            notificationDoctor = Notification.objects.create(user=doctorProfile,title="You have new appointment request",description=user.full_name+" just request you for a appointment.",link="/appointment/"+str(appointment_request.id))
            notificationPatient = Notification.objects.create(user=user,title="Successfully requested!",description="Please wait until doctor confirmation",link="/appointment/"+str(appointment_request.id))
            return Response({"appointment_id":appointment_request.id})
#Get appointments list
class GetAppointments(ListAPIView):
    permission_classes =[permissions.IsAuthenticated]
    model = Appointment
    serializer_class = AppointmentSerializer

    def get_queryset(self,**kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        if self.request.GET.get("status"):
            status=self.request.GET.get("status")
        else:
            status=""
        queryset = Appointment.objects.filter(Q(status__icontains=status)&(Q(doctor=user)|Q(patient=user))).order_by('-created_at')
        return queryset
#Get single appointment with ID
class GetSingleAppointment(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,**kwargs):
        id=kwargs.get("id")
        user = UserProfile.objects.get(user=request.user)
        appointment = Appointment.objects.get(Q(id=id)&(Q(doctor=user)|Q(patient=user)))
        if appointment.DoesNotExist:
            serializedData=AppointmentMeetingSerializer(appointment)
            return Response({'appointment':serializedData.data})
        else:
            return Response({'error':"Appointment does not exist !"},status=HTTP_404_NOT_FOUND)

class UpdateAppointment(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    models=Appointment
    serializer_class = AppointmentSerializer
    queryset=Appointment.objects.all()
    def partial_update(self, request, *args, **kwargs):
        return super(UpdateAppointment,self).partial_update(request, *args, **kwargs)