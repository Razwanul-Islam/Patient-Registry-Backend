from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveAPIView
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from core.serializers.auth_serializers import EditProfileSerializer,UserProfileSeriaLizers,UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from core.models import UserProfile

class UpdateProfile(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def put(self,request):
        user = request.user
        userSerializer = UserSerializer(user)
        editProfileSerializer = EditProfileSerializer(data=request.data,context={'user':request.user})
        # if editProfileSerializer.is_valid():
        editProfileSerializer.update()
        userData=UserSerializer(user)
        userProfile=UserProfile.objects.get(user=user)
        userProfileSeriaLizers = UserProfileSeriaLizers(userProfile)
        return Response({'user_data':userData.data,'user_profile':userProfileSeriaLizers.data})
class DoctorProfileView(APIView):
    def get(self,request,*args,**kwargs):
        profile=UserProfile.objects.select_related('user').get(id=kwargs.get('pk'))
        serializeData=UserProfileSeriaLizers(profile)
        return Response({'profile':serializeData.data})


        # else:
        #     return Response({"error":editProfileSerializer.error_messages})
