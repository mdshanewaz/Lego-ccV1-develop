from zzz_lib.zzz_log import zzz_print, zzz_print_exit
import datetime
import copy
from decimal import Decimal
from pprint import pprint
import os
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView  # , UpdateView
from django.views.generic.base import TemplateView

from resumeweb.models import mcart, mprod_exp180
from resumeweb.models import mcart_fileupload
from resumeweb.models import mcompleted_refund, form_mcompleted_refund
from resumeweb.models import mpaypal
from resumeweb.models import msendmail
from resumeweb.views.cart_context import cart_context_forQuerySet, cart_context_forTrackingId, cart_context_loggit

from resumeweb.views.vusergroup import test_is_default_group

from prof_candidate.send_email import send_email_to_user

# from io import BytesIO
# from xhtml2pdf import pisa


TEMPLATE_DIR = "prof_candidate/layout/my_orders/"


# check order status
# ==============================
class OrderStatusCheck(LoginRequiredMixin, DetailView):
    model = mcart
    template_name = TEMPLATE_DIR + "order_status_check.html"


# order status update
# ==============================
class OrderStatusResult(LoginRequiredMixin, ListView):
    template_name = TEMPLATE_DIR + "order_status_check.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["count"] = self.count or 0
        context["query"] = self.request.GET.get('order_status_search')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('order_status_search', None)

        if query is not None:
            result = mprod_exp180.objects.filter(title__icontains=query)
            return result
        return mprod_exp180.objects.none()


# # order status update
# # ==============================
# class MyInvoices(LoginRequiredMixin, TemplateView):
#     template_name = TEMPLATE_DIR + "my_invoices.html"


