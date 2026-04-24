from django.conf import settings

def whatsapp_link(request):
    """Exposes the WHATSAPP_CHANNEL_URL from settings to all templates."""
    return {
        'WHATSAPP_CHANNEL_URL': getattr(settings, 'WHATSAPP_CHANNEL_URL', '')
    }
