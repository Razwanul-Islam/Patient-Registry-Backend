from typing import Text
from django.db.models.query import QuerySet
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from core.serializers.discussion import *
from core.models import DiscussionPost,DiscussionComment,DiscussionCommentVote,DiscussionPostVote,DiscussionSubComment,DiscussionSubCommentVote,UserProfile
from django.contrib.auth import get_user_model
User = get_user_model()
#single object view of discussion
class SingelPostView(APIView):
  def get(self,request,**kwargs):
    try:
        post = DiscussionPost.objects.get(id=kwargs.get('id'))
        postSerializer = Post(post)#sereialize post model by Post serializer
        return Response({'post':postSerializer.data})
    except DiscussionPost.DoesNotExist:
        return Response({'error':'This post doest not exist'},status=status.HTTP_404_NOT_FOUND)

#Multiple post view after visiting discussion page
class multiplePostVIew(APIView):
    def get(self,request,**kwargs):
        querySet = DiscussionPost.objects.all().order_by('-created_at')
        paginated = Paginator(querySet,10)
        if request.GET.get('page'):
            querySet=paginated.get_page(request.GET.get('page'))
        else:
            querySet=paginated.get_page(1)
        datas=Post(querySet,many=True)
        return Response({'posts':datas.data})

#Create a post
class createPostView(CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=Post

# Update a post
class updatePostView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,**kwargs):
        user=request.user
        user_profile = UserProfile.objects.get(user=user)
        try:
            post = DiscussionPost.objects.get(id=kwargs.get('id'),user_profile=user_profile)
            data=request.data
            if data.get('title'):
                post.title = data.get('title')
            if data.get('description'):
                post.description = data.get('description')
            if data.get('patient_details'):
                post.patient_details = data.get('patient_details')
            if data.get('is_closed'):
                post.is_closed = data.get('is_closed')
            post.save()
            return Response({'post':Post(post).data})
        except DiscussionPost.DoesNotExist:
            return Response({'error':'You are not author of this post or this post does not exist'},status=status.HTTP_404_NOT_FOUND)

# Delete a post
class deletePostView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,**kwargs):
        user=request.user
        user_profile = UserProfile.objects.get(user=user)
        try:
            post = DiscussionPost.objects.get(id=kwargs.get('id'),user_profile=user_profile)
            post.delete()
            return Response({'success':'successfully deleted !'})
        except DiscussionPost.DoesNotExist:
            return Response({'error':'You are not author of this post or this post does not exist'},status=status.HTTP_404_NOT_FOUND)
# Vote a post
class VoteOfPost(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,**kwargs):
        postId=kwargs.get('id')
        user_profile = UserProfile.objects.get(user=request.user)
        try:
            post = DiscussionPost.objects.get(id=postId)
            try:
                vote = DiscussionPostVote.objects.get(user_profile=user_profile,post=post)
            except DiscussionPostVote.DoesNotExist:
                vote = DiscussionPostVote.objects.create(user_profile=user_profile,post=post)
            if request.data.get('vote'):
                voteText = request.data.get('vote')
                if voteText=='up' and not vote.up_vote:
                    vote.up_vote=True
                    vote.down_vote = False
                    if post.vote:
                        post.vote +=1
                    else:
                        post.vote = 1
                elif voteText=='down' and not vote.up_vote:
                    vote.up_vote=False
                    vote.down_vote = True
                elif voteText=='up' and vote.up_vote:
                    vote.down_vote = False
                    if post.vote:
                        post.vote +=0
                    else:
                        post.vote = 1
                elif voteText=='down' and not vote.down_vote and vote.up_vote:
                    vote.up_vote= False
                    vote.down_vote = True
                    post.vote -=1
                else:
                    return Response({"error:":"Somethisng not right"+str(vote.up_vote)})
                vote.save()
                post.save()
                postSerailizer = Post(post)
                return Response({'post':postSerailizer.data})
        except DiscussionPost.DoesNotExist:
            return Response({'error':'This post does not exist'},status=status.HTTP_404_NOT_FOUND)
            #### Comment a Post and subcomment a comment ####
