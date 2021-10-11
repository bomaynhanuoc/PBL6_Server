from django.conf.urls import url
from AIContest.account import views


urlpatterns = [
    url(r'getaccounts$', views.getAccounts),
    url(r'createaccount$', views.createAccount),
    url(r'updateaccount$', views.updateAccount),
    url(r'deleteaccount$', views.deleteAccount),
    url(r'loginaccount$', views.loginAccount),
    url(r'logoutaccount$', views.logoutAccount)
]
