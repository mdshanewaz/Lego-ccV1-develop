from pprint import pprint
from itertools import chain
from datetime import datetime
from itertools import chain

from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from zzz_lib.zzz_log import zzz_print

from resumeweb.models import (
    mfeedback, 
    mcoupon, 
    mcoupon_given,
    msendmail
)

from ...models import (
    mprod_exp180,
    mprod_intprep,
    mprod_proglang,
    mprod_rolebased,
    mprod_proflevel,
    mprod_visabased,
    mprod_strategy,
    ProductFaq,
    SearchQueryGuest,
    SearchQueryGuest,
)

# from haystack.query import SearchQuerySet 

from ...forms import (
    GlobalSearchForm,
)

TEMP_DIR_GENERAL = 'resumeweb/layout/general/'

import logging
logger = logging.getLogger(__name__)



class GlobalSearchResultsView(ListView):
    template_name = TEMP_DIR_GENERAL+'search-global-v2.html'
    paginate_by = 20
    count = 0

    def get_queryset(self):
        query = self.request.GET.get('query_globalsearch', None)
        query_keywords_list = []

        if query is not None:
            for i in query.split(" "):
                print(query_keywords_list.append(i))

            if len(query_keywords_list) > 0:
                for i in query_keywords_list:
                    result_exp180 = mprod_exp180.objects.filter(title__icontains=i)
                    result_intprep = mprod_intprep.objects.filter(title__icontains=i)
                    result_proglang = mprod_proglang.objects.filter(title__icontains=i)
                    result_rolebased = mprod_rolebased.objects.filter(title__icontains=i)
                    result_proflevel = mprod_proflevel.objects.filter(title__icontains=i)
                    result_visabased = mprod_visabased.objects.filter(title__icontains=i)
                    result_strategy = mprod_strategy.objects.filter(title__icontains=i)
                    result_faq = ProductFaq.objects.filter(Q(ques__icontains=i)|Q(ans__icontains=i)) 

                    # combine querysets
                    queryset_chain = chain(
                            result_exp180,
                            result_intprep,
                            result_proglang,
                            result_rolebased,
                            result_proflevel,
                            result_visabased,
                            result_strategy,
                            result_faq,

                    )
                    qs = sorted(queryset_chain,
                                key=lambda instance: instance.pk,
                                reverse=True)
                    self.count = len(qs) # since qs is actually a list
                    return qs
            else:
                resultEmpty = "result is empty"
            print("query from line96>>>{}".format(query))
        else:
            resultEmpty = "result is empty"          

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('query_globalsearch')
        
        context['product_line'] = 'Search Results'
        context['pg_layout_type'] = 'Search results from all services'
        context['pg_layout_type'] = 'all_serv_list'
        return context

    # def update_search_query(self, *args, **kwargs):
    #     query = self.request.GET.get('query_globalsearch', None)
    #     obj, created = SearchQueryGuest.objects.get_or_create(
    #         query = query,
    #         defaults = {'created':datetime.datatime.now()},
            
    #     )
    #     obj.save()


# class SearchTerms(models.Model):
#   search_terms = models.CharField(max_length=255, blank=True, null=True)
#   total_searches = models.IntegerField(default=0)
#   updated_on = models.DateTimeField(auto_now_add=True)

#   search_objects = SearchTermManager()

#   class Meta:
#     verbose_name_plural = "Search Terms"

#   def __str__(self):
#     return self.search_terms    
