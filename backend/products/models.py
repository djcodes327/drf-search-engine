import random

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

# Create your models here.
User = get_user_model()

TAGS_MODEL_VALUES = ['electronics', 'cars', 'bikes', 'movies', 'cameras']


class ProductQuerySet(models.QuerySet):
    """Custom query set for Product Model -> ProductManager."""

    def is_public(self):
        # returns all products which are public
        return self.filter(public=True)

    def search(self, query, user=None):
        # Lookup checks the data in title and content
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        # Query Set
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs


class ProductManager(models.Manager):
    """Custom manager for Product Model."""

    def get_queryset(self):
        # Setting of Custom Query Set, using self._db to specify the database.
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        # search on manager -> manager -> queryset (search) gets called
        return self.get_queryset().search(query, user=user)


class Product(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, default=1)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
    public = models.BooleanField(default=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return f"/api/products/{self.pk}"

    @property
    def endpoint(self):
        return self.get_absolute_url()

    @property
    def body(self):
        return self.content

    @property
    def path(self):
        return f"/products/{self.pk}"

    def is_public(self) -> bool:
        return self.public

    def get_tags_list(self):
        return [random.choice(TAGS_MODEL_VALUES)]

    @property
    def sale_price(self):
        return "%.2f" % (float(self.price) * 0.8)

    def get_discount(self):
        return "122"

    def __str__(self):
        return self.title
