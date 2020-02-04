from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenRefreshSlidingView,
    TokenVerifyView
)
from .views import (
    TokenObtainPairView,
    TokenObtainSlidingView,
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyView,
    GroupListCreateView,
    GroupRetrieveUpdateDestroyAPIView,
    GroupPermissionListAPIView
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/sliding/', TokenObtainSlidingView.as_view(), name='token_sliding'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/refresh/sliding/', TokenRefreshSlidingView.as_view(), name='token_refresh_sliding'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('users/', UserListCreateAPIView.as_view(), name='list_create_users'),
    path('users/<str:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='retrieve_update_delete_user'),
    path('groups/', GroupListCreateView.as_view(), name='group_list_create'),
    path('groups/<str:pk>/', GroupRetrieveUpdateDestroyAPIView.as_view(), name='group_retrieve_update_destroy'),
    path('groups/<str:pk>/permissions/', GroupPermissionListAPIView.as_view(), name='group_permissions_list')
]
