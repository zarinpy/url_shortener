import hashlib
from random import randint

from rest_framework import serializers

from short_url.models import ShortUrl, Devices


class ShortUrlCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortUrl
        exclude = ['created', 'target_url']
        read_only_fields = ['id']

    def validate(self, attrs):
        hash_object = hashlib.md5(attrs['base_url'].encode('utf-8'))
        attrs['target_url'] = attrs['base_url']
        attrs['base_url'] = "{0}{1}{2}".format(
            hash_object.hexdigest()[:5],
            self.context['request'].user.id,
            randint(1, 10)
        )

        return attrs


class DashboardUrlSeenSerializer(serializers.ModelSerializer):
    total_seen = serializers.SerializerMethodField()
    url_id = serializers.SerializerMethodField()

    class Meta:
        model = Devices
        fields = ['total_seen', 'url_id']

    @staticmethod
    def get_total_seen(obj):
        return obj['total_seen']

    @staticmethod
    def get_url_id(obj):
        return obj['url']


class DashboardByBrowserSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    browser = serializers.SerializerMethodField()

    class Meta:
        model = Devices
        fields = ['total', 'browser']

    @staticmethod
    def get_browser(obj):
        return obj['browser']

    @staticmethod
    def get_total(obj):
        return obj['total']


class DashboardByDeviceSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    device = serializers.SerializerMethodField()

    class Meta:
        model = Devices
        fields = ['total', 'device']

    @staticmethod
    def get_device(obj):
        return obj['device']

    @staticmethod
    def get_total(obj):
        return obj['total']


class DashboardByUserSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    ip = serializers.SerializerMethodField()

    class Meta:
        model = Devices
        fields = ['total', 'ip']

    @staticmethod
    def get_ip(obj):
        return obj['ip_address']

    @staticmethod
    def get_total(obj):
        return obj['total']


class DashboardByUserDeviceSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    device = serializers.SerializerMethodField()
    ip = serializers.SerializerMethodField()

    class Meta:
        model = Devices
        fields = ['total', 'ip', 'device']

    @staticmethod
    def get_ip(obj):
        return obj['ip_address']

    @staticmethod
    def get_device(obj):
        return obj['device']

    @staticmethod
    def get_total(obj):
        return obj['total']


class DashboardByUserBrowserSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    browser = serializers.SerializerMethodField()
    ip = serializers.SerializerMethodField()

    class Meta:
        model = Devices
        fields = ['total', 'ip', 'browser']

    @staticmethod
    def get_ip(obj):
        return obj['ip_address']

    @staticmethod
    def get_browser(obj):
        return obj['browser']

    @staticmethod
    def get_total(obj):
        return obj['total']
