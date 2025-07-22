from rest_framework import generics, permissions,viewsets
from rest_framework.views import APIView
from .models import Cart, User,Product, Category,OrderItem,Order
from .serializers import RegisterSerializer, UserProfileSerializer, ProductSerializer, CategorySerializer,OrderItemSerializer
from decimal import Decimal
from rest_framework.response import Response
from decimal import Decimal
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        
        return request.method in permissions.SAFE_METHODS or request.user.is_staff

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]


class CreateOrderView(APIView):
    def post(self, request):
        items = request.data.get("items", [])
        order = Order.objects.create(user=request.user, total_price=0)
        total_price = Decimal("0.00")

        for item in items:
            product = Product.objects.get(id=item["product_id"])
            quantity = item["quantity"]

            if product.stock < quantity:
                return Response(
                    {"error": f"Not enough stock for {product.name}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Decrease stock
            product.stock -= quantity
            product.save()

            price = product.price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_purchase=price
            )

            total_price += price * quantity

        order.total_price = total_price
        order.save()

        return Response({"message": "Order placed successfully!"}, status=status.HTTP_201_CREATED)
    
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAdminUser]

# Add to cart
# orders/views.py

class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity += int(quantity)
        cart_item.save()

        return Response({'message': 'Added to cart'}, status=200)
# for placing the order
class PlaceOrderFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            return Response({'error': 'Cart is empty'}, status=400)

        order = Order.objects.create(user=request.user, total_price=0)
        total_price = Decimal("0.00")

        for item in cart_items:
            product = item.product
            if product.stock < item.quantity:
                return Response({'error': f"Not enough stock for {product.name}"}, status=400)

            product.stock -= item.quantity
            product.save()

            price = product.price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price_at_purchase=price
            )

            total_price += price * item.quantity

        order.total_price = total_price
        order.save()
        cart_items.delete()

        # Trigger WebSocket event for real-time update (Django Channels)
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{request.user.id}",
            {
                "type": "order.status",
                "message": f"Order #{order.id} placed with status {order.status}"
            }
        )

        return Response({'message': 'Order placed successfully'}, status=201)

# for Update Oder (admin)
class UpdateOrderStatusView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, order_id):
        status_value = request.data.get("status")
        if status_value not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=400)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        order.status = status_value
        order.save()

        # Send real-time notification
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{order.user.id}",
            {
                "type": "order.status",
                "message": f"Your order #{order.id} is now {status_value}"
            }
        )

        return Response({"message": "Order status updated"}, status=200)
    

@login_required
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.status = 'shipped'  # or 'delivered'
        order.save()

        # Broadcast to user's WebSocket group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{order.user.id}",
            {
                "type": "order_status",
                "message": f"Your order #{order.id} has been marked as {order.status}!"
            }
        )

        return JsonResponse({"message": "Order updated and broadcast sent!"})

    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)

class UpdateOrderStatusView(APIView):
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.status = request.data.get("status", "pending")
            order.save()

            # Notify user via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{order.user.id}",
                {
                    "type": "order_status",
                    "message": f"Your order #{order.id} is now {order.status}"
                }
            )

            return Response({"message": "Order status updated and user notified."}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)    