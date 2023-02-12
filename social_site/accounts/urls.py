from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUp, LoginView, ActivateAccount


app_name = 'accounts'
urlpatterns = [
    path('sign_up/', SignUp.as_view(), name='sign-up'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]