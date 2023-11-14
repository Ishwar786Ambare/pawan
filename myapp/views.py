# Create your views here.
import json

from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import KeyValue

from django.core.cache import cache


class PingView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "pong"})


class AuthorizeView(View):
    def post(self, request, *args, **kwargs):
        secret_key = request.headers.get('Authorization')
        if secret_key == 'your_shared_secret':
            return JsonResponse({"message": "Authorized"})
        else:
            return HttpResponseForbidden("Forbidden")


@method_decorator(csrf_exempt, name='dispatch')
class SaveView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        key = data.get('key')
        value = data.get('value')

        # Cache the data
        cache.set(key, value)

        # Save to the database (optional)
        KeyValue.objects.create(key=key, value=value)

        return JsonResponse({"message": "Data saved successfully"})


class GetView(View):
    def get(self, request, *args, **kwargs):
        # Try to get the data from the cache
        data = cache.get('key_data')

        if data is None:
            # If not in cache, fetch from the database
            data = list(KeyValue.objects.values())

            # Cache the data for future requests
            cache.set('key_data', data)

        return JsonResponse(data, safe=False)


class DeleteView(View):
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        key = data.get('key')
        KeyValue.objects.filter(key=key).delete()
        return JsonResponse({"message": "Data deleted successfully"})
