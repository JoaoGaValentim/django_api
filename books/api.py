from ninja import Query, Router

from django.shortcuts import get_object_or_404
from books.models import Books, Categories
from .schemas import BooksSchema, RateSchema, SortFiltersSchema

books_router = Router()


@books_router.post("/")
def create_books(request, books_schema: BooksSchema):
    name = books_schema.dict()["name"]
    streaming = books_schema.dict()["streaming"]
    categories = books_schema.dict()["categories"]

    try:
        if streaming not in ["F", "AK"]:
            return 400, {"status": "Error: streaming is F or AK"}

        book = Books(
            name=name,
            streaming=streaming,
        )

        book.save()

        for category in categories:
            tmp = Categories.objects.get(id=category)
            book.categories.add(tmp)

        return 200, {"status": "success"}
    except:
        return 500, {"error": "Internal Server Error"}


@books_router.put("/rate-book/{books_id}")
def rate_book(request, books_id: int, rate_schema: RateSchema):
    rate_comments = rate_schema.dict()["comments"]
    rate_points = rate_schema.dict()["points"]

    try:
        book = Books.objects.get(id=books_id)
        book.comments = rate_comments
        book.points = rate_points
        book.save()

        return 200, {"status": "Success"}
    except:
        return 500, {"error": "Internal Server Error"}


@books_router.delete("/delete-book/{book_id}")
def delete(request, book_id: int):
    book = Books.objects.get(id=book_id)
    book.delete()

    return book_id


@books_router.get("/sort-book/", response={200: BooksSchema, 404: dict})
def sortear_livro(request, filters: Query[SortFiltersSchema]):
    min_points = filters.dict()["min_points"]
    categoria = filters.dict()["categories"]
    reread = filters.dict()["reread"]

    books = Books.objects.all()

    print(min_points)

    if not reread:
        books = books.filter(points=None)

    if min_points is not None:
        books = books.filter(points__gte=min_points)

    if categoria is not None:
        books = books.filter(categories__id=categoria)

    books = books.order_by("?").first()

    if books:
        return 200, books
    else:
        return 404, {"status": "Not Found Book"}
