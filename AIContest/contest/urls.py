from django.conf.urls import url
from AIContest.contest import views


urlpatterns = [
    url(r'get-contest$', views.getContest),
    url(r'get-contests$', views.getContests),
    url(r'create-contest$', views.createContest),
    url(r'add-participant', views.addParticipant),
    url(r'update-contest$', views.updateContest),
    url(r'delete-contest$', views.deleteContest)
]
