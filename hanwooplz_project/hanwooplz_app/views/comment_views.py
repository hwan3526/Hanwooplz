"""
파일명: comment_views.py
작성자: 양승조 HidSquid97
작성일: 2023. 10. 24.
설명: 댓글 기능을 Django REST Framework를 이용하여 구현

댓글 관리 API 뷰:
- CommentList: 해당 게시물에서 댓글 작성 및 조회
- CommentDetail: 특정 댓글을 수정 및 삭제
- CommentLikeView: 댓글 좋아요 추가 및 취소
"""
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import *

class CommentList(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post (self, request):
        author = request.user.id if request.user.is_authenticated else None

        comment_data = {
            "content": request.data.get("content"),
            "author": author,
        }
        serializer = CommentSerializer(data=comment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentDetail(APIView):
    def get(self, request, pk):
        comment = get_object_or_404(comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def put(self, request, pk):
        comment = get_object_or_404(comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        comment = get_object_or_404(comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CommentLikeView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        user = request.user

        if user in comment.likes.all():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)

        comment.save()
        return Response(self.get_serializer(comment).data)