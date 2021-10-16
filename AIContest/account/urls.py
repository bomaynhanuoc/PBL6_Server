from django.conf.urls import url
from AIContest.account import views


urlpatterns = [
    url(r'get-accounts$', views.getAccounts),
    url(r'create-account$', views.createAccount),
    url(r'update-account$', views.updateAccount),
    url(r'delete-account$', views.deleteAccount),
    url(r'login-account$', views.loginAccount),
    url(r'logout-account$', views.logoutAccount),
    url(r'check-token$', views.checkToken)
]
