from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Cart, CartItem, Payment, Order, OrderItem, Coupon
from cursos.models import Course, Enrollment
import stripe
import json
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def cart_view(request):
    """
    Vista del carrito de compras
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'payments/cart.html', context)

@login_required
@csrf_exempt
def remove_from_cart(request):
    """
    Remover item del carrito
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        course_id = data.get('course_id')
        
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, course_id=course_id)
            cart_item.delete()
            
            return JsonResponse({'success': True, 'message': 'Curso removido del carrito'})
            
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return JsonResponse({'error': 'Item no encontrado en el carrito'}, status=404)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def checkout(request):
    """
    Proceso de checkout
    """
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('cart')
    
    # Crear orden
    order = Order.objects.create(
        user=request.user,
        subtotal=cart.total_amount,
        total_amount=cart.total_amount
    )
    
    # Crear items de la orden
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            course=cart_item.course,
            price=cart_item.course.final_price
        )
    
    context = {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'payments/checkout.html', context)

@login_required
@csrf_exempt
def create_payment_intent(request):
    """
    Crear Payment Intent de Stripe
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')
        
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            
            # Crear Payment Intent
            intent = stripe.PaymentIntent.create(
                amount=int(order.total_amount * 100),  # Stripe usa centavos
                currency='usd',
                metadata={
                    'order_id': order.id,
                    'user_id': request.user.id
                }
            )
            
            return JsonResponse({
                'client_secret': intent.client_secret
            })
            
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Orden no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
@csrf_exempt
def confirm_payment(request):
    """
    Confirmar pago y completar inscripción
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_intent_id = data.get('payment_intent_id')
        order_id = data.get('order_id')
        
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            
            # Verificar payment intent con Stripe
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status == 'succeeded':
                # Crear registro de pago
                for order_item in order.items.all():
                    Payment.objects.create(
                        user=request.user,
                        course=order_item.course,
                        payment_method='stripe',
                        amount=order_item.price,
                        status='completed',
                        stripe_payment_intent_id=payment_intent_id
                    )
                    
                    # Crear inscripción
                    Enrollment.objects.get_or_create(
                        student=request.user,
                        course=order_item.course
                    )
                
                # Actualizar orden
                order.status = 'completed'
                order.save()
                
                # Limpiar carrito
                cart = Cart.objects.get(user=request.user)
                cart.items.all().delete()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Pago procesado correctamente'
                })
            else:
                return JsonResponse({'error': 'Pago no completado'}, status=400)
                
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Orden no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def payment_success(request, order_id):
    """
    Página de éxito del pago
    """
    order = get_object_or_404(Order, id=order_id, user=request.user, status='completed')
    
    context = {
        'order': order,
    }
    return render(request, 'payments/success.html', context)

@login_required
def my_orders(request):
    """
    Órdenes del usuario
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'payments/orders.html', context)

@login_required
@csrf_exempt
def apply_coupon(request):
    """
    Aplicar cupón de descuento
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        coupon_code = data.get('coupon_code')
        order_id = data.get('order_id')
        
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            order = Order.objects.get(id=order_id, user=request.user)
            
            if not coupon.is_valid():
                return JsonResponse({'error': 'Cupón no válido o expirado'}, status=400)
            
            if order.subtotal < coupon.minimum_amount:
                return JsonResponse({
                    'error': f'El monto mínimo para este cupón es ${coupon.minimum_amount}'
                }, status=400)
            
            # Calcular descuento
            if coupon.discount_type == 'percentage':
                discount = order.subtotal * (coupon.discount_value / 100)
            else:
                discount = coupon.discount_value
            
            # Actualizar orden
            order.coupon = coupon
            order.discount_amount = discount
            order.total_amount = order.subtotal - discount
            order.save()
            
            # Incrementar uso del cupón
            coupon.used_count += 1
            coupon.save()
            
            return JsonResponse({
                'success': True,
                'discount_amount': float(discount),
                'total_amount': float(order.total_amount)
            })
            
        except Coupon.DoesNotExist:
            return JsonResponse({'error': 'Cupón no encontrado'}, status=404)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Orden no encontrada'}, status=404)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)
