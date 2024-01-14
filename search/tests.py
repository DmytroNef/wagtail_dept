from http import HTTPStatus
from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from wagtail.models import Page

from book_repository.models import BookRepositoryPage, BookPage


class SearchViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        # get the root page
        root_page = Page.objects.first()

        # add test pages as children of the root
        self.page1 = BookPage(title="Book Page 1", name="War and Peace", create_date=date(1867, 1, 1))
        root_page.add_child(instance=self.page1)

        self.page2 = BookPage(title="Book Page 2", name="Hamlet", create_date=date(1601, 1, 1))
        root_page.add_child(instance=self.page2)

        self.page3 = BookPage(title="Book Page 2", name="Don Quixote", create_date=date(1605, 1, 1))
        root_page.add_child(instance=self.page3)

        self.page1.save()
        self.page2.save()
        self.page3.save()

    def test_search_no_query(self) -> None:
        response = self.client.get(reverse("search"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context["search_results"]), 0)

    def test_search_query(self) -> None:
        response = self.client.get(
            reverse("search"),
            {"query": "War"},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context["search_results"]), 1)

    def test_search_non_existant_book(self) -> None:
        response = self.client.get(
            reverse("search"),
            {
                "query": "Test",
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context["search_results"]), 0)

    def test_search_query_with_many_words(self) -> None:
        response = self.client.get(
            reverse("search"),
            {"query": "War Hamlet Don"},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context["search_results"]), 3)

