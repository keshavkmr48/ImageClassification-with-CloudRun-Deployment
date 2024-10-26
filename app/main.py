from fastapi import FastAPI
from app.routes import files, predict
from app.db import init_db, get_db
from .services.rabbitmq_service import consume_image_buffer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware if needed (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
async def startup_event():
    # Start the RabbitMQ consumer to listen for prediction requests
    await consume_image_buffer()
    await init_db()


# Include routes
app.include_router(files.router, prefix="/files", tags=["file"])
app.include_router(predict.router, prefix="/predict", tags=["prediction"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Image Classification API"}
