from django.db import models

from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.embeds.models import Embed  
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel


class HomePage(Page):
    parralax_Subtitle = models.CharField(blank=True, max_length=50)
    parralax_Title = models.CharField(blank=True,max_length=50)
    parralax_ButtonLink = models.CharField(null=True, blank=True, max_length=50)
    parralax_ButtonText = models.CharField(null=True, max_length=20)
    parralax_Video = models.ForeignKey(
        Embed,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    about_Subtitle = models.CharField(blank=True, max_length=50)
    about_Title = models.CharField(blank=True,max_length=50)
    about_Description = models.TextField(blank=True)
    about_ButtonLink = models.CharField(null=True, blank=True, max_length=50)
    about_ButtonText = models.CharField(null=True, max_length=20)
    portfolio_one_Subtitle = models.CharField(blank=True, max_length=50)
    portfolio_one_Title = models.CharField(blank=True,max_length=50)
    portfolio_one_Description = models.TextField(blank=True)
    portfolio_one_ButtonLink = models.CharField(null=True, blank=True, max_length=50)
    portfolio_one_ButtonText = models.CharField(null=True, max_length=20)
    portfolio_two_Subtitle = models.CharField(blank=True, max_length=50)
    portfolio_two_Title = models.CharField(blank=True,max_length=50)
    portfolio_two_Description = models.TextField(blank=True)
    portfolio_two_ButtonLink = models.CharField(null=True, blank=True, max_length=50)
    portfolio_two_ButtonText = models.CharField(null=True, max_length=20)
    portfolio_three_Subtitle = models.CharField(blank=True, max_length=50)
    portfolio_three_Title = models.CharField(blank=True,max_length=50)
    portfolio_three_Description = models.TextField(blank=True)
    portfolio_three_ButtonLink = models.CharField(null=True, blank=True, max_length=50)
    portfolio_three_ButtonText = models.CharField(null=True, max_length=20)
    
    
    content_panels = Page.content_panels + [
        MultiFieldPanel(["parralax_Subtitle", "parralax_Title", "parralax_ButtonLink", "parralax_ButtonText", "parralax_Video"], heading="Parralax Section"),
        MultiFieldPanel(["about_Subtitle", "about_Title", "about_Description", "about_ButtonLink", "about_ButtonText"], heading="About Section"),
        MultiFieldPanel(["portfolio_one_Subtitle", "portfolio_one_Title", "portfolio_one_Description", "portfolio_one_ButtonLink", "portfolio_one_ButtonText"], heading="Portfolio One Section"),
        MultiFieldPanel(["portfolio_two_Subtitle", "portfolio_two_Title", "portfolio_two_Description", "portfolio_two_ButtonLink", "portfolio_two_ButtonText"], heading="Portfolio Two Section"),
        MultiFieldPanel(["portfolio_three_Subtitle", "portfolio_three_Title", "portfolio_three_Description", "portfolio_three_ButtonLink", "portfolio_three_ButtonText"], heading="Portfolio Three Section"),
    ]
    
class ContactPage(Page):
    contact_Title = models.CharField(blank=True,max_length=50)
    contact_Subtitle = models.CharField(blank=True)
    form_Title = models.CharField(blank=True,max_length=50)
    form_Subtitle = models.CharField(blank=True)
    FAQ_Section = StreamField(
        [
            ("faq", blocks.StructBlock([
                ("title", blocks.CharBlock()),
                ("text", blocks.RichTextBlock()),
            ])),
        ],
        use_json_field=True,
        blank=True,
    )
    
    
    content_panels = Page.content_panels + ["contact_Title", "contact_Subtitle", "form_Title", "form_Subtitle", "FAQ_Section"]
    
    class LegalPage(Page):
        Legal_sub_title = models.CharField(blank=True, max_length=100)
        legal_text = RichTextField(blank=True)
        

        content_panels = Page.content_panels + [
            FieldPanel("Legal_sub_title"),
            FieldPanel("legal_text"),
        ]
    class Meta:
        verbose_name = "Legal Page"
    
    class AboutPage(Page):
        about_sub_title = models.CharField(blank=True, max_length=100)
        about_text = RichTextField(blank=True)

        content_panels = Page.content_panels + [
            FieldPanel("about_sub_title"),
            FieldPanel("about_text"),
        ]
    class Meta:
        verbose_name = "About Page"