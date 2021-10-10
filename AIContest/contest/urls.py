from django.conf.urls import url
from AIContest.contest import views


urlpatterns = [
    url(r'getcontest$', views.getContest),
    url(r'getcontests$', views.getContests),
    url(r'createcontest$', views.createContest),
    url(r'updatecontest$', views.updateContest),
    url(r'deletecontest$', views.deleteContest)
]
