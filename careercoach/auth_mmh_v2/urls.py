from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import reverse_lazy

from .forms import (
    SetPasswordCustomForm,
    MySetPasswordForm,
)

from .views import (

    mmh_auth_login_request,
    mmh_auth_logout_request,
    mmh_auth_register,
    mmh_auth_signup_validation_conf,
    mmh_auth_verify,
    password_reset_request_view,
    PasswordResetRequestEmailConfirmationWithLinkView,
    PasswordResetSetNewPasswordView,
    
)


app_name = 'auth_mmh_v2'


# signin 
# --------------------------------------------------------------
signin_urls = [
    path("signin",                          
        mmh_auth_login_request,             
        name="mmh_auth_login_request"
    ),

    path("logout",                          
        mmh_auth_logout_request,            
        name="mmh_auth_logout_request"
    ),

]



# signup 
# --------------------------------------------------------------
signup_urls = [
    path("signup",                       
        mmh_auth_register,                  
        name="mmh_auth_register_url"
    ),

    path("signup-complete/thanks",                 
        mmh_auth_signup_validation_conf,    
        name="signup_validation_temphold"
    ),

    path("verify/<str:activation_code>",    
        mmh_auth_verify,                    
        name="mmh_auth_verify"
    ),

]



# password reset 
# --------------------------------------------------------------
password_reset_urls = [    
    path(
        "password-reset",
            password_reset_request_view,
            name="password_reset"
        ),

    # path(
    #     "password-reset-done",
    #         auth_views.PasswordResetDoneView.as_view(
    #             template_name='auth_mmh_v2/layout/password_reset/step2_done.html'
    #             ),
    #         name="password_reset_done"
    #     ),

    path(
        "password-reset-done",
            PasswordResetRequestEmailConfirmationWithLinkView.as_view(),
            name="password_reset_done"
        ),
    
    # path(
    #     "password-reset-confirm/<str:uidb64>/<str:token>",
    #         auth_views.PasswordResetConfirmView.as_view(
    #             template_name='auth_mmh_v2/layout/password_reset/step3_set_password.html',
    #             success_url=reverse_lazy('auth_mmh_v2:password_reset_complete'),
    #             form_class=SetPasswordCustomForm
    #             ),
    #         name="password_reset_confirm"
    #     ),
    
    path(
        "password-reset-confirm/<str:uidb64>/<str:token>",
            PasswordResetSetNewPasswordView.as_view(),
            name="password_reset_confirm"
        ),


    path(
        "password-reset-complete/",
            auth_views.PasswordResetCompleteView.as_view(
                template_name='auth_mmh_v2/layout/password_reset/step4_complete.html',
                ),
            name="password_reset_complete"
        ),

]







urlpatterns = [
    path("", include(signin_urls)),
    path("", include(signup_urls)),
    path("", include(password_reset_urls)),
    
    # update/change password urls
    # path('password-update/', auth_views.PasswordChangeView.as_view(), name='update-password'),
    # path('password-update/done/',auth_views.PasswordChangeDoneView.as_view(), name='update-password-done'),


]
