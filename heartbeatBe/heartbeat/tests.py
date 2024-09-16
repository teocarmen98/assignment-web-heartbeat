from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import UrlItem

class UrlApiTestCase(APITestCase):
    def setUp(self):
        self.data = UrlItem.objects.create(
            url="https://www.testing0.com"
        )
        self.data = UrlItem.objects.create(
            url="https://www.testing123.com"
        )
        self.data = UrlItem.objects.create(
            url="https://hahaha.com"
        )

    def test_view_url_list(self):
        data = {
            'limit' : '2',
            'page' : '2'
        }
        url = reverse('urls-list')
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_url_detail(self):
        url = reverse('urls-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_exist_view_url_detail(self):
        url = reverse('urls-detail', args=[1000])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_url(self):
        data = {
            'url' : 'http://www.apple.com/'
        }
        url = reverse('urls-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_wrong_format_url(self):
        data = {
            'url' : 'testing123'
        }
        url = reverse('urls-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_url(self):
        data = {
            'url' : 'https://happygolucky.com'
        }
        url = reverse('urls-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_duplicate_url(self):
        data = {
            'url' : 'https://www.testing0.com'
        }
        url = reverse('urls-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_url(self):
        data = {
            'url' : 'https://www.testing100.com'
        }

        url = reverse('urls-detail', kwargs={'pk':1})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wrong_format_url(self):
        data = {
            'url' : 'testing123'
        }
        url = reverse('urls-detail', kwargs={'pk':1})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_url(self):
        data = {
            'url' : 'https://happygolucky.com'
        }
        url = reverse('urls-detail', kwargs={'pk':1})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_duplicate_url(self):
        data = {
            'url' : 'https://www.testing123.com'
        }
        url = reverse('urls-detail', kwargs={'pk':1})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_url(self):
        url = reverse('urls-detail', kwargs={'pk':1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
