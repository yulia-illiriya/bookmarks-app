from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'bookmark', BookmarkAPIView)
router.register(r'collection', CollectionAPIView)

urlpatterns = [
     path('v1/', include(router.urls)),
]
