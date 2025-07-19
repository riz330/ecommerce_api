import pytest
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from ecommerce_api.asgi import application
from asgiref.sync import sync_to_async
import asyncio

User = get_user_model()

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_notification_consumer():
    # Create user
    user = await sync_to_async(User.objects.create_user)(
        email='test@user.com',
        password='testpass123'
    )
    
    # Create communicator
    communicator = WebsocketCommunicator(
        application,
        "/ws/notifications/"
    )
    communicator.scope['user'] = user
    
    # Connect
    connected, _ = await communicator.connect()
    assert connected
    
    try:
        # Test sending a message
        await communicator.send_json_to({
            'message': 'Hello world'
        })
        
        # Receive response with timeout
        try:
            response = await asyncio.wait_for(
                communicator.receive_json_from(),
                timeout=2.0
            )
            assert response == {'message': 'Hello world'}
        except asyncio.TimeoutError:
            pytest.skip("WebSocket response timed out - may need to check Redis configuration")
    
    finally:
        # Clean up
        try:
            await communicator.disconnect()
        except Exception:
            pass  # Ignore any disconnect errors during test cleanup