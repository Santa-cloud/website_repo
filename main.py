import sqlite3
from fastapi import FastAPI, status, HTTPException
from typing import Optional


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


@app.get("/employees")
async def get_employees(
        limit: Optional[int] = -1,
        offset: Optional[int] = 0,
        order: Optional[str] = None
):
    if order is None:
        order = "id"
    elif order not in ["first_name", "last_name", "city"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    sqlite3.paramstyle = "named"
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    employees = cursor.execute(
        "SELECT EmployeeID id, LastName last_name, FirstName first_name, City city "
        f"FROM Employees ORDER BY {order} LIMIT :limit OFFSET :offset ",
        {"limit": limit, "offset": offset}
    ).fetchall()
    return {"employees": employees}


@app.get("/products_extended")
async def get_products_extended():
    cursor = app.db_connection.cursor()
    cursor.row_factory = sqlite3.Row
    products = cursor.execute(
        "SELECT Products.ProductID id, Products.ProductName name, "
        "Categories.CategoryName category, Suppliers.CompanyName supplier "
        "FROM Products "
        "JOIN Categories ON Products.CategoryID = Categories.CategoryID "
        "JOIN Suppliers ON Products.SupplierID =  Suppliers.SupplierID "
        "ORDER BY ProductID"
    ).fetchall()
    return {
        "products_extended": products
    }
