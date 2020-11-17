from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Profile

USER = get_user_model()


class UserRegisterEmailPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=68, write_only=True)
    confirm_password = serializers.CharField(max_length=68, write_only=True)
    email = serializers.EmailField()

    @staticmethod
    def user_exists(**kwargs):
        if 'email' in kwargs:
            try:
                if USER.objects.get(email=kwargs['email']):
                    raise serializers.ValidationError('User with email already '
                                                      'exists')
            except USER.DoesNotExist:
                pass

        elif 'username' in kwargs:
            try:
                if USER.objects.get(username=kwargs['username']):
                    raise serializers.ValidationError('User with username '
                                                      'already exists')
            except USER.DoesNotExist:
                pass

    def validate(self, attrs):
        password = attrs['password']
        confirm_password = attrs['confirm_password']
        if not attrs['email']:
            raise serializers.ValidationError('Email is required')
        self.user_exists(email=attrs['email'])
        if not attrs['username']:
            raise serializers.ValidationError('Username is required')
        self.user_exists(username=attrs['username'])
        if confirm_password != password:
            raise serializers.ValidationError('Passwords do not match!')
        attrs.pop('confirm_password')
        return attrs

    def save(self):
        # print(self.validated_data)
        password = self.validated_data.pop('password')
        print('v-data', self.validated_data)

        user = USER.objects.create(**self.validated_data)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user


class NameDOBSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField()

    @staticmethod
    def validate_date_of_birth(value):
        if not value:
            raise serializers.ValidationError('Date of birth is required!')

        if value > timezone.now().date():
            raise serializers.ValidationError('Are you really from future?')
        print('checking past validity')
        # check if value of the DOB is greater than 120 years
        if value < (timezone.now() - timezone.timedelta(days=(365 *
                                                              120))).date():
            raise serializers.ValidationError('Invalid Date')
        return value

    @staticmethod
    def validate_first_name(value):
        if not value:
            raise serializers.ValidationError('FirstName is required!')
        return value

    @staticmethod
    def validate_last_name(value):
        if not value:
            raise serializers.ValidationError('LastName is required!')
        return value

    def create(self, validated_data, user=None):
        if not user:
            raise serializers.ValidationError(
                    'User is required in multi-step validation form')
        try:
            prf = Profile.objects.get(user_id=user.id)
            raise serializers.ValidationError('You have already updated the '
                                              'data!!')
        except Profile.DoesNotExist:
            pass

        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        user_profile = Profile()
        user_profile.date_of_birth = validated_data['date_of_birth']
        user_profile.user = user
        user_profile.save()
        self.instance = user
        return self.instance

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.profile.date_of_birth = validated_data.get(
                'date_of_birth',
                instance.profile.date_of_birth
        )
        instance.save()
        instance.profile.save()
        return self.instance

    def save(self, email=None, **kwargs):
        if not email:
            assert 'instance' not in kwargs, (
                "You must provide an instance to update an item!"
            )

            if not kwargs['instance']:
                raise serializers.ValidationError(
                        'You must provide an instance to update an item!'
                )
            if kwargs['instance']:
                self.instance = self.update(instance=kwargs['instance'],
                                            validated_data=self.validated_data)

        elif email is not None:
            user = USER.objects.get(email=email)
            self.instance = self.create(self.validated_data, user=user)

        return self.instance
