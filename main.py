from fastapi import Depends, FastAPI, HTTPException
from models import Product
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import database_models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"], # or ["http://localhost:300"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def init_db():
    db = SessionLocal()
    try:
        count = db.query(database_models.Product).count()

        if count == 0:
            for product in products:
                db.add(database_models.Product(**product.model_dump()))
            db.commit()
    finally:
        db.close()

init_db()


@app.get("/products/", response_model=list[Product])
def get_all_products(db:Session = Depends(get_db)):

    db_products = db.query(database_models.Product).all()

    return db_products


@app.get("/products/{id}", response_model=Product)
def get_product_by_id(id:int, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@app.post("/products/", response_model=Product)
def add_product(product : Product, db: Session = Depends(get_db)):
    existing_product = db.query(database_models.Product).filter(database_models.Product.id == product.id).first()
    if existing_product is not None:
        raise HTTPException(status_code=400, detail="Product with this id already exists")

    db_product = database_models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/products/{id}")
def update_product(id:int, product:Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit()
    db.refresh(db_product)
    return {"message": "Product updated successfully", "product": db_product}


@app.delete("/products/{id}")
def delete_product(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return {"message": "product deleted"}

