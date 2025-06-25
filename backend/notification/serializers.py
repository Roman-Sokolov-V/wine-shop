# from rest_framework import serializers, status
# from rest_framework.exceptions import ValidationError
# from rest_framework.validators import UniqueTogetherValidator
#
# from notification.models import Subscription, Mailing
#
#
# class SubscriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subscription
#         fields = ("mailing", "email")
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Subscription.objects.all(),
#                 fields=("mailing", "email"),
#                 message="This subscription already exists.",
#             )
#         ]
#
#     def create(self, validated_data):
#         user = self.context["request"].user
#         if (
#             user.is_authenticated and not user.is_staff
#         ) and user.email != validated_data.get("email"):
#
#             raise ValidationError(
#                 detail="You can subscribe only on registered email.",
#                 code=status.HTTP_400_BAD_REQUEST,
#             )
#         else:
#             return super().create(validated_data)
#
#
# class MailingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Mailing
#         fields = ("title", "content")
