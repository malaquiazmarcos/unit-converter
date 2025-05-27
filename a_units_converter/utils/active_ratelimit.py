from django.http import JsonResponse

def active_ratelimit(func):
    def wrapper(request, *args, **kwargs):
        if getattr(request, 'limited', False):
            return JsonResponse(
                {'error': 'Limit reached. Maximum 15 requests per minute.'},
                status=429
            )
        return func(request, *args, **kwargs)
    return wrapper