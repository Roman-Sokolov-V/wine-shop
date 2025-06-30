from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from notification.models import Subscription, Mailing


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for subscription model
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True, many=False)

    class Meta:
        model = Subscription
        fields = ("mailing", "email", "token", "user")
        extra_kwargs = {"token": {"read_only": True}}
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=("mailing", "email"),
                message="This subscription already exists.",
            )
        ]


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ("id", "title", "content", "run_at")
