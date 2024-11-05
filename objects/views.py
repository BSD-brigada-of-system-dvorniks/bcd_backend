from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mongoengine import DoesNotExist

from .models import Object
from .serializers import ObjectSerializer


class ObjectListView(APIView):
    def get(self, request):
        objects = Object.objects.all()
        serializer = ObjectSerializer(objects, many=True)
        
        return Response(serializer.data)


class ObjectCreateView(APIView):
    def post(self, request):
        serializer = ObjectSerializer(data = request.data)
        
        if serializer.is_valid():
            obj = Object(**serializer.validated_data)
            obj.save()
            
            return Response(ObjectSerializer(obj).data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class ObjectDetailView(APIView):
    def get_object(self, id):
        try:
            return Object.objects.get(id = id)
        except DoesNotExist:
            return None

    def get(self, request, id):
        obj = self.get_object(id)
        
        if not obj:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = ObjectSerializer(obj)
        
        return Response(serializer.data)


class ObjectUpdateView(APIView):
    def get_object(self, id):
        try:
            return Object.objects.get(id = id)
        except DoesNotExist:
            return None

    def put(self, request, id):
        obj = self.get_object(id)
        
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
    def get_object(self, id):
        try:
            return Object.objects.get(id = id)
        except DoesNotExist:
            return None

    def delete(self, request, id):
        obj = self.get_object(id)
        
        if not obj:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        obj.delete()
        
        return Response(status = status.HTTP_204_NO_CONTENT)
