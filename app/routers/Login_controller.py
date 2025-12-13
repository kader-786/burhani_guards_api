# app/routers/Login_controller.py
from fastapi import APIRouter, HTTPException, status, Request
from app.models.login import LoginRequest, LoginResponse
from app.db import get_db_connection, call_function
from app.config import PG_CONFIG
import traceback
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/Login", tags=["Login"])


@router.post("/CheckLogin", response_model=LoginResponse)
async def check_login(payload: LoginRequest, request: Request):
    """
    Authenticate user and return user details
    
    - **username**: User's ITS ID (numeric)
    - **password**: User's password
    
    Returns user information and authentication status
    """
    try:
        # Get client IP address
        client_ip = request.client.host if request.client else "unknown"
        
        with get_db_connection() as conn:
            # Call the PostgreSQL function
            # Note: username should be ITS ID (numeric)
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.com_spr_login_json",
                {
                    "p_query_type": "CHECK_LOGIN",
                    "p_its_id": int(payload.username) if payload.username.isdigit() else 0,
                    "p_password": payload.password,
                    "p_ip_address": client_ip
                }
            )
            
            # Log the result for debugging
            logger.info(f"Login attempt for ITS ID: {payload.username}")
            logger.debug(f"Function result: {result}")
            
            # Parse the JSON result
            if result:
                # The function returns a JSON object with structure:
                # { "success": bool, "status_code": int, "message": str, "data": {...} }
                if isinstance(result, str):
                    result = json.loads(result)
                
                # Check if the result has the expected structure
                if result and isinstance(result, dict):
                    # Extract success, message, and data from the function response
                    success = result.get("success", False)
                    message = result.get("message", "Login failed")
                    data = result.get("data", None)
                    
                    return LoginResponse(
                        success=success,
                        message=message,
                        data=data
                    )
                else:
                    return LoginResponse(
                        success=False,
                        message="Invalid response format from server",
                        data=None
                    )
            else:
                return LoginResponse(
                    success=False,
                    message="No response from authentication server",
                    data=None
                )
            
    except Exception as ex:
        logger.error(f"Login error: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running
    """
    return {
        "status": "healthy",
        "service": "Burhani Guards Login API",
        "database": "PostgreSQL"
    }
