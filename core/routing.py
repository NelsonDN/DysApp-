from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/exercise/(?P<attempt_id>\w+)/$', consumers.ExerciseConsumer.as_asgi()),
]
