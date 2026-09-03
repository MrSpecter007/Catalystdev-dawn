from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.views.static import serve as serve_static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.conf.urls.i18n import i18n_patterns

from search import views as search_views
from portfolio import views as portfolio_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    # Caddy forward_auth endpoint — must be outside i18n_patterns so it is
    # always reachable regardless of Accept-Language. Admin sessions are
    # validated here before Caddy proxies any request to a showroom.
    path("forward-auth/showrooms/", portfolio_views.forward_auth_showrooms, name="forward_auth_showrooms"),
    path("portal/gate/", portfolio_views.portal_gate, name="portal_gate"),
    path("portal/set/", portfolio_views.portal_set, name="portal_set"),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()

# Serve uploaded media files in all environments.
# static() returns [] when DEBUG=False, so register the serve view directly.
urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve_static, {"document_root": settings.MEDIA_ROOT}),
]

urlpatterns += i18n_patterns(
    path("", include(wagtail_urls)),
    prefix_default_language=False,
)


