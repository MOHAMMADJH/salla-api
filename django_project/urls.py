from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from accounts.views import SallaOAuthView, SallaOAuthCallbackView, SallaOAuthSuccessView, SallaOAuthErrorView, \
    SallaAuthorizationView, SallaCallbackView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("pages.urls")),
    path('webhooks/', include('webhook_app.urls')),  # Include webhook URLs

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path("__debug__/", include(debug_toolbar.urls)),
                      path('salla/oauth/', SallaOAuthView.as_view(), name='salla-oauth'),
                      path('salla/oauth/callback/', SallaOAuthCallbackView.as_view(), name='salla-oauth-callback'),
                      path('salla/oauth/success/', SallaOAuthSuccessView.as_view(), name='salla-oauth-success'),
                      path('salla/oauth/error/', SallaOAuthErrorView.as_view(), name='salla-oauth-error'),
                      path('new/salla/oauth/', SallaAuthorizationView.as_view(), name='authorize_salla'),
                      path('new/salla/oauth/callback/', SallaCallbackView.as_view(), name='salla_callback'),
                      # path('new/salla/oauth/refresh/', refresh_token, name='refresh_token'),

                  ] + urlpatterns
