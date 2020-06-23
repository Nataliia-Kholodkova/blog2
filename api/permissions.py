from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
      def has_object_permission(self, request, view, obj):
           #### can write custom code
           return obj.user == request.user