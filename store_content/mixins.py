from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden, Http404

class UserIsOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return HttpResponseForbidden("This product does not exist or you do not have permission to access it.")

        if instance.seller == request.user or request.user.groups.filter(name__in=['Admin', 'Moderators']).exists():
            return super().dispatch(request, *args, **kwargs)

        return PermissionDenied