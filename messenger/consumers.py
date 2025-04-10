import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    """
    This consumer handles real-time chat messages and manages WebSocket connections.
    It adds users to a unique group representing their conversation and sends messages
    via group messaging.
    """

    async def connect(self):
        """
        Connect the users to the websockets
        """
        # the authenticated user
        self.current_user = self.scope["user"]
        # the id of the user we're chatting with (from URL)
        self.other_user_id = self.scope["url_route"]["kwargs"]["other_user_id"]

        # Debugging: Check if other_user_id is None
        if self.other_user_id is None:
            print(f"Error: other_user_id not passed correctly for {self.current_user.id}")
            return await self.close()

        # Create a unique identifier for the conversation between the two users.
        sorted_ids = sorted([str(self.current_user.id), str(self.other_user_id)])
        self.room_group_name = f"chat_{sorted_ids[0]}_{sorted_ids[1]}"
        print(f"User {self.current_user.id} connected to room: {self.room_group_name}")

        # Add this channel to the conversation group.
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection.
        await self.accept()

    async def disconnect(self, close_code):
        """
        When the WebSocket disconnects, remove it from the conversation group.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """
        Handle incoming messages from the WebSocket.
        The message is broadcasted to the entire group (i.e., both users).
        """
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")

        # Broadcast the message to the conversation group.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",  # This tells Channels which method to invoke.
                "message": message, # The content of the message.
            }
        )

    async def chat_message(self, event):
        """
        Receives messages broadcast by the group and sends them to the WebSocket client.
        """
        message = event.get("message")
        # Send the message to the WebSocket client.
        await self.send(text_data=json.dumps({
            'message': message
        }))
