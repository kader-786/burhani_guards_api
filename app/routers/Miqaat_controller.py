# app/routers/Miqaat_controller.py
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.miqaat import (
    MiqaatRequest,
    JamaatsByJamiaatMiqaatRequest,
    MiqaatInsertRequest,
    MiqaatUpdateRequest,
    MiqaatDeleteRequest,
    MiqaatResponse
)

from app.db import get_db_connection, call_function
from app.config import PG_CONFIG
from app.auth import get_current_user
import traceback
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/Miqaat", tags=["Miqaat"])


# ============================================================================
# GET ALL MIQAAT
# ============================================================================

@router.get("/GetAllMiqaat", response_model=MiqaatResponse)
async def get_all_miqaat(current_user: dict = Depends(get_current_user)):
    try:
        logger.info(f"Get all miqaat requested by user {current_user.get('its_id')}")
        
        with get_db_connection() as conn:
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_miqaat_master",
                {
                    "p_query_type": "GET-ALL-MIQAAT",
                    "p_miqaat_id": None,    # Explicitly pass None
                    "p_jamiaat_id": None    # Explicitly pass None
                }
            )
            
            logger.debug(f"Function result: {result}")
            
            if result:
                if isinstance(result, str):
                    result = json.loads(result)
                
                if isinstance(result, dict):
                    return MiqaatResponse(
                        success=result.get("success", False),
                        status_code=result.get("status_code", 200),
                        message=result.get("message", "Query executed"),
                        data=result.get("data", None)
                    )
                else:
                    return MiqaatResponse(
                        success=False,
                        status_code=500,
                        message="Invalid response format from database",
                        data=None
                    )
            else:
                return MiqaatResponse(
                    success=False,
                    status_code=500,
                    message="No response from database",
                    data=None
                )
            
    except Exception as ex:
        logger.error(f"Error retrieving all miqaat: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# GET MIQAAT BY ID
# ============================================================================

@router.post("/GetMiqaatById", response_model=MiqaatResponse)
async def get_miqaat_by_id(
    payload: MiqaatRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        miqaat_id = payload.miqaat_id
        
        logger.info(
            f"Get miqaat by ID requested by user {current_user.get('its_id')} "
            f"for miqaat_id: {miqaat_id}"
        )
        
        with get_db_connection() as conn:
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_miqaat_master",
                {
                    "p_query_type": "GET-MIQAAT-BY-ID",
                    "p_miqaat_id": miqaat_id,
                    "p_jamiaat_id": None    # Explicitly pass None
                }
            )
            
            logger.debug(f"Function result: {result}")
            
            if result:
                if isinstance(result, str):
                    result = json.loads(result)
                
                if isinstance(result, dict):
                    return MiqaatResponse(
                        success=result.get("success", False),
                        status_code=result.get("status_code", 200),
                        message=result.get("message", "Query executed"),
                        data=result.get("data", None)
                    )
                else:
                    return MiqaatResponse(
                        success=False,
                        status_code=500,
                        message="Invalid response format from database",
                        data=None
                    )
            else:
                return MiqaatResponse(
                    success=False,
                    status_code=500,
                    message="No response from database",
                    data=None
                )
            
    except Exception as ex:
        logger.error(f"Error retrieving miqaat by ID: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# GET ALL MIQAAT TYPES
# ============================================================================

@router.get("/GetAllMiqaatTypes", response_model=MiqaatResponse)
async def get_all_miqaat_types(current_user: dict = Depends(get_current_user)):
    try:
        logger.info(f"Get all miqaat types requested by user {current_user.get('its_id')}")
        
        with get_db_connection() as conn:
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_miqaat_master",
                {
                    "p_query_type": "GET-ALL-MIQAAT-TYPE",
                    "p_miqaat_id": None,    # Explicitly pass None
                    "p_jamiaat_id": None    # Explicitly pass None
                }
            )
            
            logger.debug(f"Function result: {result}")
            
            if result:
                if isinstance(result, str):
                    result = json.loads(result)
                
                if isinstance(result, dict):
                    return MiqaatResponse(
                        success=result.get("success", False),
                        status_code=result.get("status_code", 200),
                        message=result.get("message", "Query executed"),
                        data=result.get("data", None)
                    )
                else:
                    return MiqaatResponse(
                        success=False,
                        status_code=500,
                        message="Invalid response format from database",
                        data=None
                    )
            else:
                return MiqaatResponse(
                    success=False,
                    status_code=500,
                    message="No response from database",
                    data=None
                )
            
    except Exception as ex:
        logger.error(f"Error retrieving miqaat types: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# GET JAMAATS BY JAMIAAT (FOR MIQAAT)
# ============================================================================

@router.post("/GetJamaatsByJamiaat", response_model=MiqaatResponse)
async def get_jamaats_by_jamiaat(
    payload: JamaatsByJamiaatMiqaatRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        jamiaat_id = payload.jamiaat_id
        
        logger.info(
            f"Get jamaats by jamiaat requested by user {current_user.get('its_id')} "
            f"for jamiaat_id: {jamiaat_id}"
        )
        
        with get_db_connection() as conn:
            result = call_function(
                conn,
                f"{PG_CONFIG['schema']}.spr_miqaat_master",
                {
                    "p_query_type": "GET-JAMAAT-BY-JAMIAAT",
                    "p_miqaat_id": None,        # Explicitly pass None
                    "p_jamiaat_id": jamiaat_id
                }
            )
            
            logger.debug(f"Function result: {result}")
            
            if result:
                if isinstance(result, str):
                    result = json.loads(result)
                
                if isinstance(result, dict):
                    return MiqaatResponse(
                        success=result.get("success", False),
                        status_code=result.get("status_code", 200),
                        message=result.get("message", "Query executed"),
                        data=result.get("data", None)
                    )
                else:
                    return MiqaatResponse(
                        success=False,
                        status_code=500,
                        message="Invalid response format from database",
                        data=None
                    )
            else:
                return MiqaatResponse(
                    success=False,
                    status_code=500,
                    message="No response from database",
                    data=None
                )
            
    except Exception as ex:
        logger.error(f"Error retrieving jamaats by jamiaat: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# INSERT MIQAAT
# ============================================================================

@router.post("/InsertMiqaat", response_model=MiqaatResponse)
async def insert_miqaat(
    payload: MiqaatInsertRequest,
    current_user: dict = Depends(get_current_user)
):

    try:
        user_id = current_user.get("its_id")
        
        logger.info(
            f"Insert miqaat requested by user {user_id}: "
            f"miqaat_name={payload.miqaat_name}"
        )
        
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT * FROM {PG_CONFIG['schema']}.spr_miqaat_master_insert(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    """,
                    (
                        'Miqaat_Management',        # p_form_name
                        user_id,                    # p_user_id
                        payload.miqaat_name,        # p_miqaat_name
                        payload.miqaat_type_id,     # p_miqaat_type_id
                        payload.start_date,         # p_start_date
                        payload.end_date,           # p_end_date
                        payload.venue,              # p_venue
                        payload.jamaat_id,          # p_jamaat_id
                        payload.jamiaat_id,         # p_jamiaat_id
                        payload.quantity,           # p_quantity
                        payload.is_active,          # p_is_active
                        payload.reporting_time      # p_reporting_time
                    )
                )
                
                result = cursor.fetchone()
                result_code = result[0] if result else 0
                
                logger.info(f"Miqaat insert result code: {result_code}")
                
                conn.commit()
                
                if result_code == 1:
                    return MiqaatResponse(
                        success=True,
                        status_code=201,
                        message="Miqaat inserted successfully",
                        data={"result_code": result_code}
                    )
                elif result_code == 4:
                    return MiqaatResponse(
                        success=False,
                        status_code=409,
                        message="Miqaat name already exists",
                        data={"result_code": result_code}
                    )
                else:
                    return MiqaatResponse(
                        success=False,
                        status_code=500,
                        message="Failed to insert miqaat",
                        data={"result_code": result_code}
                    )
            
    except Exception as ex:
        logger.error(f"Error inserting miqaat: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# UPDATE MIQAAT
# ============================================================================

@router.put("/UpdateMiqaat", response_model=MiqaatResponse)
async def update_miqaat(
    payload: MiqaatUpdateRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user.get("its_id")
        
        logger.info(
            f"Update miqaat requested by user {user_id}: "
            f"miqaat_id={payload.miqaat_id}"
        )
        
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT * FROM {PG_CONFIG['schema']}.spr_miqaat_master_update(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    """,
                    (
                        'Miqaat_Management',        # p_form_name
                        user_id,                    # p_user_id
                        payload.miqaat_id,          # p_miqaat_id
                        payload.miqaat_name,        # p_miqaat_name
                        payload.miqaat_type_id,     # p_miqaat_type_id
                        payload.start_date,         # p_start_date
                        payload.end_date,           # p_end_date
                        payload.venue,              # p_venue
                        payload.jamaat_id,          # p_jamaat_id
                        payload.jamiaat_id,         # p_jamiaat_id
                        payload.quantity,           # p_quantity
                        payload.is_active,          # p_is_active
                        payload.reporting_time      # p_reporting_time
                    )
                )
                
                result = cursor.fetchone()
                result_code = result[0] if result else 0
                
                logger.info(f"Miqaat update result code: {result_code}")
                
                conn.commit()
                
                if result_code == 2:
                    return MiqaatResponse(
                        success=True,
                        status_code=200,
                        message="Miqaat updated successfully",
                        data={"result_code": result_code}
                    )
                elif result_code == 4:
                    return MiqaatResponse(
                        success=False,
                        status_code=409,
                        message="Miqaat name already exists for another miqaat",
                        data={"result_code": result_code}
                    )
                elif result_code == 0:
                    return MiqaatResponse(
                        success=False,
                        status_code=404,
                        message="Miqaat not found or update failed",
                        data={"result_code": result_code}
                    )
                else:
                    return MiqaatResponse(
                        success=False,
                        status_code=500,
                        message="Failed to update miqaat",
                        data={"result_code": result_code}
                    )
            
    except Exception as ex:
        logger.error(f"Error updating miqaat: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# DELETE MIQAAT
# ============================================================================

@router.delete("/DeleteMiqaat", response_model=MiqaatResponse)
async def delete_miqaat(
    payload: MiqaatDeleteRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user.get("its_id")
        
        logger.info(
            f"Delete miqaat requested by user {user_id}: "
            f"miqaat_id={payload.miqaat_id}"
        )
        
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT * FROM {PG_CONFIG['schema']}.spr_miqaat_master_delete(
                        %s, %s, %s
                    )
                    """,
                    (
                        'Miqaat_Management',    # p_form_name
                        user_id,                # p_user_id
                        payload.miqaat_id       # p_miqaat_id
                    )
                )
                
                result = cursor.fetchone()
                result_code = result[0] if result else 0
                
                logger.info(f"Miqaat delete result code: {result_code}")
                
                conn.commit()
                
                if result_code == 3:
                    return MiqaatResponse(
                        success=True,
                        status_code=200,
                        message="Miqaat deleted successfully",
                        data={"result_code": result_code}
                    )
                elif result_code == 0:
                    return MiqaatResponse(
                        success=False,
                        status_code=404,
                        message="Miqaat not found, already deleted, or delete failed",
                        data={"result_code": result_code}
                    )
                else:
                    return MiqaatResponse(
                        success=False,
                        status_code=500,
                        message="Failed to delete miqaat",
                        data={"result_code": result_code}
                    )
            
    except Exception as ex:
        logger.error(f"Error deleting miqaat: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def miqaat_health_check():
    """
    Health check for Miqaat endpoints
    
    Public endpoint - no authentication required
    """
    return {
        "status": "healthy",
        "service": "Miqaat Management",
        "endpoints": [
            "GET /Miqaat/GetAllMiqaat",
            "POST /Miqaat/GetMiqaatById",
            "GET /Miqaat/GetAllMiqaatTypes",
            "POST /Miqaat/GetJamaatsByJamiaat",
            "POST /Miqaat/InsertMiqaat",
            "PUT /Miqaat/UpdateMiqaat",
            "DELETE /Miqaat/DeleteMiqaat"
        ]
    }