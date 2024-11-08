from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Books(models.Model):
    streaming_choices = (
        ("AK", "Amazon Kindle"),
        ("F", "Fisico"),
    )

    name = models.CharField(max_length=255)

    streaming = models.CharField(
        max_length=2,
        choices=streaming_choices,
    )

    points = models.IntegerField(
        null=True,
        blank=True,
    )

    comments = models.TextField()

    categories = models.ManyToManyField(Categories)

    def __str__(self):
        return self.name
