from rest_framework import serializers
from users.models import User, SpamMarkedHisory, Contact
from django.db import IntegrityError


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    mobile = serializers.CharField(required=True)


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'mobile', 'email', 'password')

    def create(self, validated_data):
        try:
            user = super(UserSerializer, self).create(validated_data)
        except IntegrityError:
            user = User.objects.get(mobile=validated_data['mobile'])
            if not user.is_registered:
                pass
            else:
                raise serializers.ValidationError({'mobile': 'this number already exist'})
        user.is_registered = True
        for key, val in validated_data.items():
            setattr(user, key, val)
        user.set_password(validated_data['password'])
        user.save()
        return user



class RerieveProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'mobile', 'email', 'mobile',)



class MarkNumberspamSerializer(serializers.Serializer):

    mobile = serializers.CharField(required=True)


    def validate_mobile(self, value):
        request = self.context['request']
        k = User.objects.filter(mobile=value).first()
        if not k:
            raise serializers.ValidationError('User Does Not Exist')

        if request.user.mobile == value:
            raise serializers.ValidationError('Cannot mark self spam')

        return value

    def to_representation(self, instance):
        return {
            'marked_by': instance.by.mobile,
            'marked_to': instance.to.mobile
        }


    def create(self, validated_data):
        request = self.context['request']
        mobile = validated_data['mobile']
        k = User.objects.filter(mobile=mobile).first()

        marked_spam, created = SpamMarkedHisory.objects.get_or_create(
            by=request.user,
            to=k
        )
        if created:
            k.spam_marked_count += 1
            k.save()
        return marked_spam


class SearchSerializer(serializers.ModelSerializer):
    spam_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('mobile', 'first_name', 'last_name', 'spam_count')


    def get_spam_count(self, obj):
        return SpamMarkedHisory.objects.filter(to__mobile=obj.mobile).count()


class AddContactSerializer(serializers.Serializer):
    contact = serializers.CharField()

    def to_representation(self, instance):
        return {
            'primary_contact': instance.primary_contact.mobile,
            'secondary_contact': instance.related_contact.mobile
        }

    def create(self, validate_data):
        request = self.context['request']
        mobile = validate_data['contact']
        secondary_contact, created = User.objects.get_or_create(mobile=mobile)
        user = request.user
        contact, created = Contact.objects.get_or_create(
            primary_contact=user, related_contact=secondary_contact
        )
        return contact
