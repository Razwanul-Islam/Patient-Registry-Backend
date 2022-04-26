from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from core.serializers.auth_serializers import LoginSerializers,RegistrationSerializers,UserProfileSeriaLizers,UserSerializer
from django.contrib.auth import get_user_model,login
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from core.models import UserProfile
User = get_user_model
class LoginView(APIView):
    def post(self,request,*args,**kwargs):
        serializer = LoginSerializers(data=request.data, context={'request':request})
        user = serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        update_last_login(None,user)
        login(request,user)
        token,created = Token.objects.get_or_create(user=user)
        userData = UserSerializer(user)
        userProfile=UserProfileSeriaLizers(UserProfile.objects.get(user=user))
        return Response({"token":token.key,"userProfile":userProfile.data,'userData':userData.data})

class GetUserProfileView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        user = request.user
        user_Profile=UserProfileSeriaLizers(UserProfile.objects.get(user=user))
        return Response({"userProfile":user_Profile.data})

class RegistrationView(CreateAPIView):
    model = User
    permission_classes=[permissions.AllowAny]
    serializer_class = RegistrationSerializers

# Create your views here.
