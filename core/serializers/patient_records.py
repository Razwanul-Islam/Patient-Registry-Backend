from django.db.models import fields
from core.models import PatientRecord
from rest_framework import serializers
from core.models import FieldOfRecord, PatientRecord

# Serializer for every patient records field


class RegistryFields(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = FieldOfRecord
        fields = ('id', 'name', 'type', 'hint', 'text', 'files')

    def create(self, data):
        if data.get('id'):
            patientField = FieldOfRecord.objects.get(
                id=int(data.get('id')), patient_record=data.get('patient_record'))
            patientField.name = data.get('name')
            patientField.type = data.get('type')
        else:
            patientField = FieldOfRecord(patient_record=data.get(
                'patient_record'), name=data.get('name'), type=data.get('type'))
        if data.get('type') != 'files':
            patientField.text = data.get('text')
        else:
            patientField.files = data.get('files')
        if data.get('hint'):
            patientField.hint = data.get('hint')
        patientField.save()
        return patientField


# Sereializer for save or update patient Record
class PatientRecordSerializer(serializers.ModelSerializer):
    fieldofrecord_set = RegistryFields(many=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = PatientRecord
        fields = ('id', 'fieldofrecord_set', 'created_at', 'update_at')

    def create(self):
        registry_fields_data = self.data.pop('fieldofrecord_set')

        if self.data.get('id'):
            PatientRecordObject = PatientRecord.objects.get(
                id=int(self.data.get('id')), user=self.context.get('user'))
        else:
            PatientRecordObject = PatientRecord.objects.create(
                user=self.context.get('user'))
        registry_fields_serializers = self.fields['fieldofrecord_set']
        
        for field in registry_fields_data:
            field['patient_record'] = PatientRecordObject
        registryFields = registry_fields_serializers.create(
            registry_fields_data)
        return PatientRecordObject


# Serializer for Patient Record
class PatientRecordForViewSerializer(serializers.ModelSerializer):
    fieldofrecord_set = RegistryFields('fieldofrecord_set', many=True)

    class Meta:
        model = PatientRecord
        fields = '__all__'
