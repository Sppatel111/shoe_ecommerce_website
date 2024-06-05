from django.urls import path
from . import views
from .views import order_report

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home_page, name='home_page'),
    path('category/<int:category_id>/', views.product_list, name='product_list'),
    path('product/<int:shoe_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_to_cart/<int:shoe_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order_placed/', views.order_placed, name='order_placed'),
    path('orderplaced/', views.order_placed, name='order_placed'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),  # Add this line
    path('view-pdf-bill/<int:order_id>/', views.view_pdf_bill, name='view_pdf_bill'),
    path('order-report/', order_report, name='order_report'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

