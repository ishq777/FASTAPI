from fastapi import FastAPI
from models import Product

app = FastAPI()


@app.get("/")
def greet():
    return ("Hello")


products = [

Product(id=1, name="Phone", description="Nice phone", price=299, quantity=20),
Product(id=2, name="Laptop", description="Powerful laptop", price=999, quantity=10),
Product(id=3, name="Headphones", description="Noise cancelling", price=199, quantity=30),
Product(id=4, name="Tablet", description="Portable tablet", price=499, quantity=15),
Product(id=5, name="Smartwatch", description="Fitness tracking watch", price=149, quantity=25),
Product(id=6, name="Camera", description="High resolution camera", price=799, quantity=8),
Product(id=7, name="Monitor", description="Full HD display", price=249, quantity=12),
Product(id=8, name="Keyboard", description="Mechanical keyboard", price=89, quantity=18),
Product(id=9, name="Mouse", description="Wireless mouse", price=49, quantity=35),
Product(id=10, name="Printer", description="All-in-one printer", price=199, quantity=7),
Product(id=11, name="Speaker", description="Bluetooth speaker", price=79, quantity=22),
Product(id=12, name="Router", description="WiFi 6 router", price=129, quantity=14),
Product(id=13, name="SSD", description="1TB solid state drive", price=159, quantity=20),
Product(id=14, name="Hard Drive", description="2TB external HDD", price=99, quantity=16),
Product(id=15, name="Webcam", description="HD webcam", price=69, quantity=19),
Product(id=16, name="Microphone", description="USB condenser mic", price=119, quantity=11),
]


@app.get("/products")
def get_all_products():
    return products


@app.get("/product/{id}")
def get_product_by_id(id:int):
    for p in products:
        if p.id == id:
            return p
    
    return "Not found"


@app.post("/add_product")
def add_product(product : Product):
    
    products.append(product)
    return product


@app.patch("/update_product/{id}")
def update_product(id:int, product:Product):


    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "product added"

    return "Enter Valid ID"


@app.delete("/delete_product/{id}")
def delete_product(id:int):
    
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "product deleted"
    
    return "enter valid id"
