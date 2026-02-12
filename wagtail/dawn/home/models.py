from wagtail.images.models import Image
from django.db import models


from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.embeds.models import Embed  
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from shared.blocks import ServiceItemBlock
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField
)

class ContactFormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields'
    )
    
# FAQ block for StreamField
class FAQBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    text = blocks.RichTextBlock()


class ContactPage(AbstractEmailForm):

    contact_Title = models.CharField(max_length=50, blank=True)
    contact_Subtitle = models.CharField(max_length=150, blank=True)
    form_Title = models.CharField(max_length=50, blank=True)
    form_Subtitle = RichTextField(blank=True)
    btn_Text = models.CharField(max_length=20, blank=True)
    box_title = models.CharField(max_length=50, blank=True)
    box_city = models.CharField(max_length=50, blank=True)
    box_address = models.CharField(max_length=100, blank=True)
    faq_title = models.CharField(max_length=50, blank=True)
    faq_subtitle = models.CharField(max_length=150, blank=True)
    breadcrumb_home = models.CharField(max_length=150, blank=True)
    breadcrumb_contact = models.CharField(max_length=150, blank=True)
    form_thank_you_text = models.CharField(max_length=150, blank=True)
    form_other_message_text = models.CharField(max_length=150, blank=True)
    
    FAQ_Section = StreamField(
        [
            ("faq", FAQBlock()),
        ],
        use_json_field=True,
        blank=True
    )
    intro = models.TextField(blank=True)
    thank_you_text = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        FieldPanel('contact_Title'),
        FieldPanel('contact_Subtitle'),
        FieldPanel('form_Title'),
        FieldPanel('form_Subtitle'),
        FieldPanel('btn_Text'),
        FieldPanel('box_title'),
        FieldPanel('box_city'),
        FieldPanel('box_address'),
        FieldPanel('breadcrumb_home'),
        FieldPanel('breadcrumb_contact'),
        FieldPanel('form_thank_you_text'),
        FieldPanel('form_other_message_text'),
        FieldPanel('faq_title'),
        FieldPanel('faq_subtitle'),
        FieldPanel('FAQ_Section', classname="full"),
        MultiFieldPanel([
            FieldPanel('from_address'),
            FieldPanel('to_address'),
            FieldPanel('subject'),
        ], heading="Email settings"),
    ]


class HomePage(Page):
    parralax_Subtitle = models.CharField(blank=True, max_length=50)
    parralax_Title = models.CharField(blank=True, max_length=50)
    parralax_ButtonLink = models.CharField(null=True, blank=True, max_length=50)
    parralax_ButtonText = models.CharField(null=True, max_length=20)
    parralax_Video = models.FileField(
        upload_to='videos/',
        blank=True,
        null=True
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
    
    contact_title = models.CharField(blank=True, max_length=50)
    contact_subtitle = models.CharField(blank=True, max_length=150)
    contact_email = models.EmailField(blank=True)
    contact_address = models.CharField(blank=True, max_length=200)
    contact_button_text = models.CharField(blank=True, max_length=20)
    
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
        MultiFieldPanel([
            FieldPanel("contact_title"),
            FieldPanel("contact_subtitle"),
            FieldPanel("contact_email"),
            FieldPanel("contact_address"),
            FieldPanel("contact_button_text"),
        ], heading="Contact Section"),
    ]

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
    breadcrumb_home = models.CharField(max_length=150, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("about_sub_title"),
        FieldPanel("about_text"),
        FieldPanel("breadcrumb_home"),
    ]
    class Meta:
        verbose_name = "About Page"