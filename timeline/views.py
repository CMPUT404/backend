from django.shortcuts import render
from django.http import Http404

from author.models import User
from author.models import UserDetails

from timeline.models import Post, Comment
from timeline.serializers import (
    PostSerializer,
    IncomingPostSerializer,
    PostsSerializer,
    CommentSerializer )
from timeline.permissions import IsFriend, IsOwner

from rest_framework.views import APIView
from rest_framework import mixins, generics
from rest_framework.response import Response
from rest_framework import authentication, permissions

import json

class MultipleFieldLookupMixin(object):
    """Allows the lookup of multiple fields in an url for mixins"""
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)

class CreatePost(APIView):
    """Create posts using an authenticated user's credentials"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        serializer = IncomingPostSerializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
# class DeletePost(MultipleFieldLookupMixin, generics.DestroyAPIView):
#     """Delete posts using an authenticated user's credentials"""
#
#     authentication_classes = (authentication.TokenAuthentication,)
#
#     # TODO need is owner authentication permission
#     permission_classes = (permissions.IsAuthenticated,)
#
#     queryset = Post.objects.all()
#     serializer_class = PostsSerializer
#     lookup_fields = ('id',)

class GetPosts(APIView):
    permission_classes = (IsOwner, IsFriend,)

    def get_object(self, username):
        """
        Returns a list of Posts associated with a UserDetail's (User) uuid field.

        See https://docs.djangoproject.com/en/1.7/topics/db/queries/#spanning-multi-valued-relationships
        for information about quering foriegn keys that span multiple objects.
        """
        try:
            return Post.objects.filter(user__username=username)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        posts = self.get_object(username)

        serializer = PostsSerializer(posts, many=True)

        # Insert mock external server data into the response
        # No, this is not a good way of doing this and can actually be coded into PostSerializer
        # pl = json.dumps(serializer.data)
        # pl = json.loads(pl)
        # pl += self.get_extern_posts(1)

        return Response(serializer.data)

    def get_extern_posts(self, uuid):
        """Returns a list posts from external nodes"""

        # Pretend that we GET external posts here
        # Will eventually be handled with threading in seperate module.
        # Mock data with a date in the future for testing sorting

        return [{'user':{'username':'jmaguire', 'first_name':'Jerry', 'last_name':'Maguire'}, 'date': '2015-02-25', 'text': u'You complete me', 'image': None, 'id': 99,}]
