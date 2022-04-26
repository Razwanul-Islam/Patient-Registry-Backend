from django.db.models import fields
from core.models import DiscussionCategory, DiscussionPost,DiscussionComment,DiscussionCommentVote,DiscussionPostVote,DiscussionSubComment,DiscussionSubCommentVote, UserProfile
from rest_framework import serializers

class Post(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    class Meta:
        model=DiscussionPost
        fields=['id','title','description','patient_details','user_profile','created_at','update_at','vote','comments']
        depth = 1
    def create(self, validated_data):
        request = self.context.get('request')
        user=self.context.get('request').user
        user_profile = UserProfile.objects.get(user=user)
        post = DiscussionPost.objects.create(user_profile=user_profile,**validated_data)
        if request.GET.get('category'):
            categoryName = request.GET.get('category')
            category = DiscussionCategory.objects.get_or_create(name=categoryName)
            post.category = category[0]
            post.save()
        return post
    def get_comments(self,obj):
        return obj.discussioncomment_set.count()
    
class CommentSerializer(serializers.ModelSerializer):
    sub_comments=serializers.SerializerMethodField()
    class Meta:
        model=DiscussionComment
        fields=['id','text','user_profile','created_at','vote','sub_comments']
        depth = 1
    def get_sub_comments(self,obj):
        return obj.discussionsubcomment_set.count()
class SubCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=DiscussionSubComment
        fields=['id','text','user_profile','created_at','vote']
        depth = 1    