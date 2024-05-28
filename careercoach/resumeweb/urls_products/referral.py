from django.urls import path
from django.conf.urls import url, include


from ..views.products import (
    # referral
    ReferralHome,
    ReferralHowItWorks,
    ReferralHowToSubmit,
    ReferralCheckElig,
    ReferralOpenPositions,
    ReferralRequestByGuest,
    ReferralRequestSubmitConf,
    SubmitRequestAs,
    ReferralTermsCond,
    ReferralAppChecklist,
    ReferralPreparedness,
    ReferralFAQ,
    ReferralUseCases,
    ReferralCompareThis,
    ReferralProductDeliveryMethods,
)



# referral
referral_urls = [
    path(
        "home", 
        ReferralHome.as_view(), 
        name="referral_home"
    ),
    path(
        "request/create", 
        ReferralRequestByGuest.as_view(), 
        name="referral_submit_req_now"
    ),
    path("request/submit-confirmation/<int:id>/<str:token>",
        ReferralRequestSubmitConf.as_view(),
        name="referral_req_sub_conf"
    ),



    # about the service pages 
    path(
        "how-to-submit", 
        ReferralHowToSubmit.as_view(), 
        name="referral_how_to_sub_req"
    ),
    path(
        "check-eligibility", 
        ReferralCheckElig.as_view(), 
        name="referral_eligibility"
    ),
    path(
        "guest-or-candidate", 
        SubmitRequestAs.as_view(), 
        name="check_if_cand"
    ),
    path(
        "open-positions", 
        ReferralOpenPositions.as_view(), 
        name="referral_pos_list"
    ),
    path(
        "terms-conditions", 
        ReferralTermsCond.as_view(), 
        name="referral_terms_cond"
    ),
    path(
        "app-checklist", 
        ReferralAppChecklist.as_view(), 
        name="referral_app_checklist"
    ),




    # prod insight pages 
    path(
        "use-cases", 
        ReferralUseCases.as_view(), 
        name="referral_use_cases"
    ),
    path("product-comparison",
        ReferralCompareThis.as_view(), 
        name="referral_compare_this"
    ),
    path(
        "how-it-works", 
        ReferralHowItWorks.as_view(), 
        name="referral_how_it_works"
    ),
    path(
        "faq", 
        ReferralFAQ.as_view(), 
        name="referral_faq"
        ),
    path(
        "product-delivery-methods", 
        ReferralProductDeliveryMethods.as_view(), 
        name="referral_del_meths"
    ),
]
