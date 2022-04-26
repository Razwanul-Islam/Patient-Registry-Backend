from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveAPIView
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from core.serializers.auth_serializers import EditProfileSerializer,UserProfileSeriaLizers,UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from core.models import UserProfile

class DoctorProfileRankingView(APIView):
    def get(self,request):
        queryset = UserProfile.objects.all().filter(user__user_type=3).order_by('?')[0:20]
        serializedData = UserProfileSeriaLizers(queryset,many=True)
        return Response({"doctors":serializedData.data})