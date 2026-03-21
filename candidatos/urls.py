from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("importar/", views.importar_excel, name="importar_excel"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("", views.login_view, name="login"),
    path("limpar-candidatos/", views.limpar_candidatos, name="limpar_candidatos"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)