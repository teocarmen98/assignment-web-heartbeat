from django.contrib.sites import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse, Http404
from django.core.validators import URLValidator
from django.core.paginator import Paginator
from .serializers import UrlItemSerializer
from .models import UrlItem

import requests

class UrlAPIView(APIView):
    def get_object(self, pk):
        try:
            return UrlItem.objects.get(pk=pk)
        except UrlItem.DoesNotExist:
            raise Http404("Data Not Found")

    def get(self, request, pk=None, format=None):
        if pk:
            if self.get_object(pk):
                url = UrlItem.objects.get(pk=pk)
                serializer = UrlItemSerializer(url)
                return JsonResponse(serializer.data)
        else:
            urls_item_list = UrlItem.objects.all()
            paginator = Paginator(urls_item_list, request.GET.get('limit'))
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            serializer = UrlItemSerializer(page_obj, many=True)
            return JsonResponse({ 'data': serializer.data, 'total': UrlItem.objects.count()}, safe=False, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = JSONParser().parse(request)

        check_url_format_result = self.check_url_format(data['url'])

        if check_url_format_result:
            check_status_result = self.check_status(data['url'])
            data['status'] = check_status_result

            serializer = UrlItemSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            if serializer.errors['url'][0].code == 'unique':
                return JsonResponse({'error': 'URL Exist'}, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'error': 'Invalid URL'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):

        if self.get_object(pk):
            new_data= request.data

            check_url_format_result = self.check_url_format(new_data['url'])

            if check_url_format_result:
                check_status_result = self.check_status(new_data['url'])
                new_data['status'] = check_status_result

                serializer = UrlItemSerializer(self.get_object(pk), data=new_data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data)
                if serializer.errors['url'][0].code == 'unique':
                    return JsonResponse({'error': 'URL Exist'}, status=status.HTTP_400_BAD_REQUEST)
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse({'error': 'Invalid URL'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        self.get_object(pk).delete()
        return HttpResponse(status=204)

    # check url status
    def check_status(self, url):
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            return False

    # validate url format
    def check_url_format(self, url):
        validate_url = URLValidator()

        try:
            validate_url(url)
            return True
        except Exception as e:
            return False

    def update_status(self, data):
        url = UrlItem.objects.get(pk=data['id'])
        result = self.check_status(data['url'])
        if result != data['status']:
            new_data = {
                'url': data['url'],
                'status' : result
            }
            serializer = UrlItemSerializer(url, data=new_data)
            if serializer.is_valid():
                serializer.save()

    # refresh every 2s
    def refresh_data(self):
        urls_item_list = UrlItem.objects.all()
        serializer = UrlItemSerializer(urls_item_list, many=True)
        for item in serializer.data:
            self.update_status(item)