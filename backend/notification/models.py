# from django.contrib.auth import get_user_model
# from django.db import models
#
#
# User = get_user_model()
#
#
# class Mailing(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#
#     def __str__(self):
#         return self.title
#
#
# class Subscription(models.Model):
#     mailing = models.ForeignKey(
#         Mailing, on_delete=models.CASCADE, related_name="subscriptions"
#     )
#     email = models.EmailField(blank=True, null=True)
#
#     class Meta:
#         unique_together = ("email", "mailing")
