from django.shortcuts import render
from rest_framework import generics, viewsets
from collection.serializers import CollectionSerializer, BookmarkSerializer
from collection.models import Collection, Bookmark


class BookmarkAPIView(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    
    
class CollectionAPIView(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


