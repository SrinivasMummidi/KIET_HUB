"""KIETAPP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from nask import views as nask_views
from users import views as user_views
from video_call import views as video_call_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nask.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html',redirect_authenticated_user=True), name="Kiet-Login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="Kiet-Logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name="password_reset"),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name="password_reset_complete"),
    path('register/', user_views.register, name="Kiet-Register"),
    path('Account/profile/', user_views.profile, name="profile"),
    path('connect/', video_call_views.VideoCall, name='video-call'),
    path('changepwd/', user_views.change_password, name='change_password'),
    path('ManageUser/', user_views.ManageUser, name='Manage-User'),
    path('ManageUser/addUser/', user_views.AddUser, name='add-user'),
    path('ManageUser/addStaff/', user_views.AddStaff, name='add-staff'),
    path('ManageUser/addLeadership/', user_views.AddLeadership.as_view(), name='add-leader'),
    path('ManageUser/updateLeadership/<int:pk>/', user_views.UpdateLeadership.as_view(), name='update-leader'),
    path('ManageUser/addTeam/', user_views.AddTeam.as_view(), name='add-team'),
    path('ManageUser/updateTeam/<int:pk>/', user_views.UpdateTeam.as_view(), name='update-team'),
    path('ManageUser/addGroup/', user_views.CreateGroup.as_view(), name='add-group'),
    path('ManageUser/updateGroup/<int:pk>', user_views.UpdateGroup.as_view(), name='update-group'),
    path('events/', include('events.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
