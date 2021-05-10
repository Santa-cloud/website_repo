import sqlite3
from fastapi import FastAPI


app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get("/products")
async def products():
    products = app.db_connection.execute("SELECT ProductName FROM Products").fetchall()
    return {
        "products": products,
        "products_counter": len(products)
    }


@app.get("/categories")
async def get_categories():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        "SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID"
    ).fetchall()

    data["categories"] = [{"id": x['CategoryID'], "name": x["CategoryName"]} for x in data]
    return data
