from fastapi import FastAPI
from routes.borrow import router  # Import the router

app = FastAPI()

# Include the borrow routes
app.include_router(router)
