from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveAPIView,ListAPIView
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from core.serializers.auth_serializers import EditProfileSerializer,UserProfileSeriaLizers,UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from core.models import UserProfile
from django.db.models import Q


# Primarily there is no ranking
class DoctorProfileRankingView(ListAPIView):
    serializer_class = UserProfileSeriaLizers
    def get_queryset(self):
        if self.request.GET.get("q"):
            q=self.request.GET.get("q")
        else:
            q=""
        queryset = UserProfile.objects.all().filter(Q(user__user_type=3)&(Q(about__icontains=q)|Q(education__icontains=q)|Q(experience__icontains=q)|Q(speciality__icontains=q))).order_by('?').distinct()
        return queryset