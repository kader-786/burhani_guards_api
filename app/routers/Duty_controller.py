# app/routers/Duty_controller.py
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.duty import TeamDutyRequest, GuardDutyRequest, DutyResponse
from app.db import get_db_connection, call_function
from app.config import PG_CONFIG
from app.auth import get_current_user
import traceback
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/Duty", tags=["Duty"])


# ============================================================================
# ACTIVE ASSIGNED MIQAAT DUTIES (Team-based)
# ============================================================================

@router.post("/GetActiveAssignedMiqaatDuties", response_model=DutyResponse)
async def get_active_assigned_miqaat_duties(
    payload: TeamDutyRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Get active miqaat duties assigned to a team
    
    **Protected endpoint** - requires valid access token
    
    Retrieves all active miqaat duties that have been assigned to a specific team.
    Only returns duties for miqaats that are currently active.
    
    - **team_id**: Team ID to query duties for (required)
    
    **Database Function Called:**
    - Function: `bg.spr_duty_queries`
    - Query Type: `ACTIVE-ASSIGNED-MIQAAT-DUTY`
    - Parameters: `p_team_id`
    
    **Returns:**
    - List of active miqaat duties with full miqaat details
    - Each duty includes: duty_id, miqaat details, location, quota, dates, etc.
    
    **Example Request:**
```json
    {
        "team_id": 1
    }
```
    
    **Example Response:**
```json
    {
        "success": true,
        "status_code": 200,
        "message": "Active assigned miqaat duties retrieved successfully",
        "data": [
            {
                "duty_id": 1,
                "team_id": 1,
                "miqaat_id": 5,
                "miqaat_name": "Ashara Mubaraka 1446H",
                "miqaat_type_id": 1,
                "miqaat_type_name": "Ashara",
                "reporting_time": "2024-12-20T08:00:00",
                "quota": 10,
                "start_date": "2024-12-20T00:00:00",
                "end_date": "2024-12-30T23:59:59",
                "jamiaat_id": 1,
                "jamiaat_name": "Mumbai",
                "jamaat_id": 3,
                "jamaat_name": "Andheri",
                "location": "Main Gate"
            }
        ]
    }
```
    
    **Use Cases:**
    - Team commanders viewing their team's assigned duties
    - Dashboard showing upcoming duties for a team
    - Duty planning and coordination
    """
    try:
        team_id = payload.team_id
        
        # Log the request
        logger.info(
            f"Active assigned miqaat duties requested by user {current_user.get('its_id')} "
            f"for team_id: {team_id}"
        )
        
        with get_db_connection() as conn:
            # Call the PostgreSQL function
            # IMPORTANT: Pass ALL parameters in order, set unused ones to None
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_duty_queries",
                {
                    "p_query_type": "ACTIVE-ASSIGNED-MIQAAT-DUTY",
                    "p_team_id": team_id,
                    "p_its_id": None  # ← FIXED: Explicitly pass None for unused parameter
                }
            )
            
            logger.debug(f"Function result: {result}")
            
            # Parse the JSON result if it's a string
            if result:
                if isinstance(result, str):
                    result = json.loads(result)
                
                # The function returns a JSON object with success, status_code, message, data
                if isinstance(result, dict):
                    return DutyResponse(
                        success=result.get("success", False),
                        status_code=result.get("status_code", 200),
                        message=result.get("message", "Query executed"),
                        data=result.get("data", None)
                    )
                else:
                    return DutyResponse(
                        success=False,
                        status_code=500,
                        message="Invalid response format from database",
                        data=None
                    )
            else:
                return DutyResponse(
                    success=False,
                    status_code=500,
                    message="No response from database",
                    data=None
                )
            
    except Exception as ex:
        logger.error(f"Error retrieving active assigned miqaat duties: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# GUARD DUTIES ASSIGNED (Individual member-based)
# ============================================================================

@router.post("/GetGuardDutiesAssigned", response_model=DutyResponse)
async def get_guard_duties_assigned(
    payload: GuardDutyRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Get guard duties assigned to a specific member
    
    **Protected endpoint** - requires valid access token
    
    Retrieves all guard duties that have been assigned to a specific member (by ITS ID).
    Only returns duties that are currently active.
    
    - **its_id**: ITS ID of the member to query duties for (required)
    
    **Database Function Called:**
    - Function: `bg.spr_duty_queries`
    - Query Type: `GUARD-DUTIES-ASSIGNED`
    - Parameters: `p_its_id`
    
    **Returns:**
    - List of guard duties assigned to the member
    - Each duty includes: guard_duty_id, duty details, miqaat details, location, dates, etc.
    
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
        "message": "Guard duties retrieved successfully",
        "data": [
            {
                "guard_duty_id": 15,
                "duty_id": 1,
                "team_id": 1,
                "miqaat_id": 5,
                "miqaat_name": "Ashara Mubaraka 1446H",
                "miqaat_type_id": 1,
                "miqaat_type_name": "Ashara",
                "reporting_time": "2024-12-20T08:00:00",
                "start_date": "2024-12-20T00:00:00",
                "end_date": "2024-12-30T23:59:59",
                "jamiaat_id": 1,
                "jamiaat_name": "Mumbai",
                "jamaat_id": 3,
                "jamaat_name": "Andheri",
                "location": "Main Gate"
            }
        ]
    }
```
    
    **Use Cases:**
    - Individual members viewing their assigned duties
    - "My Duties" screen in mobile app
    - Personal duty calendar
    - Duty notifications and reminders
    """
    try:
        its_id = payload.its_id
        
        # Log the request
        logger.info(
            f"Guard duties requested by user {current_user.get('its_id')} "
            f"for its_id: {its_id}"
        )
        
        with get_db_connection() as conn:
            # Call the PostgreSQL function
            # IMPORTANT: Pass ALL parameters in order, set unused ones to None
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_duty_queries",
                {
                    "p_query_type": "GUARD-DUTIES-ASSIGNED",
                    "p_team_id": None,  # ← FIXED: Explicitly pass None for unused parameter
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
                    return DutyResponse(
                        success=result.get("success", False),
                        status_code=result.get("status_code", 200),
                        message=result.get("message", "Query executed"),
                        data=result.get("data", None)
                    )
                else:
                    return DutyResponse(
                        success=False,
                        status_code=500,
                        message="Invalid response format from database",
                        data=None
                    )
            else:
                return DutyResponse(
                    success=False,
                    status_code=500,
                    message="No response from database",
                    data=None
                )
            
    except Exception as ex:
        logger.error(f"Error retrieving guard duties: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# CONVENIENCE ENDPOINT - Get My Duties
# ============================================================================

@router.get("/GetMyDuties", response_model=DutyResponse)
async def get_my_duties(current_user: dict = Depends(get_current_user)):
    """
    Get duties assigned to the currently logged-in user
    
    **Protected endpoint** - requires valid access token
    
    Convenience endpoint that automatically uses the ITS ID from the JWT token
    to retrieve duties for the currently authenticated user. No need to pass ITS ID.
    
    **Database Function Called:**
    - Function: `bg.spr_duty_queries`
    - Query Type: `GUARD-DUTIES-ASSIGNED`
    - Parameters: `p_its_id` (automatically extracted from token)
    
    **Returns:**
    - List of guard duties assigned to the authenticated user
    
    **Example Response:**
```json
    {
        "success": true,
        "status_code": 200,
        "message": "Guard duties retrieved successfully",
        "data": [
            {
                "guard_duty_id": 15,
                "duty_id": 1,
                "team_id": 1,
                "miqaat_id": 5,
                "miqaat_name": "Ashara Mubaraka 1446H",
                "location": "Main Gate"
            }
        ]
    }
```
    
    **Use Cases:**
    - Mobile app "My Duties" screen
    - Dashboard showing user's upcoming duties
    - Quick access to personal duty information
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
        logger.info(f"My duties requested by user {its_id}")
        
        with get_db_connection() as conn:
            # Call the PostgreSQL function
            # IMPORTANT: Pass ALL parameters in order, set unused ones to None
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_duty_queries",
                {
                    "p_query_type": "GUARD-DUTIES-ASSIGNED",
                    "p_team_id": None,  # ← FIXED: Explicitly pass None for unused parameter
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
                    return DutyResponse(
                        success=result.get("success", False),
                        status_code=result.get("status_code", 200),
                        message=result.get("message", "Query executed"),
                        data=result.get("data", None)
                    )
                else:
                    return DutyResponse(
                        success=False,
                        status_code=500,
                        message="Invalid response format from database",
                        data=None
                    )
            else:
                return DutyResponse(
                    success=False,
                    status_code=500,
                    message="No response from database",
                    data=None
                )
            
    except HTTPException:
        raise
    except Exception as ex:
        logger.error(f"Error retrieving my duties: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# CONVENIENCE ENDPOINT - Get My Team Duties
# ============================================================================

@router.get("/GetMyTeamDuties", response_model=DutyResponse)
async def get_my_team_duties(current_user: dict = Depends(get_current_user)):
    """
    Get duties assigned to the currently logged-in user's team
    
    **Protected endpoint** - requires valid access token
    
    Convenience endpoint that automatically uses the team ID from the JWT token
    to retrieve duties for the authenticated user's team. No need to pass team ID.
    
    **Database Function Called:**
    - Function: `bg.spr_duty_queries`
    - Query Type: `ACTIVE-ASSIGNED-MIQAAT-DUTY`
    - Parameters: `p_team_id` (automatically extracted from token)
    
    **Returns:**
    - List of active miqaat duties assigned to the user's team
    
    **Example Response:**
```json
    {
        "success": true,
        "status_code": 200,
        "message": "Active assigned miqaat duties retrieved successfully",
        "data": [
            {
                "duty_id": 1,
                "team_id": 1,
                "miqaat_id": 5,
                "miqaat_name": "Ashara Mubaraka 1446H",
                "location": "Main Gate"
            }
        ]
    }
```
    
    **Use Cases:**
    - Team commanders viewing their team's duties
    - Team dashboard showing upcoming duties
    - Coordinator's overview of team assignments
    """
    try:
        # Extract team ID from the authenticated user's token
        team_id = current_user.get("team_id")
        
        if not team_id:
            logger.error("Team ID not found in token")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Team ID not found in user profile"
            )
        
        # Log the request
        logger.info(f"My team duties requested by user {current_user.get('its_id')} for team {team_id}")
        
        with get_db_connection() as conn:
            # Call the PostgreSQL function
            # IMPORTANT: Pass ALL parameters in order, set unused ones to None
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_duty_queries",
                {
                    "p_query_type": "ACTIVE-ASSIGNED-MIQAAT-DUTY",
                    "p_team_id": team_id,
                    "p_its_id": None  # ← FIXED: Explicitly pass None for unused parameter
                }
            )
            
            logger.debug(f"Function result: {result}")
            
            # Parse the JSON result if it's a string
            if result:
                if isinstance(result, str):
                    result = json.loads(result)
                
                # The function returns a JSON object with success, status_code, message, data
                if isinstance(result, dict):
                    return DutyResponse(
                        success=result.get("success", False),
                        status_code=result.get("status_code", 200),
                        message=result.get("message", "Query executed"),
                        data=result.get("data", None)
                    )
                else:
                    return DutyResponse(
                        success=False,
                        status_code=500,
                        message="Invalid response format from database",
                        data=None
                    )
            else:
                return DutyResponse(
                    success=False,
                    status_code=500,
                    message="No response from database",
                    data=None
                )
            
    except HTTPException:
        raise
    except Exception as ex:
        logger.error(f"Error retrieving my team duties: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def duty_health_check():
    """
    Health check for Duty endpoints
    
    Public endpoint - no authentication required
    """
    return {
        "status": "healthy",
        "service": "Duty Management",
        "endpoints": [
            "POST /Duty/GetActiveAssignedMiqaatDuties",
            "POST /Duty/GetGuardDutiesAssigned",
            "GET /Duty/GetMyDuties",
            "GET /Duty/GetMyTeamDuties"
        ]
    }