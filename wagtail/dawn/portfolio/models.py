from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag


from wagtail.models import Page
from wagtail.fields import RichTextField
from modelcluster.fields import ParentalKey


class ProjectPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "portfolio.ProjectPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )



class PortfolioIndexPage(Page):
    portfolio_title = models.CharField(blank=True,max_length=250)
    portfolio_subtitle = models.CharField(blank=True, max_length=250)

    content_panels = Page.content_panels + ["portfolio_title", "portfolio_subtitle"]
    subpage_types = ["portfolio.ProjectPage"]

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
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="+",
)

    tags = ClusterTaggableManager(
        through=ProjectPageTag,
        blank=True,
        help_text="Project categories (branding, design, interactive, etc.)",
    )

    project_type = models.CharField(max_length=255)
    team = models.CharField(max_length=255, blank=True)
    date_range = models.CharField(max_length=100, blank=True)

    content_panels = Page.content_panels + ["hero_image", "project_type", "team", "date_range", "tags"]

    parent_page_types = ["portfolio.PortfolioIndexPage"]
    
    

class ServiceIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + ["intro"]

class ServicePage(Page):
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + ["intro", "body"]
    

