from django.contrib import admin
from django.urls import path
from api.views import ScrapeProductView, CustomTokenObtainPairView, RegisterView, LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path('scrape/', ScrapeProductView.as_view()),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
