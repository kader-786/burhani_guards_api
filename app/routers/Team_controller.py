# app/routers/Team_controller.py
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.team import TeamRequest, TeamResponse
from app.db import get_db_connection, call_function
from app.config import PG_CONFIG
from app.auth import get_current_user
import traceback
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/Team", tags=["Team"])


# ============================================================================
# VIEW TEAM MEMBERS
# ============================================================================

@router.post("/ViewTeam", response_model=TeamResponse)
async def view_team(
    payload: TeamRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Get all team members with their details
    
    **Protected endpoint** - requires valid access token
    
    Retrieves all active members of a specific team with their complete profile information
    including contact details, position, jamaat, and organizational details.
    
    - **team_id**: Team ID to query members for (required)
    
    **Database Function Called:**
    - Function: `bg.spr_team`
    - Query Type: `VIEW-TEAM`
    - Parameters: `p_team_id`
    
    **Returns:**
    - List of team members with complete profile details
    - Each member includes: ITS ID, name, contact info, position, jamaat, etc.
    
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
        "message": "Team members retrieved successfully",
        "data": [
            {
                "its_id": 10001001,
                "full_name": "Ali Hussain",
                "full_name_arabic": "علي حسين",
                "age": 32,
                "idara": "Burhanpur",
                "category": "Active",
                "organization": "Burhani Guards",
                "email": "ali@example.com",
                "mobile": "9876543210",
                "whatsapp_mobile": "9876543210",
                "address": "Mumbai, India",
                "jamiaat_id": 1,
                "jamiaat_name": "Mumbai",
                "jamaat_id": 3,
                "jamaat_name": "Andheri",
                "city": "Mumbai",
                "position_id": 1,
                "position_name": "Commander"
            },
            {
                "its_id": 10001002,
                "full_name": "Hassan Ahmed",
                "full_name_arabic": "حسن أحمد",
                "age": 28,
                "idara": "Burhanpur",
                "category": "Active",
                "organization": "Burhani Guards",
                "email": "hassan@example.com",
                "mobile": "9876543211",
                "whatsapp_mobile": "9876543211",
                "address": "Mumbai, India",
                "jamiaat_id": 1,
                "jamiaat_name": "Mumbai",
                "jamaat_id": 3,
                "jamaat_name": "Andheri",
                "city": "Mumbai",
                "position_id": 2,
                "position_name": "Deputy"
            }
        ]
    }
```
    
    **Use Cases:**
    - Team commanders viewing their team roster
    - Administrative team member management
    - Contact list generation
    - Team coordination and communication
    - Duty assignment planning
    """
    try:
        team_id = payload.team_id
        
        # Log the request
        logger.info(
            f"View team requested by user {current_user.get('its_id')} "
            f"for team_id: {team_id}"
        )
        
        with get_db_connection() as conn:
            # Call the PostgreSQL function
            # Pass all parameters explicitly
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_team",
                {
                    "p_query_type": "VIEW-TEAM",
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
                    return TeamResponse(
                        success=result.get("success", False),
                        status_code=result.get("status_code", 200),
                        message=result.get("message", "Query executed"),
                        data=result.get("data", None)
                    )
                else:
                    return TeamResponse(
                        success=False,
                        status_code=500,
                        message="Invalid response format from database",
                        data=None
                    )
            else:
                return TeamResponse(
                    success=False,
                    status_code=500,
                    message="No response from database",
                    data=None
                )
            
    except Exception as ex:
        logger.error(f"Error retrieving team members: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# CONVENIENCE ENDPOINT - View My Team
# ============================================================================

@router.get("/ViewMyTeam", response_model=TeamResponse)
async def view_my_team(current_user: dict = Depends(get_current_user)):
    """
    Get all members of the currently logged-in user's team
    
    **Protected endpoint** - requires valid access token
    
    Convenience endpoint that automatically uses the team ID from the JWT token
    to retrieve all members of the authenticated user's team. No need to pass team ID.
    
    **Database Function Called:**
    - Function: `bg.spr_team`
    - Query Type: `VIEW-TEAM`
    - Parameters: `p_team_id` (automatically extracted from token)
    
    **Returns:**
    - List of team members with complete profile details
    - Sorted alphabetically by name
    
    **Example Response:**
```json
    {
        "success": true,
        "status_code": 200,
        "message": "Team members retrieved successfully",
        "data": [
            {
                "its_id": 10001001,
                "full_name": "Ali Hussain",
                "position_name": "Commander",
                "mobile": "9876543210",
                "email": "ali@example.com"
            }
        ]
    }
```
    
    **Use Cases:**
    - Team member viewing their own team roster
    - "My Team" screen in mobile app
    - Quick access to team contact information
    - Team member lookup
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
        logger.info(
            f"View my team requested by user {current_user.get('its_id')} "
            f"for team {team_id}"
        )
        
        with get_db_connection() as conn:
            # Call the PostgreSQL function
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_team",
                {
                    "p_query_type": "VIEW-TEAM",
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
                    return TeamResponse(
                        success=result.get("success", False),
                        status_code=result.get("status_code", 200),
                        message=result.get("message", "Query executed"),
                        data=result.get("data", None)
                    )
                else:
                    return TeamResponse(
                        success=False,
                        status_code=500,
                        message="Invalid response format from database",
                        data=None
                    )
            else:
                return TeamResponse(
                    success=False,
                    status_code=500,
                    message="No response from database",
                    data=None
                )
            
    except HTTPException:
        raise
    except Exception as ex:
        logger.error(f"Error retrieving my team members: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def team_health_check():
    """
    Health check for Team endpoints
    
    Public endpoint - no authentication required
    """
    return {
        "status": "healthy",
        "service": "Team Management",
        "endpoints": [
            "POST /Team/ViewTeam",
            "GET /Team/ViewMyTeam"
        ]
    }