from ninja import Field, ModelSchema, Schema
from .models import Books


class BooksSchema(ModelSchema):
    class Meta:
        model = Books
        fields = ["name", "streaming", "categories"]


class RateSchema(ModelSchema):
    class Meta:
        model = Books
        fields = ["points", "comments"]


class SortFiltersSchema(Schema):
    min_points: int = Field(default=None)
    categories: int = Field(default=None)
    reread: bool = Field(default=False)
