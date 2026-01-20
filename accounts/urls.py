from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
# create urls here..

app_name='account'

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('logout/',views.logout_view,name='logout'),
    path("account/", views.MyaccountView.as_view(), name="account"),
    path("create/", views.CreatePfpView.as_view(), name="create_pfp"),
    path('updatepfp/',views.UpdatePfpView.as_view(),name='update_pfp'),
    path('passwordchange/',views.PasswordChangeView.as_view(),name='password_change'),
    path("passwodrest/", auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'),name="password_reset"),
    path("reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'),name="password_reset_done"), 
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'),name="password_reset_confirm"),
    path("passwordreset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'),name="password_reset_complete"),
 ]