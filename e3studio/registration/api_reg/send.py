from django.core import signing
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import get_random_string
from allauth.account.models import EmailConfirmationHMAC, EmailAddress
from allauth.account import app_settings as account_settings
from rest_framework.response import Response
from urllib.parse import urlsplit
from datetime import datetime


def build_absolute_uri(request, location, protocol=None):
    """request.build_absolute_uri() helper
    Like request.build_absolute_uri, but gracefully handling
    the case where request is None.
    """
    # from .account import app_settings as account_settings

    if request is None:
        site = Site.objects.get_current()
        bits = urlsplit(location)
        if not (bits.scheme and bits.netloc):
            uri = "{proto}://{domain}{url}".format(
                proto=account_settings.DEFAULT_HTTP_PROTOCOL,
                domain=site.domain,
                url=location,
            )
        else:
            uri = location
    else:
        uri = request.build_absolute_uri(location)
    # NOTE: We only force a protocol if we are instructed to do so
    # (via the `protocol` parameter, or, if the default is set to
    # HTTPS. The latter keeps compatibility with the debatable use
    # case of running your site under both HTTP and HTTPS, where one
    # would want to make sure HTTPS links end up in password reset
    # mails even while they were initiated on an HTTP password reset
    # form.
    if not protocol and account_settings.DEFAULT_HTTP_PROTOCOL == "https":
        protocol = account_settings.DEFAULT_HTTP_PROTOCOL
    # (end NOTE)
    if protocol:
        uri = protocol + ":" + uri.partition(":")[2]
    return uri

    # def DEFAULT_HTTP_PROTOCOL(self):
    #     return self._setting("DEFAULT_HTTP_PROTOCOL", "http").lower()


def get_email_confirmation_url(request, key):
    """Constructs the email confirmation (activation) url.
    Note that if you have architected your system such that email
    confirmations are sent outside of the request context `request`
    can be `None` here.
    """
    url = reverse("account_confirm_email", args=[key])
    ret = build_absolute_uri(request, url)
    return ret


def send_confirmation_mail(request, user, email):
    key = signing.dumps(obj=email.pk, salt=account_settings.SALT)
    current_site = get_current_site(request)
    activate_url = get_email_confirmation_url(request, key)
    ctx = {
        "user": user,
        "activate_url": activate_url,
        "current_site": current_site,
        "key": key,
        "year": datetime.today().year,
    }
    # if signup:
    #     email_template = "account/email/email_confirmation_signup"
    # else:
    #     email_template = "account/email/email_confirmation"
    # return Response('hi')
    subject, from_email, to = 'EliteStudio Account Activation', 'lewischen856@gmail.com', email.email
    text_content = 'Your EliteStudio account requires your attention'
    # current_site = Site.objects.get(id=1)
    html_message = render_to_string(
        'account/email/email_user_signup.html', ctx)
    msg = EmailMultiAlternatives(
        subject, text_content, from_email, [to])
    msg.attach_alternative(html_message, "text/html")
    msg.send()
    return 'Sent'

    # self.send_mail(email_template, emailconfirmation.email_address.email, ctx)
