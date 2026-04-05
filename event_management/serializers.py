from rest_framework import serializers

from event_management.models import Event



class EventRegistrationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    participant_id = serializers.IntegerField()


class OrganizerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

class EventSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ("id", "title", "description", "date", "location", "organizer")
