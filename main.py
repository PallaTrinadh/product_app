from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from product_app.database import Base, engine
from product_app.routers import products, orders

app = FastAPI(title="Transactional Order Management System")

# 🚀 Allow React frontend
origins = [
    "http://localhost:5174",  # React (Vite)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # domains allowed
    allow_credentials=True,
    allow_methods=["*"],         # allow all HTTP methods
    allow_headers=["*"],         # allow all headers
)

# create tables
Base.metadata.create_all(bind=engine)

# register routers
app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
def home():
    return {"message": "Welcome to Transactional Order Management System"}

