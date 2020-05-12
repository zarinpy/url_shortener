from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from short_url.models import ShortUrl, Devices
from .filters import FilterMixin
from .serializer import ShortUrlCreateSerializer, DashboardUrlSeenSerializer, DashboardByBrowserSerializer, \
    DashboardByDeviceSerializer, DashboardByUserSerializer, DashboardByUserBrowserSerializer, \
    DashboardByUserDeviceSerializer


class ShortUrlViewSet(GenericViewSet, CreateModelMixin):
    queryset = ShortUrl.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ShortUrlCreateSerializer

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        shorted_url = serializer.data['base_url']
        data = {
            'shorted_url': '{0}/r/{1}/'.format(request.META['HTTP_HOST'], shorted_url)
        }
        return Response(data, status=status.HTTP_201_CREATED)


class RedirectToView(APIView):

    def get(self, request, input_url):
        target = get_object_or_404(ShortUrl, base_url=input_url)
        target_url = target.target_url
        if target_url[:4] != 'http':
            target_url = 'http://' + target_url

        device_values = {
            'ip_address': request.META['REMOTE_ADDR'],
            'url': target,
            'device': '',
            'browser': request.user_agent.browser.family,
            'browser_version': request.user_agent.browser.version_string,
            'os': request.user_agent.os.family,
            'os_version': request.user_agent.os.version_string,
        }

        if self.request.user_agent.is_mobile:
            device_values['device'] = Devices.MOBILE
        elif self.request.user_agent.is_tablet:
            device_values['device'] = Devices.TABLET
        elif self.request.user_agent.is_pc:
            device_values['device'] = Devices.PC
        else:
            device_values['device'] = Devices.OTHER

        Devices.objects.create(**device_values)
        return redirect(target_url)


class DashboardViewSet(GenericViewSet, FilterMixin):
    queryset = Devices.objects.none()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'url_seen':
            return DashboardUrlSeenSerializer
        elif self.action == 'by_browser':
            return DashboardByBrowserSerializer
        elif self.action == 'by_device':
            return DashboardByDeviceSerializer
        elif self.action == 'by_user':
            return DashboardByUserSerializer
        elif self.action == 'by_user_device':
            return DashboardByUserDeviceSerializer
        elif self.action == 'by_user_browser':
            return DashboardByUserBrowserSerializer

    def paginate_and_response(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def url_seen(self, request, *args, **kwargs):
        queryset = Devices.objects.select_related('url').filter(url__user=request.user) \
            .filter(**self.get_filter_kwargs()).values('url').annotate(total_seen=Count('url'))

        return self.paginate_and_response(queryset)

    @action(methods=['get'], detail=True)
    def by_browser(self, request, pk=None, *args, **kwargs):
        queryset = Devices.objects.select_related('url').filter(url_id=pk, url__user=request.user) \
            .filter(**self.get_filter_kwargs()).values('browser').annotate(total=Count('browser'))

        return self.paginate_and_response(queryset)

    @action(methods=['get'], detail=True)
    def by_device(self, request, pk=None, *args, **kwargs):
        queryset = Devices.objects.select_related('url').filter(url_id=pk, url__user=request.user) \
            .filter(**self.get_filter_kwargs()).values('device').annotate(total=Count('device'))

        return self.paginate_and_response(queryset)

    @action(methods=['get'], detail=True)
    def by_user(self, request, pk=None, *args, **kwargs):

        queryset = Devices.objects.select_related('url').filter(url_id=pk, url__user=request.user) \
            .filter(**self.get_filter_kwargs()).values('ip_address').annotate(total=Count('ip_address'))

        return self.paginate_and_response(queryset)

    @action(methods=['get'], detail=True)
    def by_user_browser(self, request, pk=None, *args, **kwargs):
        queryset = Devices.objects.select_related('url').filter(url_id=pk, url__user=request.user) \
            .filter(**self.get_filter_kwargs()).values('ip_address', 'browser').annotate(total=Count('ip_address'))

        return self.paginate_and_response(queryset)

    @action(methods=['get'], detail=True)
    def by_user_device(self, request, pk=None, *args, **kwargs):
        queryset = Devices.objects.select_related('url').filter(url_id=pk, url__user=request.user) \
            .filter(**self.get_filter_kwargs()).values('ip_address', 'device').annotate(total=Count('ip_address'))

        return self.paginate_and_response(queryset)
