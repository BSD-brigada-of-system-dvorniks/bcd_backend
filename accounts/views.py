from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Token
from .serializers import UserSerializer, LoginSerializer
from .utils import get_user_from_token

from articles.models import Object
from articles.serializers import ObjectSerializer


class RegisterView(APIView):
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
        user = get_user_from_token(request)
        token = Token.objects(user = user).first()
        
        if token:
            token.delete()
            return Response({"message": "Successfully logged out"}, status = status.HTTP_200_OK)
        
        else:
            return Response({"error": "Token not found"}, status = status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    def get(self, request):
        user = get_user_from_token(request)

        serializer = UserSerializer(user)
        return Response(serializer.data, status = status.HTTP_200_OK)


class CurrentUserObjectsView(APIView):
    def get(self, request):
        user = get_user_from_token(request)

        objects = Object.objects(author = user)
        serializer = ObjectSerializer(objects, many = True)

        return Response({"objects": serializer.data}, status = status.HTTP_200_OK)
