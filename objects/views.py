from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Object
from .serializers import ObjectSerializer
from accounts.utils import get_user_from_token


class ObjectListView(APIView):
    def get(self, request):
        objects = Object.objects.all()
        serializer = ObjectSerializer(objects, many=True)
        
        return Response(serializer.data)


class ObjectCreateView(APIView):
    def post(self, request):
        user = get_user_from_token(request)
        serializer = ObjectSerializer(data = request.data)
        
        if serializer.is_valid():
            obj = Object(author = user, **serializer.validated_data)
            obj.save()
            
            return Response(ObjectSerializer(obj).data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class ObjectDetailView(APIView):
    def get(self, request, id):
        obj = Object.objects(id = id).first()
        
        if not obj:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = ObjectSerializer(obj)
        
        return Response(serializer.data)


class ObjectUpdateView(APIView):
    def put(self, request, id):
        user = get_user_from_token(request)
        obj = Object.objects(id = id, author = user).first()
        
        if not obj:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        serializer = ObjectSerializer(obj, data = request.data, partial = True)
        
        if serializer.is_valid():
            for attr, value in serializer.validated_data.items():
                setattr(obj, attr, value)
            obj.save()
            
            return Response(ObjectSerializer(obj).data)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class ObjectDeleteView(APIView):
    def delete(self, request, id):
        user = get_user_from_token(request) 
        obj = Object.objects(id = id, author = user).first()
        
        if not obj:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        obj.delete()
        
        return Response(status = status.HTTP_204_NO_CONTENT)
