from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
class Author(models.Model, index.Indexed):
    """Author snippet model"""
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    search_fields = [
        index.FilterField('name'),
    ]

    panels = [
        FieldPanel('name'),
        FieldPanel('author_image'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'


class BookRepositoryPage(Page):
    """Book Repository Page model"""
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        is_filtered = False
        books = BookPage.objects.all()

        # books filter by author id from query param
        author_id = request.GET.get('author')
        if author_id:
            author = Author.objects.filter(id=author_id).first()
            if author:
                books = BookPage.objects.filter(authors=author)
                is_filtered = True

        # add to context all authors list with id and name
        authors = Author.objects.all().order_by('name').values('id', 'name')

        context.update({
            'authors': authors,
            'books': books,
            'is_filtered': is_filtered
        })
        return context


class BookPage(Page):
    """Book Page model"""
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
        index.RelatedFields('authors', [
            index.FilterField('name'),
        ]),
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
    """Book Page Image Orderable model"""
    page = ParentalKey(BookPage, on_delete=models.CASCADE, related_name='book_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]
