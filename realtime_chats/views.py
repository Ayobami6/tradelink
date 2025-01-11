from django.shortcuts import render
from rest_framework.views import APIView
from sparky_utils.response import service_response
from sparky_utils.advice import exception_advice
from firebase_admin import db
from rest_framework.permissions import AllowAny
from asgiref.sync import sync_to_async
from datetime import datetime

# Create your views here.


class RootView(APIView):
    """Initial Root page"""

    def get(self, request):
        return service_response(
            status="success",
            message="Welcome to Realtime Chats",
            data={},
            status_code=200,
        )


class ChatAI(APIView):
    """Chat AI Page"""

    permission_classes = [AllowAny]

    @exception_advice
    def post(self, request, *args, **kwargs):
        data = request.data
        chat_id = data.get("chat_id")
        print(chat_id)
        message_id = data.get("message_id")
        db_ref = db.reference(f"/")
        chats_ref = db_ref.child(chat_id)
        message_ref = chats_ref.child(message_id)
        message = message_ref.get()
        print(message)
        # Will process the message with AI and add the AI message
        chats_ref.push(
            {
                "message": "This is new AI message",
                "sender": "AI",
                "timestamp": datetime.now().timestamp(),
                "usernames": "GetLinkedAI",
            }
        )
        return service_response(
            status="success",
            message="Chat AI",
            data={},
            status_code=200,
        )
