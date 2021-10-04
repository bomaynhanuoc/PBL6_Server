from django.conf.urls import url
from AIContest.user import views


urlpatterns = [
    url(r'getusers$', views.getUsers),
    url(r'createuser$', views.createUser),
    url(r'updateuser$', views.updateUser)
]
