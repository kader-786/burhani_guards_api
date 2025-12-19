# app/routers/Guards_controller.py
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.guards import (
    GuardsByDateRequest, 
    GuardCheckRequest, 
    GuardsWithDutyRequest,  # ← Add this
    GuardsResponse
)
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
        "p_its_id": None,       # Explicitly pass None for unused parameter
        "p_miqaat_id": None,    # Explicitly pass None for unused parameter
        "p_duty_id": None,      # Explicitly pass None for unused parameter
        "p_team_id": None       # Explicitly pass None for unused parameter
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
        "p_date": None,         # Explicitly pass None for unused parameter
        "p_its_id": its_id,
        "p_miqaat_id": None,    # Explicitly pass None for unused parameter
        "p_duty_id": None,      # Explicitly pass None for unused parameter
        "p_team_id": None       # Explicitly pass None for unused parameter
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
# GET ALL GUARDS WITH DUTY ASSIGNMENT STATUS
# ============================================================================

@router.post("/GetAllGuardsWithDuty", response_model=GuardsResponse)
async def get_all_guards_with_duty(
    payload: GuardsWithDutyRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        miqaat_id = payload.miqaat_id
        duty_id = payload.duty_id
        team_id = payload.team_id
        
        # Log the request
        logger.info(
            f"Get all guards with duty requested by user {current_user.get('its_id')} "
            f"for miqaat_id: {miqaat_id}, duty_id: {duty_id}, team_id: {team_id}"
        )
        
        with get_db_connection() as conn:
            # Call the PostgreSQL function
            # IMPORTANT: Pass ALL parameters in order, set unused ones to None
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_guards",
                {
                    "p_query_type": "GET-ALL-GUARDS-WITH-DUTY",
                    "p_date": None,           # Explicitly pass None for unused parameter
                    "p_its_id": None,         # Explicitly pass None for unused parameter
                    "p_miqaat_id": miqaat_id,
                    "p_duty_id": duty_id,
                    "p_team_id": team_id
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
        logger.error(f"Error retrieving guards with duty status: {str(ex)}")
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
            "POST /Guards/GetAllGuardsWithDuty",  # ← Add this
            "GET /Guards/CheckMyGuardInfo"
        ]
    }