from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import PostCategory
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


def send_notifications(preview, pk, header_post, subscribers):
    html_content = render_to_string('appointment_created.html',
                                    {
                                        'text_post': preview,
                                        'link': f'{settings.SITE_URL}/news/{pk}'
                                    })
    msg = EmailMultiAlternatives(
        subject=header_post,
        body='',
        from_email='rudeigos1995@yandex.ru',
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@receiver(m2m_changed, sender=PostCategory)
def notify_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers = []

        for cat in categories:
            subscribers += cat.subscribers.all()
        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.header_post, subscribers)