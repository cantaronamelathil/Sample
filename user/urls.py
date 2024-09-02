from django.urls import path
from .views import *


urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('login/',LoginView.as_view(),name='login'),
    path('stafflist/',StaffListView.as_view(),name='stafflist'),
    path('blockstaff/<int:pk>/',BlockStaffView.as_view(),name='blockstaff'),
    path('deleteuser/<int:pk>/',DeleteStaffView.as_view(),name='deleteuser'),
    path('logout/',LogoutView.as_view(),name='logout'),
]




