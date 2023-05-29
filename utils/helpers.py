from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from datetime import timedelta

def custom_cache_decorator(function):
    def wrapper(*args, **kwargs):
        if settings.DEBUG:
            return function(*args, **kwargs)
        else:
            return cache_page(timedelta(hours=1).total_seconds())(
                vary_on_headers("Authorization")(function)
            )(*args, **kwargs)
    return wrapper