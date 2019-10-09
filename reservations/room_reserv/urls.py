from django.contrib import admin
from django.urls import path, re_path
from room_reserv.views import *

urlpatterns = [
    path('', AllRooms.as_view()),
    path('room/new', AddRoom.as_view()),
    path('room/<int:room_id>', RoomDetails.as_view()),
    path('reservation/<int:room_id>', RoomDetails.as_view()),
    path('room/modify/<int:room_id>', EditRoom.as_view()),
    path('room/delete/<int:room_id>', DeleteRoom.as_view()),
    path('search', room_search),
]
