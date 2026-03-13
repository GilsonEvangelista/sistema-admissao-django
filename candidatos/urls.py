from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from candidatos.views import dashboard
from candidatos.views import login_view

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('', login_view, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
