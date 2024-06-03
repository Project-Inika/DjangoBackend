from django.shortcuts import render
from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class StartOutfitsView(APIView):

    def post(self, request):
        try:
            # Extract message and uid from the request body
            message = request.data.get('message')
            uid = request.data.get('uid')
            print("Entered chat")

            # Make API call
            response = requests.post(
                "https://cheaply-shining-pup.ngrok-free.app/cbot",
                json={'message': message, 'uid': uid}
            )
            
            # Check if the API call was successful
            if response.status_code != 200:
                return Response({'error': 'Error calling API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Process the response data
            text = response.text
            uri_list, fit = text.split('@')
            responseObject = {'fit': fit, 'uri_list': uri_list, 'text': text}

            return Response(responseObject, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            print(f"Error calling API: {e}")
            return Response({'error': 'Error calling API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return Response({'error': f'An unexpected error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class EditOutfitsView(APIView):

    def post(self, request):
        try:
            # Extract message, uid, and newest_outfit from the request body
            message = request.data.get('message')
            uid = request.data.get('uid')
            newest_outfit = request.data.get('newest_outfit')

            # Make API call
            response = requests.post(
                "https://cheaply-shining-pup.ngrok-free.app/edit",
                json={'message': message, 'outfit': newest_outfit, 'uid': uid}
            )
            
            # Check if the API call was successful
            if response.status_code != 200:
                return Response({'error': 'Error calling API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Process the response data
            text = response.text
            uri_list, fit = text.split('@')
            responseObject = {'fit': fit, 'uri_list': uri_list, 'text': text}

            return Response(responseObject, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            print(f"Error in /editOutfits: {e}")
            return Response({'error': 'Error calling API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return Response({'error': f'An unexpected error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)