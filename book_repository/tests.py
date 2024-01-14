from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth.models import User
from wagtail.models import Site
from .models import BookRepositoryPage, BookPage, Author


class BookRepositoryPageTestCase(TestCase):
    def setUp(self):
        self.root_page = Site.objects.get().root_page
        self.book_repository_page = BookRepositoryPage(title='Book Repository', slug='book-repository')
        self.root_page.add_child(instance=self.book_repository_page)

        self.author1 = Author.objects.create(name='Test Author')
        self.author2 = Author.objects.create(name='Test Author 2')
        self.author3 = Author.objects.create(name='Test Author 3')
        self.book1 = BookPage(title='Book 1', name='Test Book 1', create_date='2022-01-15')
        self.root_page.add_child(instance=self.book1)
        self.book1.authors.add(self.author1)

        self.book2 = BookPage(title='Book 2', name='Test Book 2', create_date='2022-01-16')
        self.root_page.add_child(instance=self.book2)
        self.book2.authors.add(self.author2)

        self.book1.save()
        self.book2.save()

    def test_get_context_no_filter(self):
        request = HttpRequest()
        response = self.book_repository_page.get_context(request)

        self.assertEqual(response['is_filtered'], False)
        self.assertEqual(len(response['authors']), 3)
        self.assertEqual(len(response['books']), 2)

    def test_get_context_with_author_filter(self):
        request = HttpRequest()
        request.GET['author'] = str(self.author1.id)
        response = self.book_repository_page.get_context(request)

        self.assertEqual(response['is_filtered'], True)
        self.assertEqual(len(response['authors']), 3)
        self.assertEqual(len(response['books']), 1)

    def test_get_context_with_author_without_books_filter(self):
        request = HttpRequest()
        request.GET['author'] = str(self.author3.id)
        response = self.book_repository_page.get_context(request)

        self.assertEqual(response['is_filtered'], True)
        self.assertEqual(len(response['authors']), 3)
        self.assertEqual(len(response['books']), 0)

    def test_get_context_with_non_existent_author_filter(self):
        request = HttpRequest()
        request.GET['author'] = '999'  # Non-existent author id
        response = self.book_repository_page.get_context(request)

        self.assertEqual(response['is_filtered'], False)
        self.assertEqual(len(response['authors']), 3)
        self.assertEqual(len(response['books']), 2)
