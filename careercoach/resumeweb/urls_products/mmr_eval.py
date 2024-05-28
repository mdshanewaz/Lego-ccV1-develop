#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from django.conf.urls import url, include

from ..views.products import (
    EvalHome,
    EvalSearch,
    EvalHowItWorks,
    EvalCompareThis,
    EvalUsefulness,
    EvalFAQ,
    EvalDeliverablesInfo,
    EvalServiceAll,
    EvalDetailView_ajax,
    EvalDetailView,
)

mmr_eval_urls = [
    path("home",                        EvalHome.as_view(),                 name="eval_homepg_url"),
    path("search",                      EvalSearch.as_view(),               name="eval-search"),

    path("how-it-works",                EvalHowItWorks.as_view(),           name="eval_how_it_works"),
    path("compare-this",                EvalCompareThis.as_view(),          name="eval_compare_this"),
    path("use-cases",                  EvalUsefulness.as_view(),           name="eval_usefulness"),
    path("faq",                         EvalFAQ.as_view(),                  name="eval_faq"),
    path("product-delivery-methods",           EvalDeliverablesInfo.as_view(),     name="eval_deliverablesinfo"),
    path("all",                         EvalServiceAll.as_view(),           name="eval_all_services"),
    path("product-details/<int:id>",    EvalDetailView,                     name="eval_detail_view_link"),
]
