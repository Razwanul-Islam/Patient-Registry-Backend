from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import signals
from django.db.models.fields import BooleanField, CharField, IntegerField, UUIDField
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
                    ##########################################
                    # User Profile and Authentication Models #
                    ##########################################

class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Patient"), (3, "Doctor"))
    email = models.EmailField(max_length=254, unique=True)
    user_type = models.CharField(
        default=2, choices=user_type_data, max_length=10)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    class Meta:
        unique_together = ['email', "username"]

    objects = UserManager()


class AutoFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class UserProfile(AutoFields):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True)
    full_name  = models.CharField(max_length = 150,default='Full Name')
    title = models.CharField(max_length=150,default='Doctor')
    sex = models.CharField(max_length=50,default="Male")
    profile_pic = models.ImageField(upload_to='images/user/profile_pic',null=True)
    about = models.TextField(null=True)
    education = models.TextField(null=True)
    appointment_fee = models.IntegerField(null=True)
    experience = models.TextField(null=True)
    speciality = models.CharField(max_length = 200)
    phone = models.CharField(max_length = 15,null=True)
    address = models.CharField(max_length=200,null=True)

                                    ###########################
                                    # Patient Registry Models #
                                    ###########################

class PatientRecord(AutoFields):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class FieldOfRecord(models.Model):
    patient_record = models.ForeignKey(PatientRecord, on_delete=models.CASCADE)
    name = models.TextField()
    type = models.TextField()
    hint = models.TextField(null=True,blank=True)
    text = models.TextField(null=True,blank=True)
    files = models.FileField(upload_to='files/patient/pathology_and_others',null=True,blank=True)
    
                                    ###########################
                                    #        Discussion       #
                                    ###########################
class Vote(AutoFields):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    up_vote = models.BooleanField(default=False)
    down_vote = models.BooleanField(default=False)
    class Meta :
        abstract = True
class DiscussionCategory(AutoFields):
    name = models.CharField(max_length = 150,unique=True)
    description = models.TextField(null=True)
    thumbnail = models.ImageField(upload_to='images/discussion/category_thumbnails',null=True)
    
class DiscussionPost(AutoFields):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(DiscussionCategory, on_delete=models.CASCADE,null=True)
    title = models.TextField()
    description = models.TextField(null=True,blank=True)
    patient_details = models.TextField(null=True,blank=True)
    category = models.ForeignKey(DiscussionCategory, on_delete=models.CASCADE,null=True)
    vote = models.IntegerField(null=True)
    is_closed = models.BooleanField(default=False)

class DiscussionComment(AutoFields):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(DiscussionPost, on_delete=models.CASCADE)
    text = models.TextField()
    vote = models.IntegerField(null=True)
    
class DiscussionSubComment(AutoFields):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(DiscussionComment, on_delete=models.CASCADE)
    text = models.TextField()
    vote = models.IntegerField(null=True)

class DiscussionPostVote(Vote):
    post = models.ForeignKey(DiscussionPost, on_delete=models.CASCADE)
class DiscussionCommentVote(Vote):
    comment = models.ForeignKey(DiscussionComment, on_delete=models.CASCADE)
class DiscussionSubCommentVote(Vote):
    sub_comment = models.ForeignKey(DiscussionSubComment, on_delete=models.CASCADE)
      
                   ########################################
                   #      Notification  & Appointment     #
                   ########################################

class Notification(AutoFields):
  user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  title = models.TextField()
  description = models.TextField()
  link = models.URLField(max_length = 200,null=True)
  is_viewed = models.BooleanField(default=False)

  def as_dict(self):
      return{
          "id":"%d"%self.id,
          "user":self.user.id,
          "title":self.title,
          "description":self.description,
          "link":self.link,
          "is_viewed":self.is_viewed,
          "created_at":self.created_at.strftime("%Y-%m-%d %H:%M"),
          "update_at":self.update_at.strftime("%Y-%m-%d %H:%M"),
      }

class Appointment(AutoFields):
    doctor = models.ForeignKey(UserProfile,related_name="doctorProfile", on_delete=models.CASCADE)
    patient = models.ForeignKey(UserProfile,related_name="patientProfile", on_delete=models.CASCADE)
    status = models.CharField(max_length = 80,default="draft")
    payment_method = models.CharField(max_length = 150,null=True)
    transaction_id = models.CharField(max_length = 150,null=True)
    patient_payment_number = models.CharField(max_length = 20,null=True)
    payment_number = models.CharField(max_length=20,null=True)
    appointment_time = models.DateTimeField(null=True)

class Meeting(AutoFields):
    appointment = models.ForeignKey(Appointment,unique=True, on_delete=models.CASCADE)
    token = models.CharField(max_length = 100)
    link = models.CharField(max_length = 150,null=True)

    def as_dict(self):
        return {
            "id":self.id,
            "appointment":self.appointment.id,
            "token":self.token
        }
