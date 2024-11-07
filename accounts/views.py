from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed

from .models import User, Token
from .serializers import UserSerializer, LoginSerializer


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()  # Calls create() in the serializer
            return Response({"message": "User registered successfully"}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = User.objects(username = username).first()
            if user and user.check_password(password):
                token = Token.objects(user = user).first()
                if not token:
                    token = Token.create_token(user = user)
                
                return Response({"token": token.key}, status = status.HTTP_200_OK)

            return Response({"error": "Invalid credentials"}, status = status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        auth_header = get_authorization_header(request).split()
        if len(auth_header) == 2:
            try:
                token_key = auth_header[1].decode()
                token = Token.objects(key = token_key).first()
                if token:
                    token.delete()
                    return Response({"message": "Successfully logged out"}, status = status.HTTP_200_OK)
            except Token.DoesNotExist:
                pass

        return Response({"error": "Invalid token"}, status = status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    def get(self, request):
        auth_header = get_authorization_header(request)
        if not auth_header:
            raise AuthenticationFailed('Authorization header is missing.')

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != b'token':
            raise AuthenticationFailed('Authorization token is invalid.')

        token_key = parts[1].decode()
        
        try:
            token = Token.objects.get(key = token_key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        user = token.user

        serializer = UserSerializer(user)
        return Response(serializer.data, status = status.HTTP_200_OK)
