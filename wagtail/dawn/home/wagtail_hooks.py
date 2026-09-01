from wagtail import hooks
from django.utils.safestring import mark_safe
from django.templatetags.static import static


@hooks.register("insert_global_admin_css")
def global_admin_css():
    font_link = (
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        "family=Epilogue:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400"
        '&display=swap">'
    )
    css_link = f'<link rel="stylesheet" href="{static("css/wagtail_admin.css")}">'
    return mark_safe(font_link + css_link)
