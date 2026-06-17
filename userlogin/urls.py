from django.urls import path,include
from userlogin import views
from django.contrib.auth import views as auth_views

app_name = 'userlogin'

urlpatterns = [
      #  path('', views.index, name ='index'),
      #  path("user/", include("django.contrib.auth.urls")),
        path('register/',views.register, name ='register'),
        path('login/', views.login_user, name ='login'),
        path('logout/', views.logout_user, name ='logout'),
        path("reset_password/", auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name='password_reset'),
        path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),name='password_reset_sent'),
        path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(),name='password_reset_done'),
        path("reset-password-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
]