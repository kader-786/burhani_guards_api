from fastapi import FastAPI
from app.routers import password_controller, RoleMaster_controller, Login_controller, Points_controller, Activity_controller
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Driver's Mate API",
    description="Driver's Mate APIs for various functionalities and testing")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all "controllers"
# app.include_router(password_controller.router)
# app.include_router(RoleMaster_controller.router)
app.include_router(Login_controller.router)
app.include_router(Points_controller.router)
app.include_router(Activity_controller.router)

