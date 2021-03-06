from django.shortcuts import render, reverse, get_object_or_404, HttpResponse
from django.conf import settings
import stripe

from catalog.views import Course

# Create your views here.
def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    cart = request.session.get('shopping_cart', {})
    
    line_items = []
    for id,course in cart.items():
        course = get_object_or_404(Course, pk=id)
        line_items.append({
            'name': course.title,
            'description': course.desc,
            'amount':int(course.cost * 100),
            'currency':'sgd',
            'quantity': 1
        })
        
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items = line_items,
        success_url=request.build_absolute_uri(reverse(checkout_success) + "?session_id={CHECKOUT_SESSION_ID}"),
        cancel_url=request.build_absolute_uri(reverse('home'))
    )
    
    return render(request, 'checkout/checkout.html',{
        'session_id':session.id,
        'public_key':settings.STRIPE_PUBLISHABLE_KEY
    })
    
    
def checkout_success(request):
    request.session['shopping_cart'] = {}
    return HttpResponse("Checkout success " + request.GET.get('session_id'))
