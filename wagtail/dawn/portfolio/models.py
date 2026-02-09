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
from shared.blocks import ServiceItemBlock

from .forms import PlaceholderFormBuilder

# ---------------------------
# ABOUT PAGE SERVICE ITEM BLOCK
# ---------------------------
class AboutServiceBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    description = blocks.TextBlock(required=True)
    image = ImageChooserBlock(required=False)
    link = blocks.URLBlock(required=False)

    class Meta:
        icon = "cog"
        label = "Service"

# ---------------------------
# FAQ BLOCK
# ---------------------------
class FAQBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    text = blocks.RichTextBlock(required=True)

    class Meta:
        icon = "help"
        label = "FAQ Item"

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
# REVIEWS BLOCK
# ---------------------------        
class ReviewBlock(blocks.StructBlock):
    quote = blocks.TextBlock(required=True, help_text="The review text")
    name = blocks.CharBlock(required=True, max_length=50, help_text="Reviewer name")
    role = blocks.CharBlock(required=False, max_length=50, help_text="Reviewer role or position")
    stars = blocks.IntegerBlock(default=5, min_value=1, max_value=5, help_text="Number of stars (1-5)")
    background = ImageChooserBlock(required=False, help_text="Optional background image for this review")
    
    def get_star_lists(self, value):
        """Return filled and empty stars for template"""
        filled = range(value['stars'])
        empty = range(5 - value['stars'])
        return filled, empty

    class Meta:
        icon = "user"
        label = "Review"


# ---------------------------
# PORTFOLIO PAGES
# ---------------------------
class PortfolioIndexPage(Page):
    portfolio_title = models.CharField(max_length=250, blank=True)
    portfolio_subtitle = models.CharField(max_length=250, blank=True)
    breadcrumb_home = models.CharField(max_length=150, blank=True)
    breadcrumb_portfolio = models.CharField(max_length=150, blank=True)
    project_title = models.CharField(max_length=150, blank=True)
    project_summary = models.CharField(max_length=250, blank=True)
    date_title = models.CharField(max_length=150, blank=True)

    template = "portfolio/portfolioindexpage.html"
    subpage_types = ["portfolio.ProjectPage"]

    content_panels = Page.content_panels + [
        FieldPanel("portfolio_title"),
        FieldPanel("portfolio_subtitle"),
        FieldPanel("breadcrumb_home"),
        FieldPanel("breadcrumb_portfolio"),
        FieldPanel("project_title"),
        FieldPanel("project_summary"),
        FieldPanel("date_title"),
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
    
    reviews = StreamField([("review", ReviewBlock())], blank=True, use_json_field=True)
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
    project_result_title = models.CharField(max_length=150, blank=True)
    info_description = models.CharField(max_length=150, blank=True)
    info_requirement = models.CharField(max_length=150, blank=True)
    info_client = models.CharField(max_length=150, blank=True)
    info_industry = models.CharField(max_length=150, blank=True)
    info_services = models.CharField(max_length=150, blank=True)
    info_platforms = models.CharField(max_length=150, blank=True)
    info_date = models.CharField(max_length=150, blank=True)
    info_website = models.CharField(max_length=150, blank=True)
    btn_text = models.CharField(max_length=150, blank=True)
    

    client = models.CharField(max_length=150, blank=True)
    industry = models.CharField(max_length=150, blank=True)
    services = RichTextField(blank=True)
    platforms = RichTextField(blank=True)
    single_date = models.CharField(max_length=150, blank=True)
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
        FieldPanel("info_description"),
        FieldPanel("info_requirement"),
        FieldPanel("info_client"),
        FieldPanel("info_industry"),
        FieldPanel("info_services"),
        FieldPanel("info_platforms"),
        FieldPanel("info_date"),
        FieldPanel("info_website"),
        FieldPanel("btn_text"),
        FieldPanel("project_requirement"),
        FieldPanel("project_result"),
        FieldPanel("project_result_title"),
        FieldPanel("reviews"),
        MultiFieldPanel(
            [
                FieldPanel("client"),
                FieldPanel("industry"),
                FieldPanel("services"),
                FieldPanel("platforms"),
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
    breadcrumb_home = models.CharField(blank=True, max_length=150)
    breadcrumb_services = models.CharField(blank=True, max_length=150)
    video_link = models.URLField(blank=True)
    video_text = models.CharField(blank=True, max_length=50)
    about_title = models.CharField(blank=True, max_length=50)
    reviews = StreamField([("review", ReviewBlock())], blank=True, use_json_field=True)
    contact_subtitle = models.CharField(blank=True, max_length=50)
    contact_title = models.CharField(blank=True, max_length=50)
    contact_email = models.EmailField(blank=True)
    contact_address = models.CharField(blank=True, max_length=250)
    btn_text = models.CharField(blank=True, max_length=50)
    about_subtitle = models.CharField(blank=True, max_length=50)
    services_title = models.CharField(blank=True, max_length=50)
    services_list = StreamField(
        [
            ("service", ServiceItemBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    services = StreamField(
        [('service', AboutServiceBlock())],
        use_json_field=True,
        blank=True
    )
    
    
    template = "portfolio/serviceindexpage.html"
    subpage_types = ["portfolio.ServicePage"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("breadcrumb_home"),
        FieldPanel("breadcrumb_services"),
        FieldPanel("video_link"),
        FieldPanel("video_text"),
        FieldPanel("about_title"),
        FieldPanel("about_subtitle"),
        FieldPanel("services_title"),
        FieldPanel("reviews"),
        FieldPanel("contact_subtitle"),
        FieldPanel("contact_title"),
        FieldPanel("contact_email"),
        FieldPanel("contact_address"),
        FieldPanel("btn_text"),
        FieldPanel("services"),
        FieldPanel("services_list"),
    ]
        
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
    breadcrumb_home = models.CharField(max_length=150, blank=True)
    btn_text = models.CharField(max_length=255, blank=True)
    servicelist_title = models.CharField(max_length=255, blank=True)

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
        FieldPanel("breadcrumb_home"),
        FieldPanel("service_title"),
        FieldPanel("service_subtitle"),
        FieldPanel("service_tagline"),
        FieldPanel("service_description"),
        FieldPanel("services"),
        FieldPanel("btn_text"),
        FieldPanel("servicelist_title"),
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
