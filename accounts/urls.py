from django.urls import path
from django.views import View
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('',auth_views.LoginView.as_view(template_name='signin.html'),name='signin'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('change_password/',auth_views.PasswordChangeView.as_view(template_name='change_password.html'),name='change_password'),
    path('change_password/done/',auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'),name='password_change_done'),
    path('signup/choose_fields/',views.choose_fields,name='choose_fields'),
    path('account/',views.account,name='account')
    ]
urlpatterns += staticfiles_urlpatterns()