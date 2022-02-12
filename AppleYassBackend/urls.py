from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from rest_framework_simplejwt import views as jwt_views
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("user.urls")),
    path("category/", include("category.urls")),
    path("config/", include("setting.urls")),
    path("comments/", include("comment.urls")),
    path("statistics/", include("panelstatistics.urls")),
    path("transaction/", include("transaction.urls")),
    path("", include("product.urls")),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




