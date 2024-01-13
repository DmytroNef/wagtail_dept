from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('author_image'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'


class BookRepositoryPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]


class BookPage(Page):
    name = models.CharField(max_length=250)
    create_date = models.DateField("Create date")
    description = RichTextField(blank=True)
    authors = ParentalManyToManyField('book_repository.Author', blank=True)

    def main_image(self):
        book_image = self.book_images.first()
        if book_image:
            return book_image.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('name'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('create_date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
        ], heading="Book information"),
        FieldPanel('name'),
        FieldPanel('description'),
        InlinePanel('book_images', label="Book images"),
    ]


class BookPageImage(Orderable):
    page = ParentalKey(BookPage, on_delete=models.CASCADE, related_name='book_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]
