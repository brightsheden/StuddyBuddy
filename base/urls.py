
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('login/', loginPage, name="login"),
    path('register/', registerUser, name="register"),
    path('logout/', logoutUser, name="logout"),
    path('profile/<str:pk>/', userProfile, name="profile"),
    path("room/<str:pk>/", room, name="room"),
    path("create-room/", create_room, name="create-room"),
    path("update-room/<str:pk>/", update_room, name="update-room"),
    path("delete-room/<str:pk>/", delete_room, name="delete-room"),
    path("delete-message/<str:pk>/", delete_message, name="delete-message"),
    path("update-user/", updateUser, name="update-user"),
    path("topics/", Topics, name="topics"),
    path("activity/", activityPage, name="activity"),
    
    
]