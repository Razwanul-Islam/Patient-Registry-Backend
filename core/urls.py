from core.views.discussion_view import *
from django.contrib import admin
from django.urls import path
from core.views.authView import *
from core.views.patient_records import *
from core.views.profileView import *
from core.views.doctorProfile import *
from core.views.appointment_notification_view import *
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    #Doctor profile data
    path('doctors',DoctorProfileRankingView.as_view(),name="doctors"),
    path('login', LoginView.as_view(),name='login'),
    path('registration',RegistrationView.as_view(),name='registration'),
    path('profile/me',GetUserProfileView.as_view(),name="get_user_profile"),
    path('profile/me/update',UpdateProfile.as_view(),name='update_self_profile'),
    path('profile/doctor/<int:pk>',DoctorProfileView.as_view(),name='doctor_profile'),
    # Patient Records
    path('patient-record/get-all',ViewPatientRecords.as_view(),name='view_patient_records'),
    path('patient-record/get/<int:id>',ViewPatientSingleRecord.as_view(),name='view_patient_single_record'),
    path('patient-record/delete/<int:id>',DeletePatientSingleRecord.as_view(),name='delete_patient_single_record'),
    path('patient-record/create',CreatePatientRecord.as_view(),name='create_patient_record'),
    path('patient-record/update',CreatePatientRecord.as_view(),name='update_patient_record'),
    # Discussion
        #Post
    path('discussion/post/<int:id>',SingelPostView.as_view(),name='singel_post_view'),
    path('discussion/posts',multiplePostVIew.as_view(),name='multiple_post_view'),
    path('discussion/post/create',createPostView.as_view(),name='create_post_view'),
    path('discussion/post/update/<int:id>',updatePostView.as_view(),name='update_post_view'),
    path('discussion/post/delete/<int:id>',deletePostView.as_view(),name='delete_post_view'),
            # vote for post
    path('discussion/post/<int:id>/vote',VoteOfPost.as_view(),name='vote_for_post'),
        # Comment
    path('discussion/post/<int:id>/comment/create',Comment.as_view(),name='post_comment_view'),
    path('discussion/post/<int:id>/comments',GetAllCommentOfPost.as_view(),name='get_all_comments'),
    path('discussion/comment/<int:id>/edit',EditCommentView.as_view(),name='edit_comment'),
    path('discussion/comment/<int:id>/delete',DeleteCommentView.as_view(),name='delete_comment'),
            # vote for comment
    path('discussion/comment/<int:id>/vote',VoteOfComment.as_view(),name='vote_for_comment'),
        # Sub Comment
    path('discussion/comment/<int:id>/subcomment/create',SubComment.as_view(),name='post_sub_comment_view'),
    path('discussion/comment/<int:id>/subcomments',GetAllSubCommentOfComment.as_view(),name='get_all_subcomments'),
    path('discussion/subcomment/<int:id>/edit',EditSubCommentView.as_view(),name='edit_subcomment'),
    path('discussion/subcomment/<int:id>/delete',DeleteSubCommentView.as_view(),name='delete_subcomment'),
            # vote for subcomment
    path('discussion/subcomment/<int:id>/vote',VoteOfSubComment.as_view(),name='vote_for_subcomment'),

    # Appointment & Notification
    path("appointments",GetAppointments.as_view(),name="get_appointments"),
    path('appointment/request/<int:id>',AppointmentRequest.as_view(),name="appointment_request"),
    path('appointment/<int:id>',GetSingleAppointment.as_view(),name="get_single_appointment"),
    path('notifications',GetNotification.as_view(),name="get_user_notification"),
    path('notification/update/<int:pk>',UpdateNotification.as_view(),name="update_notification"),
    path('appointment/update/<int:pk>',UpdateAppointment.as_view(),name="update_appointment")
]
urlpatterns=format_suffix_patterns(urlpatterns)