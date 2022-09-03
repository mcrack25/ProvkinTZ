from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from billsapp.urls import router as billsapp_router

router = DefaultRouter()
router.registry.extend(billsapp_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
