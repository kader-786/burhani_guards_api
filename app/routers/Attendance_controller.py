# app/routers/Attendance_controller.py
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.attendance import AttendanceInsertRequest, AttendanceResponse
from app.db import get_db_connection
from app.config import PG_CONFIG
from app.auth import get_current_user
import traceback
import logging
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/Attendance", tags=["Attendance"])


# ============================================================================
# INSERT ATTENDANCE RECORD
# ============================================================================

@router.post("/AttendanceInsert", response_model=AttendanceResponse)
async def attendance_insert(
    payload: AttendanceInsertRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        # Log the request
        logger.info(
            f"Attendance insert requested by user {current_user.get('its_id')} "
            f"for its_id: {payload.its_id}, miqaat_id: {payload.miqaat_id}, team_id: {payload.team_id}"
        )
        
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Call the PostgreSQL function
                # IMPORTANT: Pass all parameters explicitly
                cursor.execute(
                    f"SELECT * FROM {PG_CONFIG['schema']}.spr_attendance_insert(%s, %s, %s, %s, %s)",
                    (
                        payload.form_name,
                        payload.user_id,
                        payload.its_id,
                        payload.miqaat_id,
                        payload.team_id
                    )
                )
                
                # Fetch the result
                result_row = cursor.fetchone()
                
                if result_row:
                    result_value = result_row.get('o_result', 0)
                    
                    logger.info(f"Function returned result: {result_value}")
                    
                    # Interpret the result
                    if result_value == 1:
                        # Success - COMMIT the transaction
                        conn.commit()
                        logger.info(f"Attendance record committed: attendance for ITS {payload.its_id}")
                        return AttendanceResponse(
                            success=True,
                            status_code=200,
                            message="Attendance record inserted successfully",
                            result=result_value
                        )
                    elif result_value == 4:
                        # Duplicate entry - ROLLBACK the transaction
                        conn.rollback()
                        logger.warning(f"Duplicate attendance detected for ITS {payload.its_id}")
                        return AttendanceResponse(
                            success=False,
                            status_code=409,
                            message="Attendance record already exists for this member",
                            result=result_value
                        )
                    else:
                        # Failure (0 or other value) - ROLLBACK the transaction
                        conn.rollback()
                        logger.error(f"Attendance insert failed with result: {result_value}")
                        return AttendanceResponse(
                            success=False,
                            status_code=500,
                            message="Failed to insert attendance record",
                            result=result_value
                        )
                else:
                    # No result returned - ROLLBACK the transaction
                    conn.rollback()
                    logger.error("No result returned from database function")
                    return AttendanceResponse(
                        success=False,
                        status_code=500,
                        message="No response from database",
                        result=None
                    )
            
    except Exception as ex:
        # Rollback on any exception
        try:
            if 'conn' in locals():
                conn.rollback()
                logger.info("Transaction rolled back due to exception")
        except:
            pass
        
        logger.error(f"Error inserting attendance record: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def attendance_health_check():
    """
    Health check for Attendance endpoints
    
    Public endpoint - no authentication required
    """
    return {
        "status": "healthy",
        "service": "Attendance Management",
        "endpoints": [
            "POST /Attendance/AttendanceInsert",
            "POST /Attendance/InsertMyAttendance"
        ]
    }