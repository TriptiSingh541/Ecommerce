from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserProfileView ,CategoryViewSet, ProductViewSet,CreateOrderView,OrderItemViewSet,AddToCartView, PlaceOrderFromCartView, UpdateOrderStatusView,update_order_status

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('items', OrderItemViewSet, basename='order-items')
from .views import UpdateOrderStatusView



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('categories/',CategoryViewSet.as_view({'get': 'list'}),name='categories for product'),
    path('products/',ProductViewSet.as_view({'get': 'list'}),name='Product listing'),
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('cart_add/', AddToCartView.as_view(),name="cart adding"),
    path('order_place/', PlaceOrderFromCartView.as_view(),name="placing order"),
    path('order/<int:order_id>/status/', UpdateOrderStatusView.as_view(),name='order_status'),
    path('update_order/<int:order_id>/', UpdateOrderStatusView.as_view(), name='update-order'),
]
   


urlpatterns += router.urls

