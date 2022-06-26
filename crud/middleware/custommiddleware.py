from django.utils.deprecation import MiddlewareMixin


class CustomHeaderMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.META['HTTP_CUSTOM_HEADER'] = "Hello From Ali =)"