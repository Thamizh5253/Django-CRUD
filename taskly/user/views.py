from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
import requests
import json





User = get_user_model()

# ✅ User Login API
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow non-authenticated users to access this
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'message': 'Login successful'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

# ✅ User Logout API
@api_view(['POST'])
def logout_user(request):
    if request.auth:
        request.auth.delete()  # Delete the token
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    
    return Response({'error': 'No active session'}, status=status.HTTP_400_BAD_REQUEST)

# ✅ User Registration API
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    token = Token.objects.create(user=user)  # Generate authentication token
    return Response({'token': token.key, 'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)



# @api_view(['POST'])
@csrf_exempt
def google_oauth_login(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            access_token = data.get('access_token')

            if not access_token:
                return JsonResponse({'error': 'Access token is required'}, status=400)

            # Verify the Google access token
            google_response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={access_token}')
            if google_response.status_code != 200:
                return JsonResponse({'error': 'Invalid Google token'}, status=400)

            google_data = google_response.json()
            print('Google Data:', google_data)  # Debugging

            # Check if the token is valid and issued to your app
            if google_data['aud'] != '732027334498-inlorb6888ejmq8cd53i6nqq4vi61jil.apps.googleusercontent.com':
                return JsonResponse({'error': 'Invalid token audience'}, status=400)

            # Extract user information from Google data
            user_email = google_data['email']
            first_name = google_data.get('given_name', '')
            last_name = google_data.get('family_name', '')

            # Check if the user already exists in the database
            try:
                user = User.objects.get(email=user_email)
                print('User exists:', user)  # Debugging
            except User.DoesNotExist:
                # Create a new user if they don't exist
                username = user_email.split('@')[0]  # Use email prefix as username
                user = User.objects.create_user(
                    username=username,
                    email=user_email,
                    first_name=first_name,
                    last_name=last_name,
                    password=None  # No password for OAuth users
                )
                print('New user created:', user)  # Debugging

            # Generate or get the token for the user
            token, _ = Token.objects.get_or_create(user=user)

            # Return the token and user information
            return JsonResponse({
                'status': 'success',
                'token': token.key,
                'email': user_email,
                'username': user.username,
                'message': 'Google login successful'
            })

        except Exception as e:
            print('Error:', e)  # Debugging
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)