from django.conf import settings

from .models import Favorite


def contact_context(request):
    whatsapp_number = str(getattr(settings, 'WHATSAPP_NUMBER', '') or '').strip()
    whatsapp_digits = ''.join(ch for ch in whatsapp_number if ch.isdigit())
    if len(whatsapp_digits) == 10:
        whatsapp_link_number = f"91{whatsapp_digits}"
    else:
        whatsapp_link_number = whatsapp_digits

    favorite_product_ids = []
    favorites_qs = Favorite.objects.none()
    if request.user.is_authenticated:
        favorites_qs = Favorite.objects.filter(user=request.user, hamper__is_active=True)
    else:
        session_key = request.session.session_key
        if session_key:
            favorites_qs = Favorite.objects.filter(session_key=session_key, hamper__is_active=True)

    favorite_product_ids = list(favorites_qs.values_list('hamper_id', flat=True))

    return {
        'whatsapp_number': whatsapp_link_number,
        'whatsapp_message': getattr(settings, 'WHATSAPP_MESSAGE', ''),
        'phone_number': getattr(settings, 'PHONE_NUMBER', ''),
        'phone_number_raw': getattr(settings, 'PHONE_NUMBER_RAW', ''),
        'favorites_count': len(favorite_product_ids),
        'favorite_product_ids': favorite_product_ids,
    }
