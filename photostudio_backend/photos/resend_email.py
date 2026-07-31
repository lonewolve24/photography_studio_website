import json
import logging
import urllib.error
import urllib.request

from django.conf import settings

from .models import Service, SiteSettings

logger = logging.getLogger(__name__)

RESEND_API_URL = 'https://api.resend.com/emails'


def _get_recipient_email():
    site_settings = SiteSettings.objects.first()
    if site_settings and site_settings.email:
        return site_settings.email
    if settings.CONTACT_TO_EMAIL:
        return settings.CONTACT_TO_EMAIL
    raise ValueError('No recipient email configured. Set Site Settings email or CONTACT_TO_EMAIL.')


def _service_label(service_slug):
    if not service_slug:
        return 'Not specified'
    service = Service.objects.filter(slug=service_slug).first()
    return service.title if service else service_slug.replace('-', ' ').title()


def _send_resend_email(*, to, subject, html, reply_to=None):
    if not settings.RESEND_API_KEY:
        logger.warning('RESEND_API_KEY not set — email not sent.')
        return

    payload = {
        'from': settings.RESEND_FROM_EMAIL,
        'to': [to] if isinstance(to, str) else to,
        'subject': subject,
        'html': html,
    }
    if reply_to:
        payload['reply_to'] = reply_to

    request = urllib.request.Request(
        RESEND_API_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {settings.RESEND_API_KEY}',
            'Content-Type': 'application/json',
            'User-Agent': 'Shotz-Contact-Form/1.0',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            response.read()
        logger.info('Email sent to %s — subject: %s', to, subject)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        logger.error('Resend API error %s: %s', exc.code, body)
    except Exception:
        logger.exception('Unexpected error sending email to %s', to)


def send_contact_notification(form_data):
    """Send inquiry notification to the studio — no auto-reply to visitor."""
    name = form_data['name']
    email = form_data['email']
    phone = form_data.get('phone') or 'Not provided'
    service = _service_label(form_data.get('service'))
    message = form_data['message']
    preferred_date = form_data.get('date') or 'Not specified'

    try:
        recipient = _get_recipient_email()
    except ValueError:
        logger.error('No recipient email configured — contact notification not sent.')
        return

    html = f"""
    <h2 style="color:#10344c;">New Contact / Booking Inquiry</h2>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
    <p><strong>Phone:</strong> {phone}</p>
    <p><strong>Service:</strong> {service}</p>
    <p><strong>Preferred Date:</strong> {preferred_date}</p>
    <hr>
    <p><strong>Message:</strong></p>
    <p>{message.replace(chr(10), '<br>')}</p>
    <br>
    <p style="color:#888;font-size:12px;">Sent via Shotz contact form</p>
    """

    _send_resend_email(
        to=recipient,
        subject=f'New inquiry from {name} — Shotz',
        html=html,
        reply_to=email,
    )
