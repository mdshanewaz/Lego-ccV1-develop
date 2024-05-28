from datetime import datetime

from django.db.models import Q
from itertools import chain

# from haystack.query import SearchQuerySet 
import datetime
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from zzz_lib.zzz_log import zzz_print
from ..models import ContactUsModel

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

import logging
logger = logging.getLogger(__name__)

from .forms import (
    ContactUsForm,

)
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail, BadHeaderError
RESUME_FILE_TYPES = ['doc', 'docx']
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.generic.edit import FormMixin


import datetime
from django.http import HttpResponse


from django.views.generic.edit import FormView
from commonroom.myfunctions.send_email import send_email_customized
import copy


TEMP_DIR_ACTION         = 'resumeweb/layout/guest-actions/'
TEMP_DIR_PRODABOUT      = 'resumeweb/layout/product-docs/'
TEMP_DIR_EMAIL          = 'commonroom/email/general/'

# contact us
##########################################
# class ContactUsGuestView(FormView):
#     template_name = TEMP_DIR_ACTION + "contact-us.html"
#     # model = mcontactus
#     form_class = ContactUsForm
#     success_url = reverse_lazy('customerservice:contact_us_guest')
#     success_msg = "You message has been received successfully"

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.created_at = datetime.datetime.now()
#         self.object.save()
#         messages.success(self.request, self.success_msg)

#         # send email to the user
#         appname = "CUSTSUPP"
#         subject = "Thank you for contacting with us"
#         to_emails_list = copy.deepcopy(settings.DEVELOPMENT_ONLY_EMAIL_RECIPIENTS)
#         to_emails_list.append(form.cleaned_data['email'])
#         email_context = {
#             'change_notice'     : 'Contact us from',
#             'submission_time'   : datetime.datetime.now(),
#             'msg'               : 'thanks for your contacting us'
#         }
#         html_message_text = render_to_string(
#             template_name=TEMP_DIR_EMAIL + 'test106.html',
#             context=email_context,
#             using=None,
#             request=None
#         )
#         plain_message_text = strip_tags(html_message_text)
#         print("calling send_email_customized")
#         send_email_customized(subject, plain_message_text, html_message_text, to_emails_list, appname)
#         # email function ends


#         super(ContactUsGuest, self).form_valid(form)
#         return redirect('customerservice:contact_us_guest')

#     def get_context_data(self, **kwargs):
#         """Insert the form into the context dict."""
#         if 'form' not in kwargs:
#             kwargs['form'] = self.get_form()
#             kwargs['pg_layout_type'] = 'contact_us'
#             kwargs['pg_headline'] = 'Contact Us'
#         return super().get_context_data(**kwargs)


from .forms import ContactUsForm
from django.views.generic.edit import FormView

class ContactUsGuestView(FormView):
    template_name = TEMP_DIR_ACTION + "contact-us.html"
    form_class = ContactUsForm
    success_url = reverse_lazy('customerservice:contact_us_guest')
    success_msg = "You message has been received successfully"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)
        

class ContactUsGuestConfirmView(TemplateView):
    template_name = TEMP_DIR_ACTION + "contact-us-confirm.html"
