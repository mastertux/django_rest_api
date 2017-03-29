from rest_framework import serializers
from custom_auth.models import User,Address,Profile
from rest_framework_jwt.settings import api_settings

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('street', 'number', 'district', 'city', 'state', 'country')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('token')

class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True)
    profile = ProfileSerializer(required=False)
    class Meta:
        model = User
        fields = ('first_name', 'password', 'email','profile','address')

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        user = User.objects.create_user(**validated_data)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        profile = { 'token': token, 'user': user }
        profile = Profile.objects.create(**profile)
        user.profile = profile
        user.save()
        for address in address_data:
            Address.objects.create(user=user, **address)
        return user


