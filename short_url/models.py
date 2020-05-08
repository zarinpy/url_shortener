from django.contrib.auth.models import User
from django.db import models


class ShortUrl(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='user',
        related_name='urls',
        on_delete=models.CASCADE
    )
    base_url = models.URLField(verbose_name='url')
    target_url = models.CharField(verbose_name='target', max_length=200)
    created = models.DateTimeField(auto_now_add=True)


class Devices(models.Model):
    MOBILE = 'Mobile'
    PC = 'Pc'
    TABLET = 'Tablet'
    OTHER = 'Other'
    device_choices = [
        (MOBILE, 'Mobile'),
        (TABLET, 'Tablet'),
        (PC, 'Pc'),
        (OTHER, 'Other'),
    ]
    ip_address = models.GenericIPAddressField(verbose_name='ip address')
    url = models.ForeignKey(ShortUrl, verbose_name='url', related_name='devices', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    device = models.CharField(max_length=10, choices=device_choices)
    os = models.CharField(max_length=10)
    os_version = models.CharField(max_length=5)
    browser = models.CharField(max_length=100)
    browser_version = models.CharField(max_length=5)
