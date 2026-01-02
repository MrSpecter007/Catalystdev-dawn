from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

class HomePage(Page):
    hero_title = RichTextField(blank=True)
    hero_subtitle = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
    ]
    
class Portfolio(Page):
    portfolio_title = RichTextField(blank=True)
    portfolio_subtitle = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("portfolio_title"),
        FieldPanel("portfolio_subtitle"),
    ]
    

