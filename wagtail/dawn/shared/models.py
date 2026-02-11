from django.db import models
from wagtail.models import Page, Site
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel, MultiFieldPanel
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField

from wagtail_localize.fields import TranslatableField
from django.utils.timezone import now


@register_snippet
class MainMenu(ClusterableModel):
    title = models.CharField(max_length=100)
    
    cta_label = models.CharField(
        max_length=50,
        blank=True,
        help_text="Label for the right-side button (e.g. Showcase)"
    )
    
    cta_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        FieldPanel("title"),
        InlinePanel("items", label="Menu items"),
        FieldPanel("cta_label"),
        PageChooserPanel("cta_page"),  # CTA chooser here
    ]

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    menu = ParentalKey(
        MainMenu,
        related_name="items",
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100)

    page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE
    )

    panels = [
        FieldPanel("title"),
        PageChooserPanel("page"),
        FieldPanel("parent"),
    ]

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title
    
@register_snippet
class FooterSnippet(models.Model):
    site = models.OneToOneField(
        Site,
        on_delete=models.CASCADE,
        related_name="footer",
    )

    # ─── About ───────────────────────────────────────────────
    about_title = models.CharField(max_length=255)
    about_text = RichTextField(features=["bold", "italic", "link"])

    # ─── Contact ─────────────────────────────────────────────
    contact_title = models.CharField(max_length=255)
    address = models.TextField()
    email_label = models.CharField(max_length=255)
    email = models.EmailField()

    # ─── Legal ───────────────────────────────────────────────
    legal_title = models.CharField(max_length=255)

    terms_label = models.CharField(max_length=255)
    terms_url = models.URLField()

    privacy_label = models.CharField(max_length=255)
    privacy_url = models.URLField()

    cookie_label = models.CharField(max_length=255)
    cookie_url = models.URLField()

    # ─── Copyright ───────────────────────────────────────────
    copyright_text = models.CharField(
        max_length=255,
        help_text="Use {year} where the year should appear"
    )

    # ─── Social (shared across locales) ──────────────────────
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    panels = [
        FieldPanel("site"),
        
        MultiFieldPanel(
            [
                FieldPanel("about_title"),
                FieldPanel("about_text"),
            ],
            heading="About",
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_title"),
                FieldPanel("address"),
                FieldPanel("email_label"),
                FieldPanel("email"),
            ],
            heading="Contact",
        ),
        MultiFieldPanel(
            [
                FieldPanel("legal_title"),
                FieldPanel("terms_label"),
                FieldPanel("terms_url"),
                FieldPanel("privacy_label"),
                FieldPanel("privacy_url"),
                FieldPanel("cookie_label"),
                FieldPanel("cookie_url"),
            ],
            heading="Legal",
        ),
        MultiFieldPanel(
            [
                FieldPanel("copyright_text"),
            ],
            heading="Copyright",
        ),
        MultiFieldPanel(
            [
                FieldPanel("facebook_url"),
                FieldPanel("linkedin_url"),
                FieldPanel("instagram_url"),
            ],
            heading="Social",
        ),
    ]

    # ─── Wagtail Localize configuration ──────────────────────
    translatable_fields = [
        TranslatableField("about_title"),
        TranslatableField("about_text"),
        TranslatableField("contact_title"),
        TranslatableField("address"),
        TranslatableField("email_label"),
        TranslatableField("legal_title"),
        TranslatableField("terms_label"),
        TranslatableField("privacy_label"),
        TranslatableField("cookie_label"),
        TranslatableField("copyright_text"),
    ]

    def rendered_copyright(self):
        """
        Replaces {year} token in localized copyright text.
        """
        return self.copyright_text.replace(
            "{year}",
            str(now().year)
        )
