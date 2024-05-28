from unicodedata import category
from zzz_lib.zzz_log import zzz_print
from django.db import models
from .mbase_prod import mbase_prod
from .. import const_resumeweb
from .mprod_proglang_list import mprod_proglang_list

# ******************************************************************************
class mprod_proglang(mbase_prod):
    # Note: fields listprice, saleprice and sku defined in parent classes
    title = models.CharField(max_length=500, unique=True)    
    description = models.TextField(blank=False, null=False)
    deliverables = models.TextField(blank=True, null=True)
    golivestatus = models.CharField(max_length=20,
                                choices=const_resumeweb.GOLIVE_STATUS,
                                default='draft'
                            )

    trending = models.CharField(max_length=10,
                                choices=const_resumeweb.TRENDING,
                                default='no'
                            )
    homepage_showup = models.CharField(max_length=20,
                                choices=const_resumeweb.HOMEPAGE_SHOWUP,
                                default='no'
                            )
    category = models.ForeignKey(mprod_proglang_list, on_delete=models.CASCADE)                            
    
    class_threeletterprefix = "dlc"

    class Meta:
        verbose_name_plural = "05-Dialect-services"

    def __str__(self):
        return f'{self.sku}, {self.category}, {self.title}'

    # # --------------------------------------------------------------------------
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)






