from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from core.models import UserProfile
User = get_user_model()#Get the user model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name','email','user_type']
class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type':'password'},
        write_only=True
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'),username=email,password=password)
            if not user:
                raise serializers.ValidationError("Your email and password doesn't match",code='authorization')
        else:
            raise serializers.ValidationError("Please enter your email and password",code='authorization')
        data["user"]=user
        return user

class RegistrationSerializers(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id','email','first_name','last_name','password','user_type')
        write_only_fields =('password',)
        read_only_fields =('id',)
    def create(self,data):
        user = User.objects.create(email=data.get('email'),username=data.get('email'),first_name=data.get('first_name'),last_name=data.get('last_name'),user_type=int(data.get('user_type')))
        user.set_password(data.get('password'))
        user.save()
        UserProfile.objects.create(user=user,full_name=user.first_name +" "+ user.last_name)
        return user
    
class UserProfileSeriaLizers(serializers.ModelSerializer):
    user=UserSerializer('user')
    class Meta:
        model = UserProfile
        fields = "__all__"

class EditProfileSerializer(serializers.Serializer):
    full_name  = serializers.CharField()
    title = serializers.CharField()
    about = serializers.CharField()
    education = serializers.CharField()
    experience = serializers.CharField()
    speciality = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()
    class Meta:
        fields=['full_name',
                'title',
                'about',
                'education',
                'address',
                'experience',
                'phone',
                'speciality']
    def validate(self,data):
        return True
    def update(self):
        user=self.context.get('user')
        UserProfileObject = UserProfile.objects.get(user=user)
        if self.initial_data.get('full_name'):
            UserProfileObject.full_name=self.initial_data.get('full_name')
        if self.initial_data.get('profile_pic'):
            UserProfileObject.profile_pic=self.initial_data.get('profile_pic')
        if self.initial_data.get('title'):
            UserProfileObject.title=self.initial_data.get('title')
        if self.initial_data.get('phone'):
            UserProfileObject.phone=self.initial_data.get('phone')
        if self.initial_data.get('address'):
            UserProfileObject.address=self.initial_data.get('address')
        if self.initial_data.get('about'):
            UserProfileObject.about=self.initial_data.get('about')
        if self.initial_data.get('education'):
            UserProfileObject.education=self.initial_data.get('education')
        if self.initial_data.get('experience'):
            UserProfileObject.experience=self.initial_data.get('experience')
        if self.initial_data.get('speciality'):
            UserProfileObject.speciality=self.initial_data.get('speciality')
        UserProfileObject.save()
        
        