# post a Comment on post view
class Comment(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,**kwargs):
        user=request.user
        user_profile = UserProfile.objects.get(user=user)
        try:
            post = DiscussionPost.objects.get(id=kwargs.get('id'))
            comment = DiscussionComment.objects.create(post=post,user_profile=user_profile,text=request.data.get('text'))
            commentSerializer = CommentSerializer(comment)
            return Response({'comment':commentSerializer.data})
        except DiscussionPost.DoesNotExist:
            return Response({'error':'Post does not exist or you entered wrong format of data'},status=status.HTTP_404_NOT_FOUND)
# Delete a comment
class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,**kwargs):
        id = kwargs.get('id')
        user=request.user
        user_profile = UserProfile.objects.get(user=user)
        try:
            comment = DiscussionComment.objects.get(id=id,user_profile=user_profile)
            comment.delete()
            return Response({'success':"Comment deleted successfuly"})
        except DiscussionPost.DoesNotExist:
            return Response({'error':'Comment does not exist'},status=status.HTTP_404_NOT_FOUND)
# Edit a comment
class EditCommentView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,**kwargs):
        id = kwargs.get('id')
        user=request.user
        user_profile = UserProfile.objects.get(user=user)
        try:
            comment = DiscussionComment.objects.get(id=id,user_profile=user_profile)
            if request.data.get('text'):
                comment.text = request.data.get('text')
                comment.save()
            commentSerializer = CommentSerializer(comment)
            return Response({'comment':commentSerializer.data})
        except DiscussionPost.DoesNotExist:
            return Response({'error':'Comment does not exist'},status=status.HTTP_404_NOT_FOUND)
class GetAllCommentOfPost(APIView):
    def get(self,request,**kwargs):
        id = kwargs.get('id')
        try:
            post = DiscussionPost.objects.get(id=id)
            comments = DiscussionComment.objects.all().filter(post=post)
            commentSerializer = CommentSerializer(comments,many = True)
            return Response({'comments':commentSerializer.data})
        except DiscussionComment.DoesNotExist:
            return Response({'error':'Post does not exist'},status=status.HTTP_404_NOT_FOUND)

# Vote a Comment
class VoteOfComment(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,**kwargs):
        id=kwargs.get('id')
        user_profile = UserProfile.objects.get(user=request.user)
        try:
            comment = DiscussionComment.objects.get(id=id)
            try:
                vote = DiscussionCommentVote.objects.get(user_profile=user_profile)
            except DiscussionCommentVote.DoesNotExist:
                vote = DiscussionCommentVote.objects.create(user_profile=user_profile,comment=comment)
            if request.data.get('vote'):
                voteText = request.data.get('vote')
                if voteText=='up' and not vote.up_vote:
                    vote.up_vote=True
                    vote.down_vote = False
                    if comment.vote:
                        comment.vote +=1
                    else:
                        comment.vote = 1
                elif voteText=='down' and not vote.up_vote:
                    vote.up_vote=False
                    vote.down_vote = True
                elif voteText=='up' and vote.up_vote:
                    vote.down_vote = False
                    if comment.vote:
                        comment.vote +=0
                    else:
                        comment.vote = 1
                elif voteText=='down' and not vote.down_vote and vote.up_vote:
                    vote.up_vote= False
                    vote.down_vote = True
                    comment.vote -=1
                else:
                    return Response({'voted':'you already voted'})
                vote.save()
                comment.save()
                commentSerializer = CommentSerializer(comment)
                return Response({'comment':commentSerializer.data})
        except DiscussionComment.DoesNotExist:
            return Response({'error':'This Comment does not exist'},status=status.HTTP_404_NOT_FOUND)
