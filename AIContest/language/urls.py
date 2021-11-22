from django.conf.urls import url
from AIContest.language import views


urlpatterns = [
    url(r'get-languages$', views.getLanguages),
    url(r'create-language$', views.createLanguage),
    url(r'update-language$', views.updateLanguage),
    url(r'delete-language$', views.deleteLanguage)
]
