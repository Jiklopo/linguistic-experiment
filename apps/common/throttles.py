from rest_framework import throttling


class OnePerSecondThrottle(throttling.UserRateThrottle):
    rate = '1/sec'

    def get_cache_key(self, request, view):
        api_view_name = view.__class__.__name__
        cache_key = super().get_cache_key(request, view)
        return f'{api_view_name}:{cache_key}'
