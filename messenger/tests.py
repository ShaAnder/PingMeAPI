import unittest
import json
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from pingme_api.asgi import application
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumerTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Clean up any existing test users first.
        await database_sync_to_async(User.objects.filter(username="user1").delete)()
        await database_sync_to_async(User.objects.filter(username="user2").delete)()

        # Create two test users asynchronously.
        self.user1 = await database_sync_to_async(User.objects.create_user)(
            username="user1", password="testpass"
        )
        self.user2 = await database_sync_to_async(User.objects.create_user)(
            username="user2", password="testpass"
        )

        # Set up two WebSocket communicators with proper URLs
        # For user1, the URL includes user2's ID (the user they are chatting with).
        self.communicator1 = WebsocketCommunicator(
            application, f"/ws/messenger/{self.user2.id}/"
        )
        self.communicator1.scope["user"] = self.user1  # simulate authentication

        # For user2, the URL includes user1's ID.
        self.communicator2 = WebsocketCommunicator(
            application, f"/ws/messenger/{self.user1.id}/"
        )
        self.communicator2.scope["user"] = self.user2

        # Connect both communicators.
        connected1, _ = await self.communicator1.connect()
        connected2, _ = await self.communicator2.connect()
        self.assertTrue(connected1, "User1 failed to connect")
        self.assertTrue(connected2, "User2 failed to connect")

    async def asyncTearDown(self):
        # Disconnect communicators.
        await self.communicator1.disconnect()
        await self.communicator2.disconnect()

    async def test_chat_message_exchange(self):
        """
        Test that a message sent by user1 is received by user2 and vice versa.
        """
        # User1 sends a message.
        message_from_user1 = "Hello from user1"
        await self.communicator1.send_json_to({"message": message_from_user1})

        # Verify that user2 receives the message.
        response = await self.communicator2.receive_json_from(timeout=1)
        self.assertEqual(
            response, {"message": message_from_user1},
            "User2 did not receive the message from user1"
        )

        # Now, user2 sends a reply.
        message_from_user2 = "Reply from user2"
        await self.communicator2.send_json_to({"message": message_from_user2})

        # Verify that user1 receives the reply.
        response = await self.communicator1.receive_json_from(timeout=1)
        self.assertEqual(
            response, {"message": message_from_user2},
            "User1 did not receive the reply from user2"
        )

if __name__ == "__main__":
    unittest.main()
