from django.test import TestCase, Client
from django.urls import reverse
from products.models import Genre, MediaType, Product, Category

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Sample data
        Genre.objects.create(name="Hip Hop")
        MediaType.objects.create(name="Vinyl")
        category = Category.objects.create(id=2, name="Clothing")

        Product.objects.create(
            name="Featured T-shirt",
            is_featured=True,
            category=category,
            price=19.99,
            stock=50,
            slug="featured-tshirt",
        )

        Product.objects.create(
            name="Featured Album",
            is_featured=True,
            media_type_id=1,  # Assuming 1-6 are music
            price=9.99,
            stock=50,
            slug="featured-album",
        )

    def test_home_view_context_data(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('genres', response.context)
        self.assertIn('media_types', response.context)
        self.assertIn('featured_clothing', response.context)
        self.assertIn('featured_music', response.context)
        self.assertEqual(len(response.context['genres']), 1)
        self.assertEqual(len(response.context['media_types']), 1)
        self.assertEqual(len(response.context['featured_clothing']), 1)
        self.assertEqual(len(response.context['featured_music']), 1)