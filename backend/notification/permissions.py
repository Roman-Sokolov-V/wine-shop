# from django.contrib.auth import get_user_model
# from rest_framework import permissions
#
# User = get_user_model()
#
#
# class IsOwnerOrAdmin(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         user = request.user
#         if not user or not user.is_authenticated:
#             return False
#         if user.is_staff:
#             return True
#         return obj.email == user.email
