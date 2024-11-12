from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Object
from .serializers import ObjectSerializer, BasicObjectSerializer
from accounts.utils import get_user_from_token


class ObjectListView(APIView):
    def get(self, request):
        print("Request Headers:", request.headers)

        objects = Object.objects.fields(type = 1, level = 1,
                                        article__name = 1, article__published = 1)
        serializer = BasicObjectSerializer(objects, many = True)
        return Response(serializer.data)


class ObjectCreateView(APIView):
    def post(self, request):
        user = get_user_from_token(request)
        serializer = ObjectSerializer(data = request.data)
        
        if serializer.is_valid():
            article_data = serializer.validated_data.pop('article', None)
            article = Article(author = user, **article_data) if article_data else None
            obj = Object(article = article, **serializer.validated_data)
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
        obj = Object.objects(id = id, article__author = user).first()
        
        if not obj:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        serializer = ObjectSerializer(obj, data = request.data, partial = True)
        
        if serializer.is_valid():
            article_data = serializer.validated_data.pop('article', None)

            if article_data:
                for attr, value in article_data.items():
                    if attr != 'author':
                        setattr(obj.article, attr, value)
            
            for attr, value in serializer.validated_data.items():
                setattr(obj, attr, value)
            
            obj.save()
            return Response(ObjectSerializer(obj).data)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class ObjectDeleteView(APIView):
    def delete(self, request, id):
        user = get_user_from_token(request)
        obj = Object.objects(id = id, article__author = user).first()
        
        if not obj:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        obj.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
