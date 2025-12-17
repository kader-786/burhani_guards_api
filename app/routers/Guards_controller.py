# app/routers/Guards_controller.py
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.guards import GuardsByDateRequest, GuardCheckRequest, GuardsResponse
from app.db import get_db_connection, call_function
from app.config import PG_CONFIG
from app.auth import get_current_user
import traceback
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/Guards", tags=["Guards"])


# ============================================================================
# ACCEPTED GUARDS BY MIQAAT DATE
# ============================================================================

@router.post("/GetAcceptedGuardsByMiqaatDate", response_model=GuardsResponse)
async def get_accepted_guards_by_miqaat_date(
    payload: GuardsByDateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Get accepted guards for a specific miqaat date
    
    **Protected endpoint** - requires valid access token
    
    Retrieves all guards who have accepted duty assignments for miqaats 
    starting on the specified date. Only includes active guards with accepted status.
    
    - **date**: Miqaat start date to query guards for (required, format: YYYY-MM-DD)
    
    **Database Function Called:**
    - Function: `bg.spr_guards`
    - Query Type: `ACCEPTED-GUARDS-MIQAAT-DATE`
    - Parameters: `p_date`
    
    **Returns:**
    - List of accepted guards with their details
    - Each guard includes: ITS ID, name, contact info, team, position, miqaat details
    
    **Example Request:**
```json
    {
        "date": "2025-01-10"
    }
```
    
    **Example Response:**
```json
    {
        "success": true,
        "status_code": 200,
        "message": "Accepted guards for miqaat date retrieved successfully",
        "data": [
            {
                "its_id": 10001001,
                "full_name": "Ali Hussain",
                "miqaat_id": 1,
                "miqaat_name": "Qadambosi – Andheri",
                "email": "ali@example.com",
                "mobile": "9876543210",
                "whatsapp_mobile": "9876543210",
                "team_id": 2,
                "team_name": "Team A",
                "position_id": 1,
                "position_name": "Commander"
            },
            {
                "its_id": 10001002,
                "full_name": "Hassan Ahmed",
                "miqaat_id": 1,
                "miqaat_name": "Qadambosi – Andheri",
                "email": "hassan@example.com",
                "mobile": "9876543211",
                "whatsapp_mobile": "9876543211",
                "team_id": 2,
                "team_name": "Team A",
                "position_id": 2,
                "position_name": "Deputy"
            }
        ]
    }
```
    
    **Use Cases:**
    - Miqaat day attendance tracking
    - Guard roster generation for specific date
    - Duty assignment verification
    - Communication with guards on duty
    - Attendance sheet preparation
    """
    try:
        miqaat_date = payload.miqaat_date
        
        # Log the request
        logger.info(
            f"Accepted guards by miqaat date requested by user {current_user.get('its_id')} "
            f"for date: {miqaat_date}"
        )
        
        with get_db_connection() as conn:
            # Call the PostgreSQL function
            # IMPORTANT: Pass ALL parameters in order, set unused ones to None
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_guards",
                {
                    "p_query_type": "ACCEPTED-GUARDS-MIQAAT-DATE",
                    "p_date": miqaat_date,
                    "p_its_id": None  # Explicitly pass None for unused parameter
                }
            )
            
            logger.debug(f"Function result: {result}")
            
            # Parse the JSON result if it's a string
            if result:
                if isinstance(result, str):
                    result = json.loads(result)
                
                # The function returns a JSON object with success, status_code, message, data
                if isinstance(result, dict):
                    return GuardsResponse(
                        success=result.get("success", False),
                        status_code=result.get("status_code", 200),
                        message=result.get("message", "Query executed"),
                        data=result.get("data", None)
                    )
                else:
                    return GuardsResponse(
                        success=False,
                        status_code=500,
                        message="Invalid response format from database",
                        data=None
                    )
            else:
                return GuardsResponse(
                    success=False,
                    status_code=500,
                    message="No response from database",
                    data=None
                )
            
    except Exception as ex:
        logger.error(f"Error retrieving accepted guards by miqaat date: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# GUARD CHECK BY ITS ID
# ============================================================================

@router.post("/GuardCheck", response_model=GuardsResponse)
async def guard_check(
    payload: GuardCheckRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Get guard information by ITS ID
    
    **Protected endpoint** - requires valid access token
    
    Retrieves complete guard profile information for a specific ITS ID.
    Used for guard verification, lookup, and information display.
    
    - **its_id**: ITS ID to check guard information (required)
    
    **Database Function Called:**
    - Function: `bg.spr_guards`
    - Query Type: `GUARD-CHECK`
    - Parameters: `p_its_id`
    
    **Returns:**
    - Guard profile information
    - Includes: ITS ID, name, contact info, team, position
    
    **Example Request:**
```json
    {
        "its_id": 10001001
    }
```
    
    **Example Response:**
```json
    {
        "success": true,
        "status_code": 200,
        "message": "Guard information retrieved successfully",
        "data": [
            {
                "its_id": 10001001,
                "full_name": "Ali Hussain",
                "email": "ali@example.com",
                "mobile": "9876543210",
                "whatsapp_mobile": "9876543210",
                "team_id": 2,
                "team_name": "Team A",
                "position_id": 1,
                "position_name": "Commander"
            }
        ]
    }
```
    
    **Use Cases:**
    - Guard verification at miqaat entrance
    - Quick guard information lookup
    - Contact information retrieval
    - Team and position verification
    - Guard profile display
    """
    try:
        its_id = payload.its_id
        
        # Log the request
        logger.info(
            f"Guard check requested by user {current_user.get('its_id')} "
            f"for its_id: {its_id}"
        )
        
        with get_db_connection() as conn:
            # Call the PostgreSQL function
            # IMPORTANT: Pass ALL parameters in order, set unused ones to None
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_guards",
                {
                    "p_query_type": "GUARD-CHECK",
                    "p_date": None,  # Explicitly pass None for unused parameter
                    "p_its_id": its_id
                }
            )
            
            logger.debug(f"Function result: {result}")
            
            # Parse the JSON result if it's a string
            if result:
                if isinstance(result, str):
                    result = json.loads(result)
                
                # The function returns a JSON object with success, status_code, message, data
                if isinstance(result, dict):
                    return GuardsResponse(
                        success=result.get("success", False),
                        status_code=result.get("status_code", 200),
                        message=result.get("message", "Query executed"),
                        data=result.get("data", None)
                    )
                else:
                    return GuardsResponse(
                        success=False,
                        status_code=500,
                        message="Invalid response format from database",
                        data=None
                    )
            else:
                return GuardsResponse(
                    success=False,
                    status_code=500,
                    message="No response from database",
                    data=None
                )
            
    except Exception as ex:
        logger.error(f"Error checking guard information: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# CONVENIENCE ENDPOINT - Check My Guard Info
# ============================================================================

@router.get("/CheckMyGuardInfo", response_model=GuardsResponse)
async def check_my_guard_info(current_user: dict = Depends(get_current_user)):
    """
    Get guard information for the currently logged-in user
    
    **Protected endpoint** - requires valid access token
    
    Convenience endpoint that automatically uses the ITS ID from the JWT token
    to retrieve guard information for the authenticated user. No need to pass ITS ID.
    
    **Database Function Called:**
    - Function: `bg.spr_guards`
    - Query Type: `GUARD-CHECK`
    - Parameters: `p_its_id` (automatically extracted from token)
    
    **Returns:**
    - Current user's guard profile information
    
    **Example Response:**
```json
    {
        "success": true,
        "status_code": 200,
        "message": "Guard information retrieved successfully",
        "data": [
            {
                "its_id": 10001001,
                "full_name": "Ali Hussain",
                "team_name": "Team A",
                "position_name": "Commander"
            }
        ]
    }
```
    
    **Use Cases:**
    - "My Profile" screen in mobile app
    - Quick access to own guard information
    - Profile verification
    - Contact information display
    """
    try:
        # Extract ITS ID from the authenticated user's token
        its_id = current_user.get("its_id")
        
        if not its_id:
            logger.error("ITS ID not found in token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: ITS ID not found"
            )
        
        # Log the request
        logger.info(f"My guard info requested by user {its_id}")
        
        with get_db_connection() as conn:
            # Call the PostgreSQL function
            # IMPORTANT: Pass ALL parameters in order, set unused ones to None
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_guards",
                {
                    "p_query_type": "GUARD-CHECK",
                    "p_date": None,  # Explicitly pass None for unused parameter
                    "p_its_id": its_id
                }
            )
            
            logger.debug(f"Function result: {result}")
            
            # Parse the JSON result if it's a string
            if result:
                if isinstance(result, str):
                    result = json.loads(result)
                
                # The function returns a JSON object with success, status_code, message, data
                if isinstance(result, dict):
                    return GuardsResponse(
                        success=result.get("success", False),
                        status_code=result.get("status_code", 200),
                        message=result.get("message", "Query executed"),
                        data=result.get("data", None)
                    )
                else:
                    return GuardsResponse(
                        success=False,
                        status_code=500,
                        message="Invalid response format from database",
                        data=None
                    )
            else:
                return GuardsResponse(
                    success=False,
                    status_code=500,
                    message="No response from database",
                    data=None
                )
            
    except HTTPException:
        raise
    except Exception as ex:
        logger.error(f"Error retrieving my guard info: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def guards_health_check():
    """
    Health check for Guards endpoints
    
    Public endpoint - no authentication required
    """
    return {
        "status": "healthy",
        "service": "Guards Management",
        "endpoints": [
            "POST /Guards/GetAcceptedGuardsByMiqaatDate",
            "POST /Guards/GuardCheck",
            "GET /Guards/CheckMyGuardInfo"
        ]
    }