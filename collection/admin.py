from django.contrib import admin
from collection.models import Collection, Bookmark, BookmarkInCollection

admin.site.register(Collection)
admin.site.register(Bookmark)
admin.site.register(BookmarkInCollection)
