from django.urls import path
from .views import ChatAI

urlpatterns = [
    path("chats/", ChatAI.as_view(), name="chat_ai"),
]
