import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Category

class Command(BaseCommand):
    help = 'Seeds the database with 1000 categories'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding categories...')

        # Lists to generate realistic-looking category names
        adjectives = [
            'Super', 'Mega', 'Ultra', 'Eco', 'Organic', 'Handmade', 'Vintage', 
            'Modern', 'Classic', 'Royal', 'Urban', 'Rustic', 'Smart', 'Luxury', 
            'Basic', 'Premium', 'Artisan', 'Natural', 'Daily', 'Pro'
        ]
        nouns = [
            'Electronics', 'Clothing', 'Home', 'Kitchen', 'Garden', 'Books', 
            'Toys', 'Sports', 'Beauty', 'Health', 'Automotive', 'Jewelry', 
            'Pet Supplies', 'Office', 'Groceries', 'Music', 'Tools', 'Crafts', 
            'Furniture', 'Fitness'
        ]
        
        categories_to_create = []
        existing_slugs = set(Category.objects.values_list('slug', flat=True))

        count = 0
        target = 1000

        # Generate unique categories
        while count < target:
            adj = random.choice(adjectives)
            noun = random.choice(nouns)
            suffix = random.randint(1, 9999)
            
            name = f"{adj} {noun} {suffix}"
            slug = slugify(name)

            if slug not in existing_slugs:
                existing_slugs.add(slug)
                categories_to_create.append(
                    Category(name=name, slug=slug)
                )
                count += 1

        # Use bulk_create with batch_size to insert efficiently
        Category.objects.bulk_create(categories_to_create, batch_size=500)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {target} categories!'))