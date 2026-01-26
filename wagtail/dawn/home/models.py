from wagtail.images.models import Image
from django.db import models

from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.embeds.models import Embed  
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from shared.blocks import ServiceItemBlock
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

# Form fields
class ContactFormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )


class HomePage(Page):
    parralax_Subtitle = models.CharField(blank=True, max_length=50)
    parralax_Title = models.CharField(blank=True, max_length=50)
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
    about_Title = models.CharField(blank=True, max_length=50)
    about_Description = models.TextField(blank=True)
    about_ButtonLink = models.CharField(null=True, blank=True, max_length=50)
    about_ButtonText = models.CharField(null=True, max_length=20)

    services_title = models.CharField(blank=True, max_length=50)
    services_list = StreamField(
        [
            ("service", ServiceItemBlock()),
        ],
        blank=True,
        use_json_field=True,
    )
    
    portfolio_one_Subtitle = models.CharField(blank=True, max_length=50)
    portfolio_one_Title = models.CharField(blank=True, max_length=50)
    portfolio_one_Description = models.TextField(blank=True)
    portfolio_one_ButtonLink = models.CharField(null=True, blank=True, max_length=50)
    portfolio_one_ButtonText = models.CharField(null=True, max_length=20)
    
    portfolio_two_Subtitle = models.CharField(blank=True, max_length=50)
    portfolio_two_Title = models.CharField(blank=True, max_length=50)
    portfolio_two_Description = models.TextField(blank=True)
    portfolio_two_ButtonLink = models.CharField(null=True, blank=True, max_length=50)
    portfolio_two_ButtonText = models.CharField(null=True, max_length=20)
    
    portfolio_three_Subtitle = models.CharField(blank=True, max_length=50)
    portfolio_three_Title = models.CharField(blank=True, max_length=50)
    portfolio_three_Description = models.TextField(blank=True)
    portfolio_three_ButtonLink = models.CharField(null=True, blank=True, max_length=50)
    portfolio_three_ButtonText = models.CharField(null=True, max_length=20)
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("parralax_Subtitle"),
            FieldPanel("parralax_Title"),
            FieldPanel("parralax_ButtonLink"),
            FieldPanel("parralax_ButtonText"),
            FieldPanel("parralax_Video"),
        ], heading="Parralax Section"),
        MultiFieldPanel([
            FieldPanel("services_list"),
            FieldPanel("services_title"),
        ], heading="Services Section"),
        MultiFieldPanel([
            FieldPanel("about_Subtitle"),
            FieldPanel("about_Title"),
            FieldPanel("about_Description"),
            FieldPanel("about_ButtonLink"),
            FieldPanel("about_ButtonText"),
        ], heading="About Section"),
        MultiFieldPanel([
            FieldPanel("portfolio_one_Subtitle"),
            FieldPanel("portfolio_one_Title"),
            FieldPanel("portfolio_one_Description"),
            FieldPanel("portfolio_one_ButtonLink"),
            FieldPanel("portfolio_one_ButtonText"),
        ], heading="Portfolio One Section"),
        MultiFieldPanel([
            FieldPanel("portfolio_two_Subtitle"),
            FieldPanel("portfolio_two_Title"),
            FieldPanel("portfolio_two_Description"),
            FieldPanel("portfolio_two_ButtonLink"),
            FieldPanel("portfolio_two_ButtonText"),
        ], heading="Portfolio Two Section"),
        MultiFieldPanel([
            FieldPanel("portfolio_three_Subtitle"),
            FieldPanel("portfolio_three_Title"),
            FieldPanel("portfolio_three_Description"),
            FieldPanel("portfolio_three_ButtonLink"),
            FieldPanel("portfolio_three_ButtonText"),
        ], heading="Portfolio Three Section"),
    ]
    
# FAQ block for StreamField
class FAQBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    text = blocks.RichTextBlock()

# Main contact page
class ContactPage(AbstractEmailForm):
    contact_Title = models.CharField(max_length=50, blank=True)
    contact_Subtitle = models.CharField(max_length=150, blank=True)
    form_Title = models.CharField(max_length=50, blank=True)
    form_Subtitle = RichTextField(blank=True)
    
    FAQ_Section = StreamField(
        [
            ("faq", FAQBlock()),
        ],
        use_json_field=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('contact_Title'),
        FieldPanel('contact_Subtitle'),
        FieldPanel('form_Title'),
        FieldPanel('form_Subtitle'),
        InlinePanel('form_fields', label="Form Fields"),
        FieldPanel('FAQ_Section'),
    ]    
    # include the default panels from AbstractEmailForm for email & thank-you
    promote_panels = AbstractEmailForm.promote_panels
    settings_panels = AbstractEmailForm.settings_panels

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