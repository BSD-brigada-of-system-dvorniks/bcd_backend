from django.urls import path

from .views import RegisterView, LoginView, \
                   LogoutView, CurrentUserView


appname = 'accounts'
urlpatterns = [
    path('register/', RegisterView.as_view(),    name = 'register'),
    path('login/',    LoginView.as_view(),       name = 'login'),
    path('logout/',   LogoutView.as_view(),      name = 'logout'),
    path('profile/',  CurrentUserView.as_view(), name = 'current_user'),
]
