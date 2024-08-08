from django.shortcuts import render, get_object_or_404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from comment.models import Comment
from comment.serializers import CommentSerializer


class CommentList(APIView):
    def get(self, request, post_id):
        comments = Comment.objects.filter(post=post_id).order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, post_id):
        comment_data = {
            'content': request.data.get('content'),
        }
        serializer = CommentSerializer(data=comment_data)
        if serializer.is_valid():
            serializer.save(author=self.request.user, post_id=post_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentLikeView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        user = request.user

        if user in comment.like.all():
            comment.like.remove(user)
            message = '좋아요가 취소되었습니다.'
        else:
            comment.like.add(user)
            message = ''

        comment.save()
        comment_data = self.get_serializer(comment).data
        context = {'comment_data': comment_data, 'message': message}
        return Response(context, status=status.HTTP_200_OK)
