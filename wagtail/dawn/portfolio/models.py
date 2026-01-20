from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag

from wagtail import blocks
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import StructBlock, ChoiceBlock, URLBlock
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.blocks import PageChooserBlock

from .forms import PlaceholderFormBuilder


# ---------------------------
# TAGGING
# ---------------------------
class ProjectPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "portfolio.ProjectPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


# ---------------------------
# GALLERY BLOCK
# ---------------------------
class GalleryItemBlock(StructBlock):
    media_type = ChoiceBlock(
        choices=[
            ("image", "Image"),
            ("video", "Video"),
        ],
        default="image",
        required=True,
    )
    image = ImageChooserBlock(required=False)
    video_url = URLBlock(required=False, help_text="YouTube/Vimeo URL or MP4 link")

    class Meta:
        icon = "image"
        label = "Gallery Item"


# ---------------------------
# PORTFOLIO PAGES
# ---------------------------
class PortfolioIndexPage(Page):
    portfolio_title = models.CharField(max_length=250, blank=True)
    portfolio_subtitle = models.CharField(max_length=250, blank=True)

    template = "portfolio/portfolioindexpage.html"
    subpage_types = ["portfolio.ProjectPage"]

    content_panels = Page.content_panels + [
        FieldPanel("portfolio_title"),
        FieldPanel("portfolio_subtitle"),
    ]

    def get_projects(self):
        return (
            ProjectPage.objects
            .child_of(self)
            .live()
            .select_related("hero_image")
        )
    
    def get_tags(self):
        return (
           Tag.objects
            .filter(
                portfolio_projectpagetag_items__content_object__path__startswith=self.path
            )
            .distinct()
        )


class ProjectPage(Page):
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    subtitle = RichTextField(blank=True)
    description = RichTextField(blank=True)
    project_requirement = RichTextField(blank=True)
    project_result = RichTextField(blank=True)

    client = RichTextField(blank=True)
    start_date = RichTextField(blank=True)
    end_date = RichTextField(blank=True)
    single_date = RichTextField(blank=True)
    website = RichTextField(blank=True)
    
    tags = ClusterTaggableManager(
        through=ProjectPageTag,
        blank=True,
        help_text="Project categories (branding, design, interactive, etc.)",
    )

    # Gallery as StreamField
    gallery = StreamField(
        [("gallery_item", GalleryItemBlock())],
        blank=True,
        use_json_field=True,
    )

    
    parent_page_types = ["portfolio.PortfolioIndexPage"]

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("subtitle"),
        FieldPanel("description"),
        FieldPanel("project_requirement"),
        FieldPanel("project_result"),
        MultiFieldPanel(
            [
                FieldPanel("client"),
                FieldPanel("start_date"),
                FieldPanel("end_date"),
                FieldPanel("single_date"),
                FieldPanel("website"),
            ],
            heading="Project Info",
        ),
        FieldPanel("gallery"),
        FieldPanel("tags")
    ]


# ---------------------------
# SERVICE PAGES
# ---------------------------
class ServiceIndexPage(Page):
    intro = RichTextField(blank=True)

    template = "portfolio/serviceindexpage.html"
    subpage_types = ["portfolio.ServicePage"]

    content_panels = Page.content_panels + [FieldPanel("intro")]

class ServiceItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    description = blocks.RichTextBlock(required=True)

    class Meta:
        icon = "list-ul"
        label = "Service Item"


class FAQBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    text = blocks.RichTextBlock(required=True)

    class Meta:
        icon = "help"
        label = "FAQ Item"
        
class ServicePage(Page):
    # Hero
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    service_title = models.CharField(max_length=255, blank=True)
    service_subtitle = models.CharField(max_length=255, blank=True)
    service_tagline = models.CharField(max_length=255, blank=True)

    # Main content
    service_description = RichTextField(blank=True)

    services = StreamField(
        [
            ("service", ServiceItemBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    # FAQ
    service_FAQ_tagline = models.CharField(max_length=255, blank=True)
    service_FAQ_Section = StreamField(
        [
            ("faq", FAQBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    # Conclusion
    service_conclusion_title = models.CharField(max_length=255, blank=True)
    service_conclusion_description = RichTextField(blank=True)

    template = "portfolio/servicepage.html"
    parent_page_types = ["portfolio.ServiceIndexPage"]

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("service_title"),
        FieldPanel("service_subtitle"),
        FieldPanel("service_tagline"),
        FieldPanel("service_description"),
        FieldPanel("services"),
        MultiFieldPanel(
            [
                FieldPanel("service_FAQ_tagline"),
                FieldPanel("service_FAQ_Section"),
            ],
            heading="FAQ",
        ),
        MultiFieldPanel(
            [
                FieldPanel("service_conclusion_title"),
                FieldPanel("service_conclusion_description"),
            ],
            heading="Conclusion",
        ),
    ]



# ---------------------------
# CONTACT FORM
# ---------------------------
class ContactFormField(AbstractFormField):
    page = ParentalKey(
        "ContactFormPage", on_delete=models.CASCADE, related_name="form_fields"
    )


class ContactFormPage(AbstractEmailForm):
    form_builder = PlaceholderFormBuilder
    heading = models.CharField(max_length=255)
    intro = RichTextField(blank=True)

    template = "portfolio/contactformpage.html"

    content_panels = Page.content_panels + [
        FieldPanel("heading"),
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Form fields"),
        MultiFieldPanel(
            [
                FieldPanel("to_address"),
                FieldPanel("from_address"),
                FieldPanel("subject"),
            ],
            heading="Email settings",
        ),
    ]


class FormEmbedBlock(blocks.StructBlock):
    form_page = PageChooserBlock(
        target_model="portfolio.ContactFormPage", required=True
    )

    class Meta:
        template = "blocks/form_embed.html"
        icon = "form"
