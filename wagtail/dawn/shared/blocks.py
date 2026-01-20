from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class ServiceItemBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(required=True)
    link = blocks.PageChooserBlock(required=True)

    items = blocks.ListBlock(
        blocks.StructBlock([
            ("text", blocks.CharBlock()),
            ("link", blocks.PageChooserBlock(required=False)),
        ]),
        label="Service Items"
    )

    class Meta:
        icon = "cogs"
        label = "Service"

        