from fastapi import FastAPI, HTTPException
from models import Book
from database import collection
from bson.objectid import ObjectId
from flask import request

app = FastAPI()

@app.post("/books/")
async def create_book(book: Book):
    result = collection.insert_one(book.dict())
    return {
        "id": str(result.inserted_id),
        "book": book
    }


@app.post("/books/")
async def create_book(book: Book):
    if not book.validate():
        raise HTTPException(status_code=422, detail="Invalid book data")
    result = collection.insert_one(book.dict())
    return {
        "id": str(result.inserted_id),
        "book": book
    }


@app.get("/books/")
async def read_books():
    books = []
    for book in collection.find():
        books.append(Book(**book))
    return books

@app.get("/books/top-authors")
async def top_authors():
    pipeline = [
        {"$group": {"_id": "$author", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    authors = []
    for author in collection.aggregate(pipeline):
        authors.append(author["_id"])
    print(authors)
    return authors

@app.get("/books/count")
async def count_books():
    return collection.count_documents({})

@app.get("/books/by-price-range")
async def search_books_by_price_range(min_price: float, max_price: float):
    print(min_price)
    books = []
    for book in collection.find({"price": {"$gte": min_price, "$lte": max_price}}):
        books.append(Book(**book))
    return books

@app.get("/books/by-author")
async def search_books_by_author(author: str):
    
    books = []
    for book in collection.find({"author": {"$regex": author, "$options": "i"}}):
        books.append(Book(**book))
    return books

@app.get("/books/search")
async def search_books(query: str):
    pipeline = [
        {"$search": {"text": {"query": query, "path": ["title", "author"]}}}
    ]
    books = []
    for book in collection.aggregate(pipeline):
        books.append(Book(**book))
    print(books)
    return books

@app.get("/books/bestsellers")
async def bestsellers():
    pipeline = [
        {"$sort": {"stock": -1}},
        {"$limit": 5}
    ]
    books = []
    for book in collection.aggregate(pipeline):
        books.append(Book(**book))
    return books

@app.get("/books/{book_id}")
async def read_book(book_id: str):
    book = collection.find_one({"_id": ObjectId(book_id)})
    if book:
        return Book(**book)
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}")
async def update_book(book_id: str, book: Book):
    result = collection.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": book.dict(exclude_unset=True)}
    )
    if result.modified_count == 1:
        return {"message": "Book updated successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
    result = collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 1:
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
