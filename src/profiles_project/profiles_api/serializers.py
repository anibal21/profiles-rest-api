from rest_framework import serializers
from . import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for our  user profile objects. """

    class Meta:
        model = models.UserProfile
        fields = ('id','name','lastname', 'email', 'password','country','phone','url_image')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        """Create and return a new user"""

        user = models.UserProfile(
            email = validated_data['email'],
            name = validated_data['name'],
            lastname = validated_data['lastname'],
            country = validated_data['country'],
            phone = validated_data['phone'],
            url_image = validated_data['url_image']

        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """A serializer for profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only':True}}

class UserProcessHistorySerializer(serializers.ModelSerializer):
    """ A serializer for load process made for user"""

    class Meta:
        model =models.UserProcessHistory
        fields = ('user_profile','description','last_mod','remaining_storage','status')

class UploadImageSerializer(serializers.ModelSerializer):
    """A serializer for upload images"""

    class Meta:
        model = models.Image
        fields = ('id','detail','image')

class UploadFileSerializer(serializers.ModelSerializer):
    """A serializer for upload files"""

    class Meta:
        model = models.AnyFile
        fields = ('id','detail','anyfile')

class MultiUploadSerializer(serializers.ModelSerializer):
    """A serializer for upload multiple files for an user"""

    class Meta:
        model = models.Proof
        fields = ('id','detail','anyfile')
