from zzz_lib.zzz_log import zzz_print

import copy
import datetime
from base64 import b64decode

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode

from ..models import mverificationcode

from ..forms import (
    mmhNewUserForm,
    mmhSignInForm,
    PasswordResetCustomForm,
)

from ..my_function import user_is_deactivated
from django.utils.html import strip_tags
import os

TEMP_DIR_HTMLPAGES      = 'auth_mmh_v2/layout/'
TEMP_DIR_EMAIL          = 'commonroom/email/auth/signup/'

from commonroom.myfunctions.send_email import send_email_customized

from ..extras import DivErrorList
# ******************************************************************************
def mmh_auth_register(request):
    zzz_print("    %-28s: %s" % ("mmh_auth_register", "********************"))
    form_error = ""
    if request.method == "POST":
        form = mmhNewUserForm(data=request.POST, error_class=DivErrorList)
        if form.is_valid():
            zzz_print("    %-28s: %s" % ("form.is_valid", ""))

            ## at first, save user given email add in a var 
            user_email_add = form.cleaned_data["email"]
            # save user_email_add in a session variable to be used in another view
            request.session['user_email_add'] = user_email_add

            ## Check if this email add is in 'deactivated acct' list
            chk = user_is_deactivated(user_email_add)
            if chk:
                form_error = "Email was used for account creation and then account was deactivated"
            ## else: do something
            else:
                # 2021/05/25: Users now log in with their email address.
                #             But we are still using Django's default user model.
                #             We no longer ask for a username when creating a new account.
                #             Instead we force a lower case version of the users email address into their username.
                #             And we use this as their username.
                user    = form.save()
                # Note: form data, specifically the username, is already forced to lowercase in form.save() method
                vc                  = mverificationcode.objects.create(user=user)
                zzz_print("    %-28s: user = %s, email = %s, vc = %s" % ("account created", user, user_email_add, vc))

                # send email to the user
                appname = "AUTH"
                subject = (user.first_name).capitalize() + ", thanks for creating your account!"
                to_emails_list = copy.deepcopy(settings.DEVELOPMENT_ONLY_EMAIL_RECIPIENTS)
                to_emails_list.append(user_email_add)
                email_context = {
                    'change_notice'     : 'Contact us from',
                    'submission_time'   : datetime.datetime.now(),
                    'msg'               : 'thanks for your contacting us',
                    'activation_code'   : vc.hash_value,
                    'dns_name'          : settings.DNS_NAME,
                    'protocol'          : settings.PROTOCOL,
                    'domain'            : settings.DOMAIN,

                }
                html_message_text = render_to_string(
                    template_name=TEMP_DIR_EMAIL + 'registration_verif_link_fancyhtml.html',
                    context=email_context,
                    using=None,
                    request=None
                )
                plain_message_text = strip_tags(html_message_text)
                send_email_customized(subject, plain_message_text, html_message_text, to_emails_list, appname)
                
                # redirect user to page thanking them for creating their account
                return redirect("auth_mmh_v2:signup_validation_temphold")
        
        else:
            zzz_print("    %-28s: %s" % ("NOT form.is_valid", ""))
    else:
        zzz_print("    %-28s: %s" % ("request.method", "!= POST"))
        form = mmhNewUserForm(error_class=DivErrorList)

    template_name   = TEMP_DIR_HTMLPAGES + "signup/signup-step1.html"
    context         = {
        "pg_header": "Sign Up",
        "form": form, 
        "form_error": form_error,
        "pg_layout_type" : "signup",
    }
    return render(request = request, template_name = template_name, context = context)


# ******************************************************************************
def mmh_auth_signup_validation_conf(request):
    zzz_print("    %-28s: %s" % ("mmh_auth_signup_validation_conf", "********************"))
    template_name   = TEMP_DIR_HTMLPAGES + "signup/signup-step2.html"
    context         = {
        "user_email": request.session.get('user_email_add'),
        "from_email": settings.EMAIL_CONFIG["AUTH"]["EMAIL_HOST_USER"],
        "verified": "Thank you for creating an account",
        "activation_code": "Please check your email for a validation link",
    }
    return render(request = request, template_name = template_name, context = context)


# ******************************************************************************
def mmh_auth_verify(request, activation_code):
    # import pdb; pdb.set_trace()
    zzz_print("    %-28s: %s" % ("mmh_auth_verify", "********************"))
    zzz_print("    %-28s: %s" % ("activation_code", activation_code))
    print(activation_code)
    verified_message = ""
    verified_succeeded = True
    try:
        decoded = b64decode(bytes(activation_code, 'utf-8'))
        zzz_print("    %-28s: %s" % ("decoded", decoded))
        user_email, code = decoded.decode('utf-8').split(':')
        zzz_print("    %-28s: %s" % ("user_email", user_email))
        zzz_print("    %-28s: %s" % ("code", code))

        iVerificationCode = mverificationcode.objects.get(user__email=user_email, code=code)
        print(iVerificationCode)
        # Test if this user has already been validated
        if not iVerificationCode.user.is_active:
            zzz_print("    %-28s: %s" % ("user.is_active", iVerificationCode.user.is_active))

            iVerificationCode.verified = timezone.now()
            iVerificationCode.save()
            iVerificationCode.user.is_active = True
            iVerificationCode.user.save()

            zzz_print("    %-28s: %s" % ("user.is_active", iVerificationCode.user.is_active))

            # send email to the user
            appname = "AUTH"
            subject = (iVerificationCode.user.first_name).capitalize() + ", thanks for verifying your account!",
            to_emails_list = copy.deepcopy(settings.DEVELOPMENT_ONLY_EMAIL_RECIPIENTS)
            to_emails_list.append(user_email)
            email_context = {
                'change_notice'     : 'Contact us from',
                'submission_time'   : datetime.datetime.now(),
                'msg'               : 'thanks for your contacting us',
                'first_name'        : 'thanks for your contacting us',
                'last_name'         : 'thanks for your contacting us',

            }
            html_message_text = render_to_string(
                template_name=TEMP_DIR_EMAIL + 'registration_complete_fancyhtml.html',
                context=email_context,
                using=None,
                request=None
            )
            plain_message_text = strip_tags(html_message_text)
            send_email_customized(subject, plain_message_text, html_message_text, to_emails_list, appname)
            print("send_email_customized from line#171 is called")

            verified_message = "Your account is now verified"
            print(verified_succeeded)
        else:
            zzz_print("    %-28s: %s" % ("user.is_active", iVerificationCode.user.is_active))
            verified_message = "Your account was already verified"
            print(verified_succeeded)

    except Exception as e:
        print("this is the exception {}".format(e))
        zzz_print("    %-28s: %s" % ("ERROR: activation_code", activation_code))
        verified_message = "Something went wrong in our server. Please try again later"
        verified_succeeded = False
        print(verified_succeeded)

    template_name   = TEMP_DIR_HTMLPAGES + "signup/signup-step3.html",
    context         = {
        "verified_message"  : verified_message,
        "verified_succeeded": verified_succeeded,
        "activation_code"   : activation_code,
    }
    return render(request = request, template_name = template_name, context = context)