# Comment(subcomment) on a comment
class SubComment(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,**kwargs):
        user=request.user
        user_profile = UserProfile.objects.get(user=user)
        try:
            comment = DiscussionComment.objects.get(id=kwargs.get('id'))
            sub_commnet = DiscussionSubComment.objects.create(comment=comment,user_profile=user_profile,text=request.data.get('text'))
            return Response({'subcomment':SubCommentSerializer(sub_commnet).data})
        except DiscussionPost.DoesNotExist:
            return Response({'error':'Comment does not exist'},status=status.HTTP_404_NOT_FOUND)
# Delete a sub-comment
class DeleteSubCommentView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,**kwargs):
        id = kwargs.get('id')
        user=request.user
        user_profile = UserProfile.objects.get(user=user)
        try:
            subcomment = DiscussionSubComment.objects.get(id=id,user_profile=user_profile)
            subcomment.delete()
            return Response({'success':"Subcomment deleted successfuly"})
        except DiscussionPost.DoesNotExist:
            return Response({'error':'subcomment does not exist'},status=status.HTTP_404_NOT_FOUND)
# Edit a comment
class EditSubCommentView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,**kwargs):
        id = kwargs.get('id')
        user=request.user
        user_profile = UserProfile.objects.get(user=user)
        try:
            subcomment = DiscussionSubComment.objects.get(id=id,user_profile=user_profile)
            if request.data.get('text'):
                subcomment.text = request.data.get('text')
                subcomment.save()
            subcommentSerializer = SubCommentSerializer(subcomment)
            return Response({'subcomment':subcommentSerializer.data})
        except DiscussionPost.DoesNotExist:
            return Response({'error':'subcomment does not exist'},status=status.HTTP_404_NOT_FOUND)
# Get all sub comment of a comment
class GetAllSubCommentOfComment(APIView):
    def get(self,request,**kwargs):
        id = kwargs.get('id')
        try:
            comment = DiscussionComment.objects.get(id=id)
            subcomments = DiscussionSubComment.objects.all().filter(comment=comment)
            subcommentSerializer = SubCommentSerializer(subcomments,many = True)
            return Response({'subcomments':subcommentSerializer.data})
        except DiscussionComment.DoesNotExist:
            return Response({'error':'Comment does not exist'},status=status.HTTP_404_NOT_FOUND)

# Vote a SubComment
class VoteOfSubComment(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,**kwargs):
        id=kwargs.get('id')
        user_profile = UserProfile.objects.get(user=request.user)
        try:
            comment = DiscussionSubComment.objects.get(id=id)
            try:
                vote = DiscussionSubCommentVote.objects.get(user_profile=user_profile)
            except DiscussionSubCommentVote.DoesNotExist:
                vote = DiscussionSubCommentVote.objects.create(user_profile=user_profile)
            if request.data.get('vote'):
                voteText = request.data.get('vote')
                if voteText=='up' and not vote.up_vote:
                    vote.up_vote=True
                    vote.down_vote = False
                    if comment.vote:
                        comment.vote +=1
                    else:
                        comment.vote = 1
                elif voteText=='down' and not vote.up_vote:
                    vote.up_vote=False
                    vote.down_vote = True
                elif voteText=='up' and vote.up_vote:
                    vote.down_vote = False
                    if comment.vote:
                        comment.vote +=0
                    else:
                        comment.vote = 1
                elif voteText=='down' and not vote.down_vote and vote.up_vote:
                    vote.up_vote= False
                    vote.down_vote = True
                    comment.vote -=1
                else:
                    return Response({'voted':'you already voted'})
                vote.save()
                comment.save()
                commentSerializer = SubCommentSerializer(comment)
                return Response({'comment':commentSerializer.data})
        except DiscussionSubComment.DoesNotExist:
            return Response({'error':'This Subcomment does not exist'},status=status.HTTP_404_NOT_FOUND)
