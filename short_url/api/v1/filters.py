from datetime import datetime, timedelta

from rest_framework.exceptions import ValidationError


def build_filter(key, query_params, filters):
    now = datetime.now().date()
    if key in query_params.keys() and query_params[key] != '':
        try:
            q = query_params[key]

            if q == 'today':
                filters.update({'created__gte': '{0} 00:00:00'.format(now.strftime('%Y-%m-%d'))})
                filters.update({'created__lte': '{0} 23:59:59'.format(now.strftime('%Y-%m-%d'))})
            elif q == 'this_week':
                last_week = now - timedelta(days=7)
                filters.update({'created__gte': '{0} 00:00:00'.format(last_week.strftime('%Y-%m-%d'))})
                filters.update({'created__lte': '{0} 23:59:59'.format(now.strftime('%Y-%m-%d'))})
            elif q == 'this_month':
                this_month = now - timedelta(days=30)
                filters.update({'created__gte': '{0} 00:00:00'.format(this_month.strftime('%Y-%m-%d'))})
                filters.update({'created__lte': '{0} 23:59:59'.format(now.strftime('%Y-%m-%d'))})
            elif q == 'yesterday':
                yesterday = now - timedelta(days=1)
                filters.update({'created__gte': '{0} 00:00:00'.format(yesterday.strftime('%Y-%m-%d'))})
                filters.update({'created__lte': '{0} 23:59:59'.format(now.strftime('%Y-%m-%d'))})
            return filters
        except ValueError:
            raise ValidationError('تاریخ صحیح نیست.')


class FilterMixin:
    def get_filter_kwargs(self):
        filters = {}
        query_params = self.request.query_params
        build_filter('when', query_params, filters)

        return filters
