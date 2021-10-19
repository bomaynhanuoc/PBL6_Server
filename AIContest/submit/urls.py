from django.conf.urls import url
from AIContest.submit import views


urlpatterns = [
    url(r'get-submit$', views.getSubmit),
    url(r'view-submit$', views.viewSubmit),
    url(r'get-submits$', views.getSubmits),
    url(r'create-submit$', views.createSubmit)
]
