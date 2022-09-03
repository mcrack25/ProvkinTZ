from billsapp.urls import router as billsapp_router
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.registry.extend(billsapp_router.registry)


urlpatterns = [
    path('', RedirectView.as_view(url='/api')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
