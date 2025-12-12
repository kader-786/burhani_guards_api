from fastapi import APIRouter, HTTPException
from app.models.points import Points
from app.db import get_db_connection
import traceback
import pyodbc
from typing import List, Dict, Any
from decimal import Decimal
import math

router = APIRouter(prefix="/Points", tags=["Points"])

def execute_sp(conn, proc_name: str, params: dict) -> List[Dict[str, Any]]:
    """Execute a stored procedure and return the result set as a list of dictionaries.    """
    param_values = list(params.values())
    param_names = [f"{k}=?" for k in params]
    sql = f"EXEC {proc_name} {', '.join(param_names)}"

    with conn.cursor() as cursor:
        cursor.execute(sql, param_values)

        if not cursor.description:
            return []

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

@router.post("/GetIsActive")
def get_is_active(payload: Points):
    try:
        with get_db_connection() as conn:
            result = execute_sp(conn, "SPR_POINTS", {
                "@Query_Type": "SELECT-IS-ACTIVE",
                "@TROOP_ID": payload.Troop_ID
            })
            return {"Table": result}
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/GetActivity")
def get_activity(payload: Points):
    try:
        with get_db_connection() as conn:
            result = execute_sp(conn, "SPR_POINTS", {
                "@Query_Type": "SELECT-ACTIVITY",
                "@ACTIVITY_ID": payload.Activity_ID
            })
            return {"data": result}
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/GetRounds")
def get_rounds(payload: Points):
    try:
        with get_db_connection() as conn:
            result = execute_sp(conn, "SPR_POINTS", {
                "@Query_Type": "SELECT-HAS-ROUND",
                "@ACTIVITY_ID": payload.Activity_ID
            })
            return {"Table": result}
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))



@router.post("/Insert")
def insert_points(payload: Points):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Prepare output param
                result_param = cursor.execute("""
                    DECLARE @Result NUMERIC;
                    EXEC SPR_POINTS_INSERT 
                        @Result = @Result OUTPUT,
                        @FORM_NAME = ?, 
                        @MEETING_ID = ?, 
                        @USER_ID = ?, 
                        @PATROL_ID = ?, 
                        @ACTIVITY_ID = ?, 
                        @ROUND_ID = ?, 
                        @POINTS_TYPE_ID = ?, 
                        @POINTS = ?, 
                        @REMARKS = ?, 
                        @YEAR_ID = ?;
                    SELECT @Result AS Result;
                """, 
                payload.Form_Name,
                payload.Meeting_ID,
                payload.User_ID,
                payload.Patrol_ID,
                payload.Activity_ID if payload.Activity_ID else None,
                payload.Round_ID if payload.Round_ID else None,
                payload.Points_Type_ID,
                payload.Point,
                payload.Remarks,
                payload.Year_ID)

                # Advance to result set and fetch
                while cursor.nextset():
                    if cursor.description:  # only stop at a SELECT
                        break

                row = cursor.fetchone()
                return row[0]

    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))
