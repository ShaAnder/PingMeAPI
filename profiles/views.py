from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from django.http import Http404
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from pingme_api.permissions import IsOwnerOrReadOnly


class ProfileList(ListAPIView):
    """
    List all profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class ProfileDetail(RetrieveUpdateAPIView):
    """
    Retrieve or update a profile.
    Only the owner can update.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
