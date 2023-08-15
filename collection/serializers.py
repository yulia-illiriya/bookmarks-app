from rest_framework import serializers
from collection.models import Bookmark, Collection, BookmarkInCollection
from user_profile.serializers import UserSerializer
from collection.utils import extract_page_info


class BookmarkSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    collection = serializers.StringRelatedField(many=True, source='bookmarkincollection_set.collection', required=False)
    page_header = serializers.ReadOnlyField()
    page_description = serializers.ReadOnlyField()
    type_of_link = serializers.ReadOnlyField()
    preview = serializers.ReadOnlyField()
    
    def create(self, validated_data):
        
        """
        Юзер может передать только линк, остальное либо заполнится,
        либо останется пустым, потому что нет разметки.        
        
        """
        user = self.context['request'].user
        page_link = validated_data.get('page_link')
        data = extract_page_info(page_link)

        page_header = data.get('title', '')
        page_description = data.get('description', '')
        type_of_link = data.get('type', 'website')
        preview = data.get('image', '')
        
        choice = ['book', 'article', 'music', 'video']
        type_of_link = 'website' if type_of_link not in choice else type_of_link
        
        bookmark = Bookmark.objects.create(
            page_header=page_header,
            page_description=page_description,
            type_of_link=type_of_link,
            preview=preview,
            page_link=page_link,
            user=user
            )
        
        return bookmark
        
    def update(self, instance, validated_data):
        
        """Обновить можно только связь с коллекциями"""
        
        collection_data = validated_data.pop('collection', [])
        collections_to_add = Collection.objects.filter(collection_title__in=collection_data)
        collections_to_remove = instance.collection.exclude(collection_title__in=collection_data)
        
        for collection in collections_to_remove:
            BookmarkInCollection.objects.filter(bookmark=instance, collection=collection).delete()

        for collection in collections_to_add:
            BookmarkInCollection.objects.get_or_create(bookmark=instance, collection=collection)
            
            instance.save()        
        
    class Meta:
        model = Bookmark
        fields = [
            'page_header', 
            'page_description', 
            'page_link', 
            'type_of_link', 
            'preview', 
            'created_at', 
            'updated_at', 
            'user',
            'collection'
            ]
        
        
class CollectionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    bookmark = serializers.StringRelatedField(many=True, source="bookmarkincollection_set.bookmark", required=False)
    
    def create(self, validated_data):
        bookmark_data = validated_data.pop('bookmark', [])  # Получаем данные о закладках из validated_data        
        user = self.context['request'].user
        collection = Collection.objects.create(**validated_data, user=user)
        
        if bookmark_data:
            for bookmark in bookmark_data:
                BookmarkInCollection.objects.create(collection=collection, bookmark=bookmark)
                
        collection.bookmark.set(bookmark_data)

        return collection
    
    def update(self, instance, validated_data):
        bookmark_data = validated_data.pop('bookmark', [])
                
        if bookmark_data:
            for bookmark in bookmark_data:
                BookmarkInCollection.objects.create(collection=instance, bookmark=bookmark)
                
        instance.bookmark.set(bookmark_data)
                
        instance.save()
        
        return instance
    
    class Meta:
        model = Collection
        fields = ['collection_title', 'collection_description', 'created_at', 'updated_at', 'user', 'bookmark']
        
        

    