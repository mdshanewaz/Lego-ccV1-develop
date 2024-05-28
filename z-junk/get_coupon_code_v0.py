from resumeweb.models import (mcoupon, mcoupon_given,)
from zzz_lib.zzz_log import zzz_print
from django.http import HttpResponse, HttpResponseRedirect
import requests

import logging
logger = logging.getLogger(__name__)



def generate_coupon(product_liked):
    # Find best active mcoupon instance for this product liked
    imcoupon = mcoupon.objects\
        .filter(product_liked=product_liked, active=True)\
        .order_by('-discount_percent')\
        .first()
    print('--------------------------------------------------------------------------')
    print('value of imcoupon>>>{}'.format(imcoupon))
    print('--------------------------------------------------------------------------')

    logger.warning("line20>>>'value of imcoupon>>>{}'.format(imcoupon)")


    if not imcoupon:
        # zzz_print("    %-28s: %s" % ("selected product is doesnot offer any coupon", form.cleaned_data["product_liked"]))
        # redirect user to page thanking them for their feedback
        return HttpResponse('someting is wrong')


    else:
        # zzz_print("   %s " % ("ACTIVE MCOUPON FOUND"))

        # Generate mcoupon_given instance for it
        imcoupon_given = mcoupon_given.objects.mcoupon_given_add(request=requests, mcoupon=imcoupon)
        
        context = {
            'coupon_code'     	: imcoupon.product_liked,
            'discount_percent'  : imcoupon.discount_percent,
            'hours_to_expire'   : imcoupon.hours_to_expire,
            'random_string_32'  : imcoupon_given.random_string_32,
            'email_address'     : email_add_given,
        }

    return context
