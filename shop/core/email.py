import os

from django.core.mail import send_mail

import app.settings as settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class OrderEmailSender:

    def send_order_created(self, order):
        self._send(
            subject="Заказ успешно оформлен",
            message=f"Вы оформили заказ на сайте неформатного магазина \"Культура\"\n"
                    f"НОМЕР ЗАКАЗА: {order.customer_id}\n"
                    f"К оплате: {order.cart_total()}",
            html_message=render_to_string('shop/order_created.html', {'order': order}),
            email=order.email
        )

    def _send(self, subject, message, html_message, email):
        send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            auth_user=settings.EMAIL_HOST_USER,
            auth_password=settings.EMAIL_HOST_PASSWORD,
            recipient_list=[email],
            fail_silently=False,
        )
