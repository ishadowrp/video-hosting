from celery import shared_task

from accounts.models import Notification, User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import datetime


@shared_task
def notifications_email_sending():
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=3)
    full_url = ''.join(['http://', get_current_site(None).domain, ':8000'])

    for u in User.objects.all():
        list_of_notifications = Notification.objects.filter(created__range=(start_date, end_date), user=u,
                                                            status_read=False)
        if len(list_of_notifications) > 0:
            html_content = render_to_string(
                'subs_email_each_day.html',
                dict(notifications=list_of_notifications, usr=u, full_url=full_url)
            )
            msg = EmailMultiAlternatives(
                subject=f'Hi, {u.first_name} {u.last_name}. You missed some notifications',
                body='',
                # это то же, что и message
                from_email='ilya.dinaburgskiy@yandex.ru',
                to=[f'{u.email}'],  # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()  # отсылаем
