from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['full_name'] = f"{user.first_name} {user.last_name}"
        token['profile_image'] = user.profile_image.url if user.profile_image else None
        token['phone_number'] = user.phone_number
        return token
