from django.test import TestCase, Client
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory

from external.models import Server
from author.models import UserDetails, FriendRelationship

from timeline.models import Post, Comment

import uuid
import json

# To send HTTP requests
c = Client()
f = APIRequestFactory()

# Values to be inserted and checked in the Author model
USERNAME = 'programmer'
GITHUB_USERNAME = "programmer"
BIO = "This is my witty biography!"

# Values to be inserted and checked in the User model
# required User model attributes

USER_A = {'username':"User_A", 'password':uuid.uuid4()}

# Values to be inserted and checked in the UserDetails model

# optional User model attributes
FIRST_NAME = "Jerry"
LAST_NAME = "Maguire"
EMAIL = "jmaguire@smi.com"
PASSWORD = str(uuid.uuid4())

# Post attributes
TEXT = "Some post text"

class TimelineAPITestCase(TestCase):
    """
    Testing Timeline API Prototypes
    """
    def setUp(self):

        self.user_a = User.objects.create_user(**USER_A)
        self.user_a.save()
        self.server = Server.objects.create(address='example.com')

        self.user_details = UserDetails.objects.create(user = self.user_a,
            github_username = GITHUB_USERNAME + 'A',
            bio = BIO + 'A',
            server = self.server)

        self.user_dict = {
            'username':USERNAME,
            'first_name':FIRST_NAME,
            'last_name':LAST_NAME,
            'password':PASSWORD,
            'email':EMAIL,
            'github_username':GITHUB_USERNAME,
            'bio':BIO }

        self.post = Post.objects.create(text = TEXT,
            user = self.user_a)

        self.auth_headers = {
            'HTTP_AUTHORIZATION': "" }

    def tearDown(self):
        """Remove all created objects from mock database"""
        UserDetails.objects.all().delete()
        User.objects.all().delete()
        Post.objects.all().delete()

    def test_create_post(self):
        response = c.post('/author/post', {'text':TEXT}, format='json')


        # Retrieve uploaded post manually
        pass

    def test_create_post_authentication(self):
        # Not authenticated, can't create a post
        response = c.post('/author/post', {'text':TEXT}, format='json')
        self.assertEquals(response.status_code, 401)

    def test_create_post_bad_fields(self):
        pass

    # def test_delete_post(self):
    #     pass
    #
    # def test_delete_post_authentication(self):
    #     pass
    #
    # def test_delete_post_not_owner(self):
    #     pass
    #
    # def test_delete_post_fail(self):
    #     pass
