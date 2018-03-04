"""soccerapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers

from django.views.generic import TemplateView

from general.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

admin.site.site_header = "Soccer App Admin"

router = routers.DefaultRouter()
router.register(r'location', LocationViewSet, 'location')
router.register(r'gameevent', GameEventViewSet, 'gameevent')

urlpatterns += [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^account/', include('allauth.urls')),
    url(r"^$", index, name="index"),
    url(r'^docs/$', get_swagger_view(title='API Docs'), name='api_docs'),
    url(r'^api/', include(router.urls)),
    # this url is used to generate email content
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),   
    url(r'^profile/', profile, name="profile"),
    url(r'^location/(?P<id>\d+)', location, name="location"),
    url(r'^game/(?P<id>\d+)', game, name="game"),
    url(r"^upload-image$", upload_image, name="upload-image"),
    url(r'^accept_invitation/(?P<code>.+)', accept_invitation, name="accept_invitation")
]
