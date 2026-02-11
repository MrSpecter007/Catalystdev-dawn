from wagtail.models import Locale, Page, Site
from .models import MainMenu

def main_menu(request):
    """
    Provides main menu and page translations for the language switcher.
    Fallbacks to the first page under root if current_page is missing.
    """

    # Get current page
    page = getattr(request, "current_page", None)

    # Fallback to first page under root (homepage)
    if not page:
        page = Page.objects.filter(depth=2).first()  # depth=2 = first real page under root

    # Get locales
    locales = Locale.objects.all()

    # Build translations dict: list of {locale, page}
    page_translations = []
    for locale in locales:
        if page:
            # get translation or fallback to the page itself
            translated = page.get_translation_or_none(locale)
            page_translations.append({
                "locale": locale,
                "page": translated if translated else page,
            })

    return {
        "main_menu": MainMenu.objects.first(),
        "page_translations": page_translations,
        "debug_page": page,  # optional for debugging
        "locales": locales,
    }

def footer(request):
    site = Site.find_for_request(request)

    footer = getattr(site, "footer", None)

    return {
        "footer": footer,
    }