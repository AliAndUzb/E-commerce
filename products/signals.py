import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Order


@receiver(post_save, sender=Order)
def notify_admin(sender, instance, created, **kwargs):
    if created:  # Check if a new record is created
        token = settings.TELEGRAM_BOT_TOKEN
        admin_id = settings.ADMIN_ID
        method = 'sendMessage'

        # Prepare the message text (replace this with actual order details)
        message_text = f"New Order: {instance.id}\n Product: {instance.product.name}\n Quantity: {instance.quantity}\n " \
                       f"Client: {instance.customer.username}\n Tel: {instance.phone_number}"

        response = requests.post(
            url=f'https://api.telegram.org/bot{token}/{method}',
            data={'chat_id': admin_id, 'text': message_text}
        ).json()