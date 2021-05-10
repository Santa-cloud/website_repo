import sqlite3
from fastapi import FastAPI, status, HTTPException


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
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    data = cursor.execute(
        "SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID"
    ).fetchall()
    return {
        "categories":
            [{"id": x['CategoryID'], "name": x["CategoryName"]} for x in data]
    }


@app.get("/customers")
async def get_customers():
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    customers = cursor.execute(
        "SELECT CustomerID id, COALESCE(CompanyName, '') name, "
        "COALESCE(Address , '') || ' ' || COALESCE(PostalCode, '') || ' ' || "
        "COALESCE(City , '') || ' ' || COALESCE(Country , '') full_address "
        "FROM Customers"
    ).fetchall()
    return {
        "customers": customers
        }


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    product = cursor.execute(
        "SELECT ProductID id, ProductName name "
        "FROM Products "
        "WHERE ProductID = ?", (product_id, )
    ).fetchone()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return product
