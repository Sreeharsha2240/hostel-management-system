from django.utils.cache import add_never_cache_headers


class PrivatePageMiddleware:
    """Keep authenticated pages out of browser and shared proxy caches."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        authenticated = request.user.is_authenticated
        response = self.get_response(request)
        if authenticated or request.user.is_authenticated:
            add_never_cache_headers(response)
        return response
