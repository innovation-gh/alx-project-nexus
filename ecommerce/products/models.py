from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Django's AbstractUser already includes 'id', 'username', and 'password'
    # 'email' is included but we'll ensure it's unique
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # This creates the one-to-many relationship.
    # It adds a 'category_id' column to the Product table.
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # Keeps products if a category is deleted
        null=True,                  # Allows products to be un-categorized
        related_name='products'     # Allows you to access products from a category instance
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Optimizes database queries for category and date filtering
        indexes = [models.Index(fields=['category', 'created_at'])]
        ordering = ['-created_at'] # Sorts products by newest first

    def __str__(self):
        return f"{self.name} ({self.category.name if self.category else 'Uncategorized'})"