# ******************************************************************************
@user_passes_test(test_is_default_group, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_default_group", 'viewname': "OrderHistoryAll"}))
def OrderHistoryAll(request):
    zzz_print("    %-28s: %s" % ("OrderHistoryAll", "********************"))
    template = loader.get_template(TEMPLATE_DIR + "order_history.html")
    qs = mcart.objects.mcartInstance_userOrderHistory_all(
        request).order_by('-created')
    # zzz_print("    %-28s: %s" % ("qs.count()", qs.count()))
    context = {
        "no_of_orders": qs.count(),
        "object_list": qs,
        "section_header_1": "My Order History",
    }
    return HttpResponse(template.render(context, request))


# ******************************************************************************
@user_passes_test(test_is_default_group, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_default_group", 'viewname': "OrderHistoryPending"}))
def OrderHistoryPending(request):
    zzz_print("    %-28s: %s" %
              ("OrderHistoryPending", "********************"))
    template = loader.get_template(TEMPLATE_DIR + "order_history.html")
    # mmh: Due to merge of this view with processing view we need to do two queries for each status
    # qs = mcart.objects.mcartQS_userOrderHistory_byStatus(request, "pending")
    # qs = mcart.objects.mcartQS_userOrderHistory_byStatus(request, "processing")

    qs = mcart.objects.mcartQS_userOrderHistory_byStatus(request, "pending")
    qs2 = mcart.objects.mcartQS_userOrderHistory_byStatus(
        request, "processing")
    # zzz_print("    %-28s: %s" % ("qs.count()", qs.count()))
    # zzz_print("    %-28s: %s" % ("qs2.count()", qs2.count()))

    # Then merge queries with union
    qs3 = qs.union(qs2).order_by('id')
    # zzz_print("    %-28s: %s" % ("qs3.count()", qs3.count()))
    context = {
        "no_of_orders": qs3.count(),
        "object_list": qs3,
    }
    return HttpResponse(template.render(context, request))


# mmh: removed when processing merged into pending view
# # ******************************************************************************
# @user_passes_test(test_is_default_group, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_default_group", 'viewname': "OrderHistoryInProcessing"}))
# def OrderHistoryInProcessing(request):
#     zzz_print("    %-28s: %s" % ("OrderHistoryInProcessing", "********************"))
#     template = loader.get_template(TEMPLATE_DIR + "order_history.html")
#     qs = mcart.objects.mcartQS_userOrderHistory_byStatus(request, "processing")
#     context = {
#         "no_of_orders"  : qs.count(),
#         "object_list"   : qs,
#     }
#     return HttpResponse(template.render(context, request))


# ******************************************************************************
@user_passes_test(test_is_default_group, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_default_group", 'viewname': "OrderHistoryDelivered"}))
def OrderHistoryDelivered(request):
    zzz_print("    %-28s: %s" %
              ("OrderHistoryDelivered", "********************"))
    template = loader.get_template(TEMPLATE_DIR + "order_history.html")
    qs = mcart.objects.mcartQS_userOrderHistory_byStatus(request, "delivered")
    context = {
        "no_of_orders": qs.count(),
        "object_list": qs,
    }
    return HttpResponse(template.render(context, request))


# ******************************************************************************
@user_passes_test(test_is_default_group, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_default_group", 'viewname': "OrderHistoryCancelled"}))
def OrderHistoryCancelled(request):
    zzz_print("    %-28s: %s" % ("OrderHistoryCancelled", ""))
    template = loader.get_template(TEMPLATE_DIR + "order_history.html")
    qs = mcart.objects.mcartQS_userOrderHistory_byStatus(request, "cancelled")

    context = {
        "no_of_orders": qs.count(),
        "object_list": qs,
        "section_header_1": "Cancelled Orders",
    }
    return HttpResponse(template.render(context, request))


# ******************************************************************************
@user_passes_test(test_is_default_group, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_default_group", 'viewname': "OrderHistoryError"}))
def OrderHistoryError(request):
    zzz_print("    %-28s: %s" % ("OrderHistoryError", ""))
    template = loader.get_template(TEMPLATE_DIR + "order_history_wrapper.html")
    qs = mcart.objects.mcartQS_userOrderHistory_byStatus(request, "error")

    context = {
        "no_of_orders": qs.count(),
        "object_list": qs,
    }
    return HttpResponse(template.render(context, request))


# ******************************************************************************
@user_passes_test(test_is_default_group, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_default_group", 'viewname': "CancelOrder_mmh"}))
def CancelOrder_mmh(request, tracking_id):
    zzz_print("    %-28s: %s" % ("CancelOrder_mmh", tracking_id))

    qs = mcart.objects.mcartInstance_userOrderHistory_byTrackingId(
        request, tracking_id)
    zzz_print("    %-28s: %s" % ("qs.count()", qs.count()))

    # FATAL ERROR:
    # MMH: CHANGE THIS TO CAPTURING ERROR MESSAGE AND REDIRECTING TO AN ERROR VIEW PAGE WHERE THIS MESSAGE IS DISPLAYED AND LOGGED
    if qs.count() != 1:
        zzz_print_exit("    %-28s: %s" % ("qs.count() != 1", qs.count()))

    mcart_instance = qs[0]

    # FATAL ERROR:
    # MMH: CHANGE THIS TO CAPTURING ERROR MESSAGE AND REDIRECTING TO AN ERROR VIEW PAGE WHERE THIS MESSAGE IS DISPLAYED AND LOGGED
    if mcart_instance.grace_left_in_seconds() < 1:
        zzz_print_exit("    %-28s: %s" % ("grace_left_in_seconds < 1",
                       mcart_instance.grace_left_in_seconds()))

    # FATAL ERROR:
    # MMH: CHANGE THIS TO CAPTURING ERROR MESSAGE AND REDIRECTING TO AN ERROR VIEW PAGE WHERE THIS MESSAGE IS DISPLAYED AND LOGGED
    if mcart_instance.processing_status == "delivered":
        zzz_print_exit("    %-28s: %s" % ("mcart_instance.processing_status",
                       mcart_instance.processing_status))
    if mcart_instance.processing_status == "cancelled":
        zzz_print_exit("    %-28s: %s" % ("mcart_instance.processing_status",
                       mcart_instance.processing_status))
    if mcart_instance.processing_status == "error":
        zzz_print_exit("    %-28s: %s" % ("mcart_instance.processing_status",
                       mcart_instance.processing_status))

    zzz_print("    %-28s: %s" % ("request.method", request.method))
    if request.method == 'POST':
        form = form_mcompleted_refund(request.POST, request.FILES)
        if form.is_valid():
            reason = form.cleaned_data.get('reason')
            explanation = form.cleaned_data.get('explanation')
            zzz_print("    %-28s: %s" % ("reason", reason))
            zzz_print("    %-28s: %s" % ("explanation", explanation))

            capture_id = mcart_instance.mcompleted_purchase.capture_id
            zzz_print("    %-28s: %s" % ("capture_id", capture_id))

            if not capture_id:
                zzz_print("    %-28s: %s" % ("CAPTURE_ID",
                          "NOT SET. ARE YOU USING OLD PURCHASES???"))
                zzz_print("    %-28s: %s" % ("CAPTURE_ID",
                          "NOT SET. ARE YOU USING OLD PURCHASES???"))
                zzz_print("    %-28s: %s" % ("CAPTURE_ID",
                          "NOT SET. ARE YOU USING OLD PURCHASES???"))
                zzz_print("    %-28s: %s" % ("CAPTURE_ID",
                          "NOT SET. ARE YOU USING OLD PURCHASES???"))
                zzz_print_exit("    %-28s: %s" % ("CAPTURE_ID",
                               "NOT SET. ARE YOU USING OLD PURCHASES???"))

            mcart_qs = mcart.objects.filter(id=mcart_instance.id)
            zzz_print("    %-28s: %s" % ("mcart_qs.count()", mcart_qs.count()))

            cart_context = cart_context_forQuerySet(request, mcart_qs)

            ipaypal = mpaypal.objects.mpaypal_add("mpaypal_capture_refund")
            ipaypal.mpaypal_capture_refund(capture_id, cart_context)
            data = ipaypal.get_response_data()

            # zzz_print("    %-28s: %s" % ("data", "-----------------------------"))
            # pprint(data)
            # zzz_print("    %-28s: %s" % ("data", "-----------------------------"))

            # EXAMPLE OF DATA
            # {'amount': {'currency_code': 'USD', 'value': '2.00'},
            #  'create_time': '2021-06-07T10:20:06-07:00',
            #  'id': '6R6981378Y194730V',
            #  'links': [{'href': 'https://api.sandbox.paypal.com/v2/payments/refunds/6R6981378Y194730V',
            #             'method': 'GET',
            #             'rel': 'self'},
            #            {'href': 'https://api.sandbox.paypal.com/v2/payments/captures/1BK406470M5627505',
            #             'method': 'GET',
            #             'rel': 'up'}],
            #  'seller_payable_breakdown': {'gross_amount': {'currency_code': 'USD',
            #                                                'value': '2.00'},
            #                               'net_amount': {'currency_code': 'USD',
            #                                              'value': '1.94'},
            #                               'paypal_fee': {'currency_code': 'USD',
            #                                              'value': '0.06'},
            #                               'total_refunded_amount': {'currency_code': 'USD',
            #                                                         'value': '2.00'}},
            #  'status': 'COMPLETED',
            #  'update_time': '2021-06-07T10:20:06-07:00'}

            to_emails_list = copy.deepcopy(settings.DEVELOPMENT_ONLY_EMAIL_RECIPIENTS)
            if request.user.is_authenticated:
                to_emails_list.append(request.user.email)
            elif 'mmh_guestemailaddress' in request.session:
                to_emails_list.append(request.session['mmh_guestemailaddress'])
            elif mcart_instance.mcompleted_purchase.guest_login_email_address:
                to_emails_list.append(
                    mcart_instance.mcompleted_purchase.guest_login_email_address)
            else:
                zzz_print("    %-28s: %s" % ("WARNING", "(NOT request.user.is_authenticated) AND (mmh_guestemailaddress NOT in request.session) and (NOT IN mcart_instance.mcompleted_purchase.guest_login_email_address)"))

            if data and data['status'] == 'COMPLETED':
                # zzz_print("    %-28s: %s" % ("refund data['id']", data['id']))
                mcart_instance.set_processing_status_cancelled()

                # create mcompleted_refund instance
                icompleted_refund = mcompleted_refund.objects.add_mcompleted_refund(
                    paypalrefund_id=data['id'],
                    amount_currencycode=data['amount']['currency_code'],
                    amount_value=Decimal(data['amount']['value']),
                    reason=reason,
                    explanation=explanation
                )
                # and update mcart_instance foreign key for this new mcompleted_refund instance
                mcart_instance.mcompleted_refund = icompleted_refund
                mcart_instance.save()

                # SEND AN EMAIL CONFIRMING REFUND APPROVED.
                plain_message_text = "About the cancellation: \n" + os.linesep
                # plain_message_text  += "date: "+ str(datetime.datetime.now())+"\n"
                plain_message_text += "Amount: $" + \
                    data['amount']['value'] + "\n" + os.linesep
                plain_message_text += "PayPal Refund Reference Id: " + \
                    data['id']+"\n" + os.linesep
                plain_message_text += "About the original order: " + \
                    mcart_instance.title + "." + os.linesep
                change_notice = plain_message_text
                # imsendmail = msendmail.objects.add(
                #     subject             = request.user.first_name + ", a refund was processed",
                #     plain_message       = plain_message_text,
                #     html_message        = html_message_text,
                #     from_email          = settings.EMAIL_HOST_USER,
                #     to_emails_list      = to_emails_list
                # )
                # imsendmail.send_to_each_recipient_seperately()
                email_address = request.user.email
                subject = "Order cancelled successfully"
                time = datetime.datetime.now()
                send_email_to_user(email_address, subject, change_notice, time)

                return HttpResponseRedirect(
                    reverse('prof_candidate:mmh_cancel_order_success', kwargs={
                            'tracking_id': mcart_instance.tracking_id})
                )
            else:  # refund failed
                mcart_instance.set_processing_status_error()

                # SEND AN EMAIL INDICATING REFUND FAILED
                plain_message_text = "A refund of " + \
                    data['amount']['value'] + " was NOT, REPEAT NOT, successfully processed for the cancellation of " + \
                    mcart_instance.title + "."
                plain_message_text += " PayPal Refund Reference Id = " + \
                    data['id'] + "."
                plain_message_text += " This email text and its html version need work."
                html_message_text = plain_message_text
                imsendmail = msendmail.objects.add(
                    subject=request.user.first_name + ", a refund FAILED TO process",
                    plain_message=plain_message_text,
                    html_message=html_message_text,
                    from_email=settings.EMAIL_HOST_USER,
                    to_emails_list=to_emails_list
                )
                imsendmail.send_to_each_recipient_seperately()

                return HttpResponseRedirect(
                    reverse('prof_candidate:mmh_cancel_order_failed', kwargs={
                            'tracking_id': mcart_instance.tracking_id})
                )
        else:
            zzz_print("    %-28s: %s" % ("form.is NOT valid()", ""))
    else:
        form = form_mcompleted_refund()

    form_html = render_to_string(
        "prof_candidate/pg-contents/my_orders/mmh_tform.html", {'form': form}, request=request)
    template = loader.get_template(TEMPLATE_DIR + "order_cancel.html")
    context = {
        "header_text": "Cancelling Order",
        "object": mcart_instance,
        "form": form_html,
    }
    return HttpResponse(template.render(context, request))


# ******************************************************************************
@user_passes_test(test_is_default_group, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_default_group", 'viewname': "CancelOrderSuccess_mmh"}))
def CancelOrderSuccess_mmh(request, tracking_id):
    zzz_print("    %-28s: %s" % ("CancelOrderSuccess_mmh", tracking_id))

    qs = mcart.objects.mcartInstance_userOrderHistory_byTrackingId(
        request, tracking_id)
    zzz_print("    %-28s: %s" % ("qs.count()", qs.count()))
    mcart_instance = qs[0]

    template = loader.get_template(TEMPLATE_DIR + "order_cancel.html")
    context = {
        "header_text": "Order Cancelled",
        "object": mcart_instance,
        "form": "",
    }
    return HttpResponse(template.render(context, request))


# ******************************************************************************
@user_passes_test(test_is_default_group, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_default_group", 'viewname': "CancelOrderFailed_mmh"}))
def CancelOrderFailed_mmh(request, tracking_id):
    zzz_print("    %-28s: %s" % ("CancelOrderFailed_mmh", tracking_id))

    qs = mcart.objects.mcartInstance_userOrderHistory_byTrackingId(
        request, tracking_id)
    zzz_print("    %-28s: %s" % ("qs.count()", qs.count()))
    mcart_instance = qs[0]

    template = loader.get_template(TEMPLATE_DIR + "order_cancel.html")
    context = {
        "header_text": "ATTEMPT TO CANCEL ORDER FAILED!!!!!!!!!!",
        "object": mcart_instance,
        "form": "",
    }
    return HttpResponse(template.render(context, request))


# ******************************************************************************
@user_passes_test(test_is_default_group, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_default_group", 'viewname': "OrderDetails"}))
def OrderDetails(request, tracking_id):
    zzz_print("    %-28s: %s" % ("OrderDetails", tracking_id))

    cart_context = cart_context_forTrackingId(request, tracking_id)
    cart_context_loggit(cart_context)

    mcart_instance = cart_context['products_list'][0]['mcart']

    serviceoption_total = 0
    for serviceoption in cart_context['products_list'][0]['mcart_serviceoptions']:
        serviceoption_total += serviceoption.price
    zzz_print("    %-28s: %s" % ("serviceoption_total", serviceoption_total))

    resume_uploaded = ""
    if cart_context['resume_required']:
        imcart_fileupload = mcart_fileupload.objects.get(
            mcompleted_purchase=mcart_instance.mcompleted_purchase
        )
        resume_uploaded = imcart_fileupload.document

    mcart_deliveryoption = None
    if len(cart_context['products_list'][0]['mcart_deliveryoptions']):
        mcart_deliveryoption = cart_context['products_list'][0]['mcart_deliveryoptions'][0]

    context = {
        "mcart_instance": mcart_instance,
        "mcart_item_totalcost": cart_context['products_list'][0]['item_totalcost'],
        "mcart_serviceoptions": cart_context['products_list'][0]['mcart_serviceoptions'],
        "mcart_serviceoption_total": serviceoption_total,
        "mcart_deliveryoption": mcart_deliveryoption,
        'resume_uploaded1': resume_uploaded,
        'resume_uploaded2': (str(resume_uploaded.name).split("/"))[1],
        'section_header_1': "Order Details"
    }
    template = loader.get_template(TEMPLATE_DIR + "order_details.html")
    return HttpResponse(template.render(context, request))


# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None


# def InvoicePDF(request, tracking_id):
#     zzz_print("    %-28s: %s" % ("OrderDetails", tracking_id))

#     cart_context = cart_context_forTrackingId(request, tracking_id)
#     cart_context_loggit(cart_context)

#     mcart_instance = cart_context['products_list'][0]['mcart']

#     serviceoption_total = 0
#     for serviceoption in cart_context['products_list'][0]['mcart_serviceoptions']:
#         serviceoption_total += serviceoption.price
#     zzz_print("    %-28s: %s" % ("serviceoption_total", serviceoption_total))

#     resume_uploaded = ""
#     if cart_context['resume_required']:
#         imcart_fileupload = mcart_fileupload.objects.get(
#             mcompleted_purchase=mcart_instance.mcompleted_purchase)
#         resume_uploaded = imcart_fileupload.document

#     mcart_deliveryoption = None
#     if len(cart_context['products_list'][0]['mcart_deliveryoptions']):
#         mcart_deliveryoption = cart_context['products_list'][0]['mcart_deliveryoptions'][0]

#     context = {
#         "mcart_instance": mcart_instance,
#         "mcart_item_totalcost": cart_context['products_list'][0]['item_totalcost'],
#         "mcart_serviceoptions": cart_context['products_list'][0]['mcart_serviceoptions'],
#         "mcart_serviceoption_total": serviceoption_total,
#         "mcart_deliveryoption": mcart_deliveryoption,
#         'resume_uploaded': resume_uploaded,
#         'section_header_1': "Order Details"
#     }


#     # template = loader.get_template("prof_candidate/components/invoice_pdf.html")

#     pdf = render_to_pdf('prof_candidate/components/invoice_pdf.html', context)

#     # return HttpResponse(template.render(context, request))
#     return HttpResponse(pdf, content_type='application/pdf')

import mimetypes
from docx.document import Document
import docx
# def DownloadMyResume(request, filename):
#     filename = 'Jenkins_CI_Ia.doc'
#     filepath = '/Users/zoti01011989/ZotisDrive/media/resume-cart/' + filename
#     # path = open(filepath, 'r')
#     # # Set the mime type
#     # mime_type, _ = mimetypes.guess_type(filepath)
#     # # Set the return value of the HttpResponse
#     # response = HttpResponse(path, content_type=mime_type)
#     # # Set the HTTP header for sending to browser
#     # response['Content-Disposition'] = "attachment; filename=%s" % filename    

#     document = Document()
#     document.save(filename)    
#     return HttpResponse("im fine")


def DownloadMyResume(request, filename):
    filename = 'JRW-for-Python-Developer-(003).docx'
    filepath = '/Users/zoti01011989/ZotisDrive/media/resume-cart/' + filename
    print('SLA FILE: ', filepath)
    if os.path.exists(filepath):
        with open(filepath, 'rb') as worddoc: # read as binary
            content = worddoc.read() # Read the file
            response = HttpResponse(
                content,
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = 'attachment; filename=download_filename.docx'
            response['Content-Length'] = len(content) #calculate length of content
            return response
    else:
        return HttpResponse("Failed to Download SLA")

# # Import mimetypes module
# import mimetypes
# # import os module
# import os
# # Import HttpResponse module
# from django.http.response import HttpResponse


# def download_file(request):
#     # Define Django project base directory
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     # Define text file name
#     filename = 'test.txt'
#     # Define the full file path
#     filepath = BASE_DIR + '/downloadapp/Files/' + filename
#     # Open the file for reading content
#     path = open(filepath, 'r')
#     # Set the mime type
#     mime_type, _ = mimetypes.guess_type(filepath)
#     # Set the return value of the HttpResponse
#     response = HttpResponse(path, content_type=mime_type)
#     # Set the HTTP header for sending to browser
#     response['Content-Disposition'] = "attachment; filename=%s" % filename
#     # Return the response value
#     return response
