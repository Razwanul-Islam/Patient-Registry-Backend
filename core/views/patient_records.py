from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from core.models import FieldOfRecord,PatientRecord
from core.serializers.patient_records import *
from django.core.paginator import Paginator
from django.db.models import Q
# View for create or update patient records
class CreatePatientRecord(APIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request):
        user=request.user
        patientRecordSerializer=PatientRecordSerializer(data=request.data, context={'user':user})
        if patientRecordSerializer.is_valid():
            patientRecord=patientRecordSerializer.create()
            Record=PatientRecordForViewSerializer(patientRecord).data
            return Response({'patient_record':Record})
        else:
            return Response(patientRecordSerializer.errors)

# Retrive patinet records with paginator
class ViewPatientRecords(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        querySet=PatientRecord.objects.all().filter(user=request.user)
        Paginated=Paginator(querySet,20)
        if request.GET.get('page'):
            querySet=Paginated.get_page(request.GET.get('page'))
        else:
            querySet=Paginated.get_page(1)
        datas=PatientRecordForViewSerializer(querySet,many=True)
        return Response({'records':datas.data})

# Search patient records
class SearchPatientRecords(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PatientRecordSerializer
    model = PatientRecord
    def get_queryset(self):
        if self.request.GET.get("q"):
            q = self.request.GET.get("q")
        else:
            q=""
        query = PatientRecord.objects.filter(Q(user=self.request.user)&Q(fieldofrecord__text__icontains=q)).distinct()
        return query

# view single patient record
class ViewPatientSingleRecord(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request,*args,**kwargs):
        querySet=PatientRecord.objects.get(user=request.user,id=kwargs.get('id'))
        if querySet.DoesNotExist:
            datas=PatientRecordForViewSerializer(querySet)
            return Response({'record':datas.data})
        else:
            return Response({"error":"You are not author of this record"},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

# Delete a patient record   
class DeletePatientSingleRecord(APIView):
    permission_classes=(IsAuthenticated,)
    def delete(self,request,*args,**kwargs):
        querySet=PatientRecord.objects.get(user=request.user,id=kwargs.get('id'))
        querySet.delete()
        return Response({'message':"success fully deleted"})
