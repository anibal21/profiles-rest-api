from rest_framework import serializers
from . import models
import decimal


#To create directories
import os, shutil, errno
from django.conf import settings
import hashlib, base64

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for our  user profile objects. """

    class Meta:
        model = models.UserProfile
        fields = ('id','name','lastname', 'email', 'password','url_image','plan_id')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        """Create and return a new user"""
        #Creating a folder in static directory
        static_dir = settings.MEDIA_ROOT

        email_code = validated_data['email']

        hashed = hashlib.sha256(str(email_code).encode('utf-8')).hexdigest()

        dir_path = os.path.join(static_dir,hashed)
        if  not os.path.exists(dir_path):
            try:
                os.mkdir(dir_path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    #directory already exists
                    pass
                else:
                    print(e)

        user = models.UserProfile(
            email = validated_data['email'],
            name = validated_data['name'],
            lastname = validated_data['lastname'],
            url_image = validated_data['url_image'],
            plan_id = validated_data['plan_id'],
            url_docs = hashed
        )

        user.set_password(validated_data['password'])
        user.save()

        user_model = models.UserProfile.objects.get(email=validated_data['email'])
        plan_model = models.PlanType.objects.get(id=validated_data['plan_id'])

        plan = models.UserPlan(
            user = user_model,
            plan = plan_model
        )

        referral = models.Codes.objects.filter(email=email_code)
        if referral:
            referral[0].status = 2
            referral[0].save()

        plan.save()


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
        fields = ('user_profile','description','last_mod','filled_storage','filled_storage_doc','filled_storage_image','filled_storage_music','filled_storage_video','status')

class UploadImageSerializer(serializers.ModelSerializer):
    """A serializer for uploa_d,'images"""

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
        model = models.UserFile
        fields = ('id','email','filename','filesize','filetype','last_mod','status','detail','anyfile')

    def create(self, validated_data):
        """Create and return a new file"""

        user = models.UserProfile.objects.get(email = validated_data['email'])

        hashed = hashlib.sha256(str(user.email).encode('utf-8')).hexdigest()

        userfile = models.UserFile(
            user = user,
            email = validated_data['email'],
            filename = validated_data['filename'],
            filesize = validated_data['filesize'],
            filetype = validated_data['filetype'],
            status = validated_data['status'],
            detail = validated_data['detail'],
            anyfile = validated_data['anyfile'],
            url_docs = hashed
        )
        userfile.save()

        #print("gettype filetype")
        #print(type(validated_data['filetype'].id))
        #int
        #print("gettype filesize")
        #print(type(validated_data['filesize']))
        #string

        user_process_history = models.UserProcessHistory.objects.get(user_profile = user, status = 1)

        if validated_data['filetype'].id == 1:
            user_process_history.filled_storage_image = user_process_history.filled_storage_image + decimal.Decimal(validated_data['filesize'])
            user_process_history.filled_storage = user_process_history.filled_storage + decimal.Decimal(validated_data['filesize'])
        elif validated_data['filetype'].id == 2:
            user_process_history.filled_storage_video = user_process_history.filled_storage_image + decimal.Decimal(validated_data['filesize'])
            user_process_history.filled_storage = user_process_history.filled_storage + decimal.Decimal(validated_data['filesize'])
        elif validated_data['filetype'].id == 3:
            user_process_history.filled_storage_music = user_process_history.filled_storage_image + decimal.Decimal(validated_data['filesize'])
            user_process_history.filled_storage = user_process_history.filled_storage + decimal.Decimal(validated_data['filesize'])
        elif validated_data['filetype'].id == 4:
            user_process_history.filled_storage_doc = user_process_history.filled_storage_image + decimal.Decimal(validated_data['filesize'])
            user_process_history.filled_storage = user_process_history.filled_storage + decimal.Decimal(validated_data['filesize'])
        user_process_history.save()

        return userfile

class PlanSerializer(serializers.ModelSerializer):
    """A serializer for upload files"""

    class Meta:
        model = models.PlanType
        fields = ('id','name','price','storage','detail','status')

class UserPlanSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    plan_id = serializers.CharField(max_length=10)

class ListUserPlanSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=255)
    plan = serializers.CharField(max_length=255)

class GetUserPlanSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)

class DeleteFileSerializer(serializers.Serializer):
    filename = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)

class LoginCollectorSerializer(serializers.Serializer):
    rut = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=100)

class CollectorSerializer(serializers.Serializer):
    collector_rut = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=255)

class AddCodeSerializer(serializers.Serializer):
    collector_rut = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)

class ListCodesSerializer(serializers.Serializer):
    collector_rut = serializers.CharField(max_length=255)

class ListCodesByUserSerializer(serializers.Serializer):
    collector = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    given_date = serializers.CharField(max_length=255)
    status = serializers.IntegerField(default=1)

class RegisterCollectorSerializer(serializers.Serializer):
    collector_rut = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
