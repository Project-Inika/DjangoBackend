from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from rest_framework.parsers import MultiPartParser, FormParser

from .helpers import extract_substring, process_paths, remove_last_characters, process_text, process_text2, process_image

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class ApiConnectionView(APIView):
    
    def post(self, request):
        try:
            body = json.loads(request.body)
            uid = body.get('uid')

            # Make API call
            response = requests.post(
                "https://cheaply-shining-pup.ngrok-free.app/searchQuery",
                json={"message": "shirt", "uid": uid}
            )

            # Check if the request was successful
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Error calling API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.exceptions.RequestException as e:
            print(f"Error calling API: {e}")
            return Response({'error': 'Error calling API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except json.JSONDecodeError as e:
            return Response({'error': 'Invalid JSON in request body'}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class ImageResultsView(APIView):

    def get(self, request):
        try:
            # body = json.loads(request.body)
            results, class_search, uid = request.query_params.getlist('results'), request.query_params.get('classSearch'), request.query_params.get('uid')

            if isinstance(results, list) and results:
                final_paths = [f"data:image/jpeg;base64,{base64_image}" for base64_image in results]
            else:
                result = extract_substring(results)
                urls_array = result.split(",")
                updated_array = urls_array
                if class_search == '1':
                    updated_array = urls_array[:5]
                prefix = f"https://storage.googleapis.com/inika-webpage.appspot.com/{uid}"
                processed_paths = process_paths(updated_array, prefix, uid)
                final_paths = remove_last_characters(processed_paths, 1)
            
            return Response({'finalPaths': final_paths}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            print(f"Error calling API: {e}")
            return Response({'error': 'Error calling API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except json.JSONDecodeError as e:
            return Response({'error': 'Invalid JSON in request body'}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class TextSearchResultsView(APIView):

    def post(self, request):
        try:
            body = json.loads(request.body)
            message, uid = body.get('message'), body.get('uid')
            print(f"Received message: {message}, UID: {uid}")

            # Make API call
            response_class = requests.post("https://cheaply-shining-pup.ngrok-free.app/search", json={'message':message})
            print(f"API call response: {response_class.status_code}, {response_class.text}")

            if response_class.status_code != 200:
                return Response({'error': 'Error calling API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # parsing the response
            parsed_data = json.loads(response_class.json())
            print(parsed_data)
            class_input = parsed_data.get('class')
            input = parsed_data.get('var1')
            spell_checked = parsed_data.get('var2')

            # Determine the search type and process accordingly
            if class_input == 0:
                api_response = process_text(message, uid)
            else:
                api_response = process_text2(input, uid)
            
             # Constructing the response object
            response_object = {
                'searchClass': class_input,
                'modifiedWord': input,
                'spellCheck': spell_checked,
                'apiResponseB': api_response
            }

            return Response(response_object, status=status.HTTP_200_OK)
        
        except requests.exceptions.RequestException as e:
            print(f"Error calling API: {e}")
            return Response({'error': 'Error calling API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return Response({'error': 'Invalid JSON in request body'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@method_decorator(csrf_exempt, name='dispatch')
class ImageSearchView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            file = request.data.get('file')

            if not file:
                return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Process the image
            api_response = process_image(file)
            print(type(api_response['images']))

            # Constructing the response object
            response_object = {'apiResponseB': api_response['images']}
            return Response(response_object, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



        
