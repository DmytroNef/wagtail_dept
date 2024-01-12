from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel


class AuthorPage(Page):
    name = RichTextField()
    description = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('description'),
        InlinePanel('books', heading="Books", label="Book"),
    ]

    class Meta:
        verbose_name = "Author Page"
        verbose_name_plural = "Author Pages"

class BookPage(Orderable):
    author = ParentalKey(AuthorPage, on_delete=models.CASCADE, related_name='books')
    name = RichTextField()
    description = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('description'),
    ]
