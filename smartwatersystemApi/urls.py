

from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    #Auth
    path("admin/", admin.site.urls),
    
    # API
    path("water/",include("mainApp.urls"), name="main_app" ),
    path("auth-person/",include("account.urls"), name="auth_app" ),
    
    # Web App
    re_path(r'^$', views.IndexView.as_view(), name="index_url"),
    path('users/', include('users.urls', namespace="users")),
    
    # Les média
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}),
]
