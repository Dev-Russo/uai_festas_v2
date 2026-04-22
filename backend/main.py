from fastapi import FastAPI
from routers import auth, user, events, products, sales, dashboard
from routers.commissioner import router as commissioner_router, me_router as commissioner_me_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.18.5:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(events.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(dashboard.router)
app.include_router(commissioner_router)
app.include_router(commissioner_me_router)
