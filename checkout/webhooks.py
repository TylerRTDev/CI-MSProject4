# views.py
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
import stripe
from .models import CheckoutOrder
import stripe

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponseBadRequest()

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        stripe_session_id = session['id']
        metadata = session.get('metadata', {})
        guest_email = metadata.get('guest_email')
        full_name = metadata.get('full_name')
        shipping_address = metadata.get('shipping_address')
        shipping_city = metadata.get('shipping_city')
        shipping_postcode = metadata.get('shipping_postcode')
        billing_address = metadata.get('billing_address')
        billing_city = metadata.get('billing_city')
        billing_postcode = metadata.get('billing_postcode')
        
        if CheckoutOrder.objects.filter(stripe_session_id=stripe_session_id).exists():
            return JsonResponse({'status': 'duplicate'}, status=200)
        
        order = CheckoutOrder.objects.create(
            guest_email=guest_email,
            full_name=full_name,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_postcode=shipping_postcode,
            billing_address=billing_address,
            billing_city=billing_city,
            billing_postcode=billing_postcode,
            total_amount=session['amount_total'] / 100,
            stripe_session_id=stripe_session_id
        )

    return JsonResponse({'status': 'success'})
