from rest_framework import routers
from .views import BillViewSet, UploadViewSet


router = routers.DefaultRouter()
router.register('upload', UploadViewSet, basename="upload")
router.register('bills', BillViewSet, basename="bills")
