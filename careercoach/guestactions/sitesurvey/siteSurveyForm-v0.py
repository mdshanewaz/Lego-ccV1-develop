from django import forms
from resumeweb.models import SiteSurvey
from ..validators import validate_email_guest
from django.utils.translation import ugettext_lazy as _

########## FROM STYLE
TEXT_AREA_STYLE = {
    'row': 5,
    'cols': 10,
    'class': 'form-control form-control-xs rounded-0'
}
TEXT_INPUT_STYLE = {
    'class': 'form-control form-control-xs rounded-0'
}

HMPG_RATINGS = (
    ("excellent", "Excellent"),
    ("Good", "Good"),
    ("bad", "Didnot like it"),
)

USRFRNDLY_RATINGS = (
    ("veryfriendly", "Very Friendly"),
    ("ok", "It's Ok"),
    ("notfriendly", "Not user friendly at all"),
)

PROMO_RATINGS = (
    ("Yes", "Yes"),
    ("No", "No")
)

SERVICE_RATINGS = (
    ("excellent", "Excellent"),
    ("Good", "Good"),
    ("Bad", "Didnot like it"),    

)

OVERALL_RATINGS = (
    ("excellent", "Excellent"),
    ("Good", "Good"),
    ("bad", "Didnot like it"), 
)

CONSENTS = (
    ("Yes", "Yes"),
    ("No", "No")
    
)

class SiteSurveyForm(forms.ModelForm):
    site_used       = forms.ChoiceField(label="Have you made any purchase yet?",choices=CONSENTS,widget=forms.RadioSelect)
    hmpg_design     = forms.ChoiceField(label="What do you feel about our site homepage design?",choices=HMPG_RATINGS,widget=forms.RadioSelect)
    userfriendly    = forms.ChoiceField(label="How user-friendly the site is?",choices=USRFRNDLY_RATINGS,widget=forms.RadioSelect)
    promo_offers    = forms.ChoiceField(label="Have you used any promo offer yet?",choices=PROMO_RATINGS,widget=forms.RadioSelect)
    service_lineup  = forms.ChoiceField(label="What do you think about our service lines?",choices=SERVICE_RATINGS,widget=forms.RadioSelect)
    overall_exp     = forms.ChoiceField(label="How satisfied are you with overall experience?",choices=OVERALL_RATINGS,widget=forms.RadioSelect)
    recommend       = forms.ChoiceField(label="Will you recommend us to your friends?", choices=CONSENTS,widget=forms.RadioSelect)
    message         = forms.CharField(widget = forms.Textarea())
    name            = forms.CharField()
    email           = forms.EmailField(
        max_length = 200,
        label = "Contact Email",
        help_text=_("<small style='color: grey'>we never share your email address with any 3rd party</small>"),
        widget = forms.TextInput(
            attrs = TEXT_INPUT_STYLE
        ),
        error_messages = {
            'invalid': _(u''),
        },
        validators=[validate_email_guest]
    )

    class Meta:
        model = SiteSurvey
        fields = '__all__'
        exclude = ('created_at',)
