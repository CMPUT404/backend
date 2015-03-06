from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from timeline import views

urlpatterns = [

    # GET  /author/:username/posts
    url(r'^author/(?P<username>[0-9a-zA-Z_]+)/posts$', views.GetPosts.as_view()),

    # POST /author/post
    url(r'^author/post$', views.CreatePost.as_view()),

    # DELETE /author/post/:post_id
    # url(r'^author/post/(?P<page_id>[0-9]+)$', views.DeletePost.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
