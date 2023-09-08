from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib import messages
from products.models import Product
from checkout.models import Coupon


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})
    coupon_id = request.session.get("coupon_id", int())

    try:
        coupon = Coupon.objects.get(id=coupon_id)

    except Coupon.DoesNotExist:
        coupon = None

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.sort_price
        product_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if total != 0 and total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    if coupon:
        discount = total * Decimal(coupon.discount / 100)
        grand_total = total - discount + delivery
        stripe_total = round(grand_total * 100)
    else:
        discount = 0
        grand_total = delivery + total
        stripe_total = round(grand_total * 100)
    
    grand_total = delivery + total
    
    context = {
        'bag_items': bag_items,
        'coupon': coupon,
        'discount': discount,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context