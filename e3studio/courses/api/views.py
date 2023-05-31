# import os
# import matplotlib.pyplot as plt
# import seaborn as sb
# import pandas as pd
# import scipy as sp
# import numpy as np
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from courses.models import Subject
from .serializers import SubjectSerializer, MessageSerializer
from django.contrib.sites.models import Site


class SubjectListView(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        subject_obj = Subject.objects.all()
        subjectset = [item for item in Subject.objects.all()]
        serializer = SubjectSerializer(subjectset, many=True)
        serializer_data = serializer.data
        return Response(serializer.data)


class MessageSendView(UpdateAPIView):
    serializer_class = MessageSerializer

    def put(self, request, format=None):
        # current_site = get_current_site(request)
        current_site = Site.objects.get(id=1)
        email_subject = 'Message Received from {0} at E3 Studio'.format(
            request.data['name'])
        message = render_to_string('account/email/e3s_send_message.txt', {
            'user': request.data['name'],
            'email': request.data['email'],
            'message': request.data['message'],
            'domain': current_site.domain,
        })
        from_email = request.data['email']
        to_email = 'e3studio29@gmail.com'
        email = EmailMessage(email_subject, message, from_email, to=[to_email])
        email.send()
        return Response('Your message has been successfully sent. Please wait 1 to 2 days for my reply.')
