from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
from .models import Category, Shoe, Cart, CartItem, Order
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY

def landing_page(request):
    categories = Category.objects.filter(parent_category__isnull=True)
    return render(request, 'store/landing_page.html', {'categories': categories})

def home_page(request):
    categories = Category.objects.filter(parent_category__isnull=True)
    return render(request, 'store/home_page.html', {'categories': categories})

def product_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Shoe.objects.filter(category=category)
    return render(request, 'store/product_list.html', {'category': category, 'products': products})

def product_detail(request, shoe_id):
    product = get_object_or_404(Shoe, id=shoe_id) 
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def add_to_cart(request, shoe_id):
    shoe = get_object_or_404(Shoe, id=shoe_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, shoe=shoe, defaults={'quantity': 1})

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

@login_required
def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None

    return render(request, 'store/cart.html', {'cart': cart})

@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            amount = int(cart.get_total_price() * 100)
            YOUR_DOMAIN = "http://localhost:8000"  # Update this with your domain

            # Create an order for each item in the cart
            for cart_item in cart.cartitem_set.all():
                Order.objects.create(user=request.user, shoe=cart_item.shoe, quantity=cart_item.quantity)

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'inr',
                            'product_data': {
                                'name': 'Total Amount',
                            },
                            'unit_amount': amount,
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/orderplaced/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )

            return JsonResponse({'id': checkout_session.id})
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart not found'}, status=404)


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        subtotal = cart.get_total_price()
    except Cart.DoesNotExist:
        subtotal = 0  

    return render(request, 'store/checkout.html', {'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY, 'subtotal': subtotal})

@login_required
def payment_cancel(request):
    return render(request, 'store/payment_cancel.html')


@login_required
def order_placed(request):
    try:
        latest_order = Order.objects.filter(user=request.user).latest('id')
        
        total_amount_paid = latest_order.shoe.price * latest_order.quantity

        return render(request, 'store/order_placed.html', {
            'latest_order': latest_order,
           
            'total_amount_paid': total_amount_paid,
            'order_id': latest_order.id
        })
    except Order.DoesNotExist:
        return render(request, 'store/order_placed.html')

from io import BytesIO
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def generate_pdf_bill(order):
    response = BytesIO()

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Heading - Added a title above the table
    styles = getSampleStyleSheet()
    title = Paragraph("<b>Order Invoice</b>", styles['Title'])
    elements.append(title)
    elements.append(Paragraph("<br/>", styles['Normal']))  # Space between title and table

    # Order Information
    order_info = [
        ["Order Number:", f"{order.id}"],
        ["Order Date:", f"{order.created_at.strftime('%Y-%m-%d %H:%M:%S')}"],  # assuming you have created_at field in Order
        ["Total Amount Paid:", f"Rs.{order.shoe.price * order.quantity}"],
    ]
    order_table = Table(order_info, colWidths=[2 * inch, 4 * inch])
    order_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(order_table)

    # Shoe Information
    shoe_info = [
        ["Shoe Name:", order.shoe.name],
        ["Description:", Paragraph(order.shoe.description, styles['BodyText'])],  # Wrapping the description
        ["Size:", order.shoe.size],
        ["Price:", f"Rs.{order.shoe.price}"],
        ["Quantity:", order.quantity],
        ["Subtotal:", f"Rs.{order.shoe.price * order.quantity}"],
    ]

    # Table for shoe info with automatic text wrapping for description
    shoe_table = Table(shoe_info, colWidths=[2 * inch, 4 * inch])
    shoe_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Align text to the top of the cell
    ]))

    elements.append(shoe_table)

    # Build PDF
    doc.build(elements)

    response.seek(0)
    return response


@login_required
def view_pdf_bill(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    buffer = generate_pdf_bill(order)

    return FileResponse(buffer, as_attachment=False, filename=f"Order_{order_id}.pdf")

@login_required
def order_report(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, 'store/order_report.html', {'orders': orders})

