from shop.models.product import Product, Category
from accounts.tests.test_user_modle import TestUserAccount
from django.core.files.uploadedfile import SimpleUploadedFile


class ProductTest(TestUserAccount):

    def setUp(self) -> None:
        self.category = Category.objects.create(name="men")
        self.cat = Category.objects.all()
        return super().setUp()

    def test_product_cat(self):
        """Checking Product Category object if created"""
        self.assertEqual(self.cat.count(), 1)
        self.assertEqual(self.cat[0].name, "men")
        self.assertEqual(self.cat[0].parent, None)

    def test_product(self):
        """Creating Product Object"""

        product = Product(
            name="Hoodie",
            desc="UngaBunga Hoodie",
        )
        product.product_image = SimpleUploadedFile(
            name='default.jpg', content=open(
                "static/images/default.jpg", 'rb').read(),
            content_type='image/jpeg')
        product.category = self.cat[0]
        product.save()

        """Checking if the product image uploaded successfully"""
        self.assertNotEqual(product.product_image, None)
