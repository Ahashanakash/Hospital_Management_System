from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from . import models
from . import serializers
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

class ContactusViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = models.ContactUs.objects.all()
    serializer_class = serializers.ContactUsSerializer

    def perform_create(self, serializer):
        contact = serializer.save()
        subject = f"New Contact Us message from {contact.name}"
        message = (
            f"Name: {contact.name}\n"
            f"Phone: {contact.phone}\n"
            f"Email: {contact.email}\n\n"
            f"Problem/Message:\n{contact.problem}"
        )
        sender = settings.EMAIL_HOST_USER
        admin_recipient = getattr(settings, 'CONTACT_EMAIL', settings.EMAIL_HOST_USER)
        reply_to_list = [contact.email] if contact.email else []
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=sender,
            to=[admin_recipient],
            reply_to=reply_to_list,
        )
        email.send(fail_silently=False)

       