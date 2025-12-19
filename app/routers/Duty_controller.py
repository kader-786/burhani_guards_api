# app/routers/Duty_controller.py
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.duty import (
    TeamDutyRequest, 
    GuardDutyRequest,
    DutyByIdRequest,
    TeamsByJamiaatRequest,
    DutyInsertRequest,
    DutyUpdateRequest,
    DutyDeleteRequest,
    GuardDutyInsertRequest,
    DutyResponse,
    DutyCRUDResponse,
    GuardDutyInsertResponse
)
from app.db import get_db_connection, call_function
from app.config import PG_CONFIG
from app.auth import get_current_user
import psycopg2
from psycopg2.extras import RealDictCursor
import traceback
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/Duty", tags=["Duty"])


# ============================================================================
# QUERY ENDPOINTS
# ============================================================================

# ============================================================================
# ACTIVE ASSIGNED MIQAAT DUTIES (Team-based)
# ============================================================================

@router.post("/GetActiveAssignedMiqaatDuties", response_model=DutyResponse)
async def get_active_assigned_miqaat_duties(
    payload: TeamDutyRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        team_id = payload.team_id
        
        logger.info(
            f"Active assigned miqaat duties requested by user {current_user.get('its_id')} "
            f"for team_id: {team_id}"
        )
        
        with get_db_connection() as conn:
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_duty_queries",
                {
                    "p_query_type": "ACTIVE-ASSIGNED-MIQAAT-DUTY",
                    "p_team_id": team_id,
                    "p_its_id": None,
                    "p_duty_id": None,
                    "p_jamiaat_id": None
                }
            )
            
            logger.debug(f"Function result: {result}")
            
            if result:
                if isinstance(result, str):
                    result = json.loads(result)
                
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
    try:
        its_id = payload.its_id
        
        logger.info(
            f"Guard duties requested by user {current_user.get('its_id')} "
            f"for its_id: {its_id}"
        )
        
        with get_db_connection() as conn:
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_duty_queries",
                {
                    "p_query_type": "GUARD-DUTIES-ASSIGNED",
                    "p_team_id": None,
                    "p_its_id": its_id,
                    "p_duty_id": None,
                    "p_jamiaat_id": None
                }
            )
            
            logger.debug(f"Function result: {result}")
            
            if result:
                if isinstance(result, str):
                    result = json.loads(result)
                
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
# GET ALL DUTIES
# ============================================================================

@router.get("/GetAllDuties", response_model=DutyResponse)
async def get_all_duties(current_user: dict = Depends(get_current_user)):

    try:
        logger.info(f"Get all duties requested by user {current_user.get('its_id')}")
        
        with get_db_connection() as conn:
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_duty_queries",
                {
                    "p_query_type": "GET-ALL-DUTIES",
                    "p_team_id": None,
                    "p_its_id": None,
                    "p_duty_id": None,
                    "p_jamiaat_id": None
                }
            )
            
            logger.debug(f"Function result: {result}")
            
            if result:
                if isinstance(result, str):
                    result = json.loads(result)
                
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
        logger.error(f"Error retrieving all duties: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# GET DUTY BY ID
# ============================================================================

@router.post("/GetDutyById", response_model=DutyResponse)
async def get_duty_by_id(
    payload: DutyByIdRequest,
    current_user: dict = Depends(get_current_user)
):

    try:
        duty_id = payload.duty_id
        
        logger.info(
            f"Get duty by ID requested by user {current_user.get('its_id')} "
            f"for duty_id: {duty_id}"
        )
        
        with get_db_connection() as conn:
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_duty_queries",
                {
                    "p_query_type": "GET-DUTY-BY-ID",
                    "p_team_id": None,
                    "p_its_id": None,
                    "p_duty_id": duty_id,
                    "p_jamiaat_id": None
                }
            )
            
            logger.debug(f"Function result: {result}")
            
            if result:
                if isinstance(result, str):
                    result = json.loads(result)
                
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
        logger.error(f"Error retrieving duty by ID: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# GET TEAMS BY JAMIAAT
# ============================================================================

@router.post("/GetTeamsByJamiaat", response_model=DutyResponse)
async def get_teams_by_jamiaat(
    payload: TeamsByJamiaatRequest,
    current_user: dict = Depends(get_current_user)
):

    try:
        jamiaat_id = payload.jamiaat_id
        
        logger.info(
            f"Get teams by jamiaat requested by user {current_user.get('its_id')} "
            f"for jamiaat_id: {jamiaat_id}"
        )
        
        with get_db_connection() as conn:
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_duty_queries",
                {
                    "p_query_type": "GET-TEAMS-BY-JAMIAAT",
                    "p_team_id": None,
                    "p_its_id": None,
                    "p_duty_id": None,
                    "p_jamiaat_id": jamiaat_id
                }
            )
            
            logger.debug(f"Function result: {result}")
            
            if result:
                if isinstance(result, str):
                    result = json.loads(result)
                
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
        logger.error(f"Error retrieving teams by jamiaat: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# GET LIST OF ACTIVE MIQAAT
# ============================================================================

@router.get("/GetListOfActiveMiqaat", response_model=DutyResponse)
async def get_list_of_active_miqaat(current_user: dict = Depends(get_current_user)):

    try:
        logger.info(f"Get list of active miqaat requested by user {current_user.get('its_id')}")
        
        with get_db_connection() as conn:
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_duty_queries",
                {
                    "p_query_type": "GET-LIST-OF-ACTIVE-MIQAAT",
                    "p_team_id": None,
                    "p_its_id": None,
                    "p_duty_id": None,
                    "p_jamiaat_id": None
                }
            )
            
            logger.debug(f"Function result: {result}")
            
            if result:
                if isinstance(result, str):
                    result = json.loads(result)
                
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
        logger.error(f"Error retrieving active miqaat list: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# DUTY CRUD OPERATIONS
# ============================================================================

# ============================================================================
# INSERT DUTY
# ============================================================================

@router.post("/InsertDuty", response_model=DutyCRUDResponse)
async def insert_duty(
    payload: DutyInsertRequest,
    current_user: dict = Depends(get_current_user)
):

    try:
        user_id = current_user.get("its_id")
        
        logger.info(
            f"Insert duty requested by user {user_id}: "
            f"team_id={payload.team_id}, miqaat_id={payload.miqaat_id}, "
            f"location={payload.location}"
        )
        
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT * FROM {PG_CONFIG['schema']}.spr_duty_insert(
                        %s, %s, %s, %s, %s, %s
                    )
                    """,
                    (
                        'Duty_Management',      # p_form_name
                        user_id,                # p_user_id
                        payload.team_id,        # p_team_id
                        payload.miqaat_id,      # p_miqaat_id
                        payload.quota,          # p_quota
                        payload.location        # p_location
                    )
                )
                
                result = cursor.fetchone()
                result_code = result[0] if result else 0
                
                logger.info(f"Duty insert result code: {result_code}")
                
                conn.commit()
                
                if result_code == 1:
                    return DutyCRUDResponse(
                        success=True,
                        status_code=201,
                        message="Duty created successfully",
                        data={"result_code": result_code}
                    )
                elif result_code == 4:
                    return DutyCRUDResponse(
                        success=False,
                        status_code=409,
                        message="Duty already exists with same team, miqaat, and location",
                        data={"result_code": result_code}
                    )
                else:
                    return DutyCRUDResponse(
                        success=False,
                        status_code=500,
                        message="Failed to create duty",
                        data={"result_code": result_code}
                    )
            
    except Exception as ex:
        logger.error(f"Error inserting duty: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# UPDATE DUTY
# ============================================================================

@router.put("/UpdateDuty", response_model=DutyCRUDResponse)
async def update_duty(
    payload: DutyUpdateRequest,
    current_user: dict = Depends(get_current_user)
):

    try:
        user_id = current_user.get("its_id")
        
        logger.info(
            f"Update duty requested by user {user_id}: "
            f"duty_id={payload.duty_id}"
        )
        
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT * FROM {PG_CONFIG['schema']}.spr_duty_update(
                        %s, %s, %s, %s, %s, %s, %s
                    )
                    """,
                    (
                        'Duty_Management',      # p_form_name
                        user_id,                # p_user_id
                        payload.duty_id,        # p_duty_id
                        payload.team_id,        # p_team_id
                        payload.miqaat_id,      # p_miqaat_id
                        payload.quota,          # p_quota
                        payload.location        # p_location
                    )
                )
                
                result = cursor.fetchone()
                result_code = result[0] if result else 0
                
                logger.info(f"Duty update result code: {result_code}")
                
                conn.commit()
                
                if result_code == 2:
                    return DutyCRUDResponse(
                        success=True,
                        status_code=200,
                        message="Duty updated successfully",
                        data={"result_code": result_code}
                    )
                elif result_code == 4:
                    return DutyCRUDResponse(
                        success=False,
                        status_code=409,
                        message="Duty already exists with same team, miqaat, and location for another duty",
                        data={"result_code": result_code}
                    )
                elif result_code == 0:
                    return DutyCRUDResponse(
                        success=False,
                        status_code=404,
                        message="Duty not found or update failed",
                        data={"result_code": result_code}
                    )
                else:
                    return DutyCRUDResponse(
                        success=False,
                        status_code=500,
                        message="Failed to update duty",
                        data={"result_code": result_code}
                    )
            
    except Exception as ex:
        logger.error(f"Error updating duty: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# DELETE DUTY
# ============================================================================

@router.delete("/DeleteDuty", response_model=DutyCRUDResponse)
async def delete_duty(
    payload: DutyDeleteRequest,
    current_user: dict = Depends(get_current_user)
):

    try:
        user_id = current_user.get("its_id")
        
        logger.info(
            f"Delete duty requested by user {user_id}: "
            f"duty_id={payload.duty_id}"
        )
        
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT * FROM {PG_CONFIG['schema']}.spr_duty_delete(
                        %s, %s, %s
                    )
                    """,
                    (
                        'Duty_Management',      # p_form_name
                        user_id,                # p_user_id
                        payload.duty_id         # p_duty_id
                    )
                )
                
                result = cursor.fetchone()
                result_code = result[0] if result else 0
                
                logger.info(f"Duty delete result code: {result_code}")
                
                conn.commit()
                
                if result_code == 3:
                    return DutyCRUDResponse(
                        success=True,
                        status_code=200,
                        message="Duty deleted successfully",
                        data={"result_code": result_code}
                    )
                elif result_code == 0:
                    return DutyCRUDResponse(
                        success=False,
                        status_code=404,
                        message="Duty not found, already deleted, or delete failed",
                        data={"result_code": result_code}
                    )
                else:
                    return DutyCRUDResponse(
                        success=False,
                        status_code=500,
                        message="Failed to delete duty",
                        data={"result_code": result_code}
                    )
            
    except Exception as ex:
        logger.error(f"Error deleting duty: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# GUARD DUTY INSERT/DELETE
# ============================================================================

@router.post("/GuardDutyInsert", response_model=GuardDutyInsertResponse)
async def guard_duty_insert(
    payload: GuardDutyInsertRequest,
    current_user: dict = Depends(get_current_user)
):

    conn = None
    try:
        user_id = current_user.get("its_id")
        
        if payload.flag == 'I':
            if not all([payload.duty_id, payload.team_id, payload.miqaat_id, payload.its_id]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="INSERT operation requires: duty_id, team_id, miqaat_id, and its_id"
                )
            
            logger.info(
                f"Guard duty INSERT requested by user {user_id}: "
                f"duty_id={payload.duty_id}, team_id={payload.team_id}, "
                f"miqaat_id={payload.miqaat_id}, its_id={payload.its_id}"
            )
        
        elif payload.flag == 'D':
            if not payload.guard_duty_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="DELETE operation requires: guard_duty_id"
                )
            
            logger.info(
                f"Guard duty DELETE requested by user {user_id}: "
                f"guard_duty_id={payload.guard_duty_id}"
            )
        
        conn = psycopg2.connect(
            host=PG_CONFIG['host'],
            database=PG_CONFIG['database'],
            user=PG_CONFIG['user'],
            password=PG_CONFIG['password'],
            port=PG_CONFIG['port']
        )
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(
            """
            SELECT o_result 
            FROM bg.spr_guard_duty_insert(
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            """,
            (
                payload.form_name,
                payload.flag,
                user_id,
                payload.duty_id,
                payload.team_id,
                payload.miqaat_id,
                payload.its_id,
                payload.guard_duty_id
            )
        )
        
        result = cursor.fetchone()
        result_value = result['o_result'] if result else 0
        
        cursor.close()
        
        if result_value == 1:
            conn.commit()
            logger.info(f"Guard duty INSERT successful")
            
            return GuardDutyInsertResponse(
                success=True,
                status_code=201,
                message="Guard duty assigned successfully",
                result=1
            )
        
        elif result_value == 3:
            conn.commit()
            logger.info(f"Guard duty DELETE successful")
            
            return GuardDutyInsertResponse(
                success=True,
                status_code=200,
                message="Guard duty removed successfully",
                result=3
            )
        
        elif result_value == 4:
            conn.rollback()
            logger.warning(f"Duplicate guard duty assignment attempt")
            
            return GuardDutyInsertResponse(
                success=False,
                status_code=409,
                message="Guard already assigned to this duty",
                result=4
            )
        
        else:
            conn.rollback()
            logger.error(f"Guard duty operation failed with result={result_value}")
            
            return GuardDutyInsertResponse(
                success=False,
                status_code=500,
                message="Failed to process guard duty operation",
                result=0
            )
    
    except HTTPException:
        raise
    
    except Exception as ex:
        if conn:
            conn.rollback()
        
        logger.error(f"Unexpected error in guard_duty_insert: {str(ex)}")
        logger.error(traceback.format_exc())
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )
    
    finally:
        if conn:
            conn.close()


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
            "GET /Duty/GetAllDuties",
            "POST /Duty/GetDutyById",
            "POST /Duty/GetTeamsByJamiaat",
            "GET /Duty/GetListOfActiveMiqaat",
            "POST /Duty/InsertDuty",
            "PUT /Duty/UpdateDuty",
            "DELETE /Duty/DeleteDuty",
            "POST /Duty/GuardDutyInsert"
        ]
    }