import random
import urllib.request
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from shop.models import Category, Product

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with mock products and downloaded genuine images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=20,
            help='Number of products to create (default: 20)'
        )

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        self.stdout.write(f'Seeding {total} products with downloaded images...')

        categories = list(Category.objects.all())
        if not categories:
            self.stdout.write(self.style.ERROR('No categories found! Run seed_categories first.'))
            return

        sellers = list(User.objects.filter(is_staff=True) | User.objects.all())
        if not sellers:
            self.stdout.write(self.style.ERROR('No users/sellers found! Create a superuser or user first.'))
            return

        product_adjectives = ['Wireless', 'Ergonomic', 'Portable', 'Durable', 'Smart', 'Compact', 'Heavy Duty', 'Ultra-Slim', 'Handcrafted', 'Vintage']
        product_nouns = ['Headphones', 'Backpack', 'Water Bottle', 'Desk Lamp', 'Running Shoes', 'Smartwatch', 'Coffee Maker', 'Bluetooth Speaker', 'Notebook', 'Yoga Mat']

        existing_slugs = set(Product.objects.values_list('slug', flat=True))
        success_count = 0

        for i in range(total):
            adj = random.choice(product_adjectives)
            noun = random.choice(product_nouns)
            unique_suffix = random.randint(1000, 9999)
            
            name = f"{adj} {noun} {unique_suffix}"
            slug = slugify(name)
            
            while slug in existing_slugs:
                unique_suffix = random.randint(10000, 99999)
                name = f"{adj} {noun} {unique_suffix}"
                slug = slugify(name)
            
            existing_slugs.add(slug)

            category = random.choice(categories)
            seller = random.choice(sellers)
            price = Decimal(random.uniform(9.99, 499.99)).quantize(Decimal('0.01'))
            stock = random.randint(5, 150)
            description = f"This is a high-quality {name.lower()} designed for daily performance and long-lasting durability. Perfect for enthusiasts and professionals alike."

            # Create product instance first
            product = Product(
                category=category,
                seller=seller,
                name=name,
                slug=slug,
                description=description,
                price=price,
                stock=stock,
                available=True
            )

            # Fetch a real image from Picsum Photos and save to ImageField
            try:
                image_id = random.randint(10, 500)
                image_url = f"https://picsum.photos/id/{image_id}/600/600"
                
                req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    image_content = response.read()
                    file_name = f"{slug}.jpg"
                    product.image.save(file_name, ContentFile(image_content), save=False)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Could not download image for {name}: {e}"))

            product.save()
            success_count += 1
            self.stdout.write(f"Created [{success_count}/{total}]: {name}")

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {success_count} products with genuine images!'))