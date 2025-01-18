import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.db.models import Q
import logging
from django.http import JsonResponse
from channels.db import database_sync_to_async

# Set up logging
logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(f"New WebSocket connection: {self.channel_name}")
        self.user = self.scope['user']
        self.receiver_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f"chat_{self.user.id}_{self.receiver_id}"

        # Log connection details
        logger.info(f"User {self.user.username} connecting to chat with receiver {self.receiver_id}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the connection
        await self.accept()


    async def disconnect(self, close_code):
        # Log disconnect
        logger.info(f"User {self.user.username} disconnected from chat with receiver {self.receiver_id}")

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            logger.warning("Invalid JSON received.")
            return

        message_type = data.get('type')
        sender = self.user

        if message_type == 'chat_message':
            # Handle sending a chat message
            message = data.get('message')
            receiver_id = data.get('receiver')

            # Log received data
            logger.info(f"Received message: {message} from sender: {sender.username} to receiver ID: {receiver_id}")


            # Validate input
            if not message or not receiver_id:
                logger.warning("Invalid data received: Missing 'message' or 'receiver'.")
                return

            # Get the receiver
            receiver = await self.get_receiver(receiver_id)
            if receiver is None:
                logger.warning(f"Receiver with ID {receiver_id} not found.")
                return  # Exit early if the receiver is invalid

            # Save the message to the database
            try:
                await self.save_message(sender, receiver, message)
                logger.info("Message saved successfully.")
            except Exception as e:
                logger.error(f"Failed to save message: {str(e)}")
                return

            # Send the message to WebSocket group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'sender': sender.username,
                    'message': message
                }
            )

        elif message_type == 'load_previous_messages':
            # Handle loading previous messages
            receiver_id = data.get('receiver')

            if not receiver_id:
                logger.warning("Missing 'receiver' for loading previous messages.")
                return

            try:
                # Fetch messages from the database
                previous_messages = await self.get_previous_messages(receiver_id)
                # Send the messages back to the frontend
                await self.send(text_data=json.dumps({
                    'type': 'previous_messages',
                    'messages': [
                        {
                            'sender': message['sender__username'],
                            'content': message['content']
                        } for message in previous_messages
                    ]
                }))
            except Exception as e:
                logger.error(f"Failed to load previous messages: {str(e)}")

        else:
            logger.warning(f"Unknown message type: {message_type}")



    @database_sync_to_async
    def save_message(self, sender, receiver_id, content):
        from django.contrib.auth.models import User  # Import User model here
        from . models import Message  # Import Message model here
        try:
            receiver = database_sync_to_async(User.objects.get)(id=receiver_id) # Convert receiver_id to integer
            # print(sender, receiver_id, content)
            Message.objects.create(sender=sender, receiver=receiver_id, content=content)
        except User.DoesNotExist:
            logger.warning(f"User with ID {receiver_id} not found.")
            return None
        except ValueError:
            logger.error(f"Invalid receiver ID: {receiver_id}.  Must be an integer.")
            return None
        except Exception as e:
            logger.error(f"Error saving message: {e}", exc_info=True)
            return None

    async def chat_message(self, event):
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'sender': event['sender'],
            'message': event['message']
        }))

    @database_sync_to_async
    def get_receiver(self, receiver_id):
        from django.contrib.auth.models import User  # Moved import here
        try:
            return User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            # Log receiver not found
            logger.warning(f"User with ID {receiver_id} does not exist.")
            return None
    
    async def get_previous_messages(self, receiver_id):
        from .models import Message  # Import Message model here
        try:
            messages = await database_sync_to_async(Message.objects.filter)(
                Q(sender=self.user, receiver_id=receiver_id) |
                Q(sender_id=receiver_id, receiver=self.user)
            )
            messages = await database_sync_to_async(messages.order_by)('timestamp')
            messages = await database_sync_to_async(messages.values)('sender__username', 'content')
            return await database_sync_to_async(list)(messages)
        except Exception as e:
            logger.error(f"Database error in get_previous_messages: {e}")
            return []
        
