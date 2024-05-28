from zzz_lib.zzz_log import zzz_print
from django.contrib import admin
from django import forms

from resumeweb.models import (
    mprod_exp180,
    mprod_exp180_serviceoption,

)


from resumeweb.models import (
    mprod_intprep,
    mprod_intprep_catlist,
    mprod_intprep_serviceoption,

)


from resumeweb.models import (
    mprod_proflevel,
    mprod_proflevel_list,
    mprod_proflevel_serviceoption,
)


from resumeweb.models import (
    mprod_proglang,
    mprod_proglang_list,
    mprod_proglang_serviceoption,

)


from resumeweb.models import (
    mprod_rolebased,
    mprod_rolebased_list,
    mprod_rolebased_serviceoption,

)



from resumeweb.models import (
    mprod_strategy,
    mprod_strategy_taglist,
    mprod_strategy_serviceoption,    

)



from resumeweb.models import (
    mprod_visabased,
    mprod_visabased_list,
    mprod_visabased_serviceoption,


)


from resumeweb.models import (

    mprod_exp180_deliveryoption,
    mprod_intprep_deliveryoption,
    mprod_proflevel_deliveryoption,
    mprod_proglang_deliveryoption,
    mprod_rolebased_deliveryoption,
    mprod_strategy_deliveryoption,
    mprod_visabased_deliveryoption,


)






# mprod_visabased_list
########################################################################################
@admin.register(mprod_visabased_list)
class Admin_USVISA_CAT_LIST(admin.ModelAdmin):
    list_display = (
        "visaname",
    )



# usvisa serv list
########################################################################################
@admin.register(mprod_visabased)
class Admin_USVISA_SERV_LIST(admin.ModelAdmin):
    list_display = (
        "sku",
        "title",
        "deliverables",
        "category",
        "golivestatus",
        "trending",
        "homepage_showup"
    )
    # Fields to exclude from add/edit Admin Form
    exclude = ('sku',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(Admin_USVISA_SERV_LIST, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'description' or db_field.name == 'title':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield




## service options
## *****************************************************************************************
@admin.register(mprod_visabased_serviceoption)
class AdminUSvisaServiceoption(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "listprice",
        "price",
        'products'
    )
    # Fields to exclude from add/edit Admin Form
    exclude = ('sku',)


    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(AdminUSvisaServiceoption, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'description' or db_field.name == 'name':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield






## delivery options
## *****************************************************************************************
@admin.register(mprod_visabased_deliveryoption)
class admin_mprod_visabased_deliveryoption(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "listprice",
        "price",
        "hours_to_cancel_after_payment",
        "hours_to_deliver_after_payment",
    )
    # Fields to exclude from add/edit Admin Form
    exclude = ('sku',)


    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(admin_mprod_visabased_deliveryoption, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'description' or db_field.name == 'name':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


        