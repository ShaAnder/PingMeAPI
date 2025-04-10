from rest_framework import serializers
from .models import Profile
from cloudinary.utils import cloudinary_url

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    image_url = serializers.ReadOnlyField(source='image.url')  # Read-only URL
    image = serializers.ImageField(write_only=True, required=False)  # Write-only upload

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'status_mode',
            'status_text', 'name', 'location',
            'content', 'image', 'image_url'
        ]

    def get_profile_image(self, obj):
        image = obj.user_profile.image
        # If image is a File/Image instance with a .url attribute, return that.
        if hasattr(image, 'url'):
            return image.url
        # Otherwise, assume it's already a URL or a string.
        return image
