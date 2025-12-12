from fastapi import APIRouter, HTTPException
from app.models.Activity import Activity
from app.db import get_db_connection, get_tds_connection
import traceback
# import pytds as tds
from pytds import TableValuedParam
import json

# from pytds.tds import ColumnMetaData, ColumnType, TableValuedParam
from decimal import Decimal
from typing import List, Dict, Any

router = APIRouter(prefix="/Activity", tags=["Activity"])

def execute_sp(conn, proc_name: str, params: dict) -> List[Dict[str, Any]]:
    """Execute a stored procedure and return the result set as a list of dictionaries."""
    param_values = list(params.values())
    param_names = [f"{k}=?" for k in params]
    sql = f"EXEC {proc_name} {', '.join(param_names)}"

    with conn.cursor() as cursor:
        cursor.execute(sql, param_values)

        if not cursor.description:
            return []

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

@router.post("/Get")
def get_all_activities(payload: Activity):
    try:
        with get_db_connection() as conn:
            result = execute_sp(conn, "SPR_ACTIVITY_MASTER", {
                "@QUERY_TYPE": "SELECT-ALL",
                "@TROOP_ID": payload.Troop_ID
            })
            return result
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/SelectByID")
def select_activity_by_id(payload: Activity):
    try:
        with get_db_connection() as conn:
            result = execute_sp(conn, "SPR_ACTIVITY_MASTER", {
                "@QUERY_TYPE": "SELECT-BY-ID",
                "@ACTIVITY_ID": payload.Activity_ID
            })
            return {"Table": result}
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/Insert")
def insert_activity(payload: Activity):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DECLARE @Result INT;
                    EXEC SPR_ACTIVITY_MASTER_INSERT_PY 
                        @Result = @Result OUTPUT,
                        @FORM_NAME = ?, 
                        @USER_ID = ?, 
                        @ACTIVITY_NAME = ?, 
                        @MEETING_ID = ?, 
                        @ACTIVITY_DATE = ?, 
                        @POINTS_TYPE_ID = ?, 
                        @MAX_POINTS = ?, 
                        @HAS_ROUNDS = ?, 
                        @ROUNDS = ?, 
                        @TROOP_ID = ?, 
                        @ACTIVITY_MASTER_DETAIL_JSON = ?;
                    SELECT @Result AS Result;
                """,
                payload.Form_Name,
                payload.User_ID,
                payload.Activity_Name,
                payload.Meeting_ID,
                payload.Activity_Date,
                payload.Points_Type_ID,
                payload.Max_Points,
                int(payload.Has_Rounds),
                payload.Rounds,
                payload.Troop_ID,
                payload.Activity_Master_Detail)

                while cursor.nextset():
                    if cursor.description:
                        break

                row = cursor.fetchone()
                return row[0]

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.get("/TestSelectAll")
def test_select_all_activity_master():
    try:
        with get_tds_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ACTIVITY_ROUNDS_LINK")
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            data = [dict(zip(columns, row)) for row in rows]
            return {"data": data}
    except Exception as e:
        import traceback
        print("Exception occurred:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/Update")
def update_activity(payload: Activity):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DECLARE @Result INT;
                    EXEC SPR_ACTIVITY_MASTER_UPDATE_PY 
                        @FORM_NAME = ?, 
                        @UserID = ?,
                        @USER_ID = ?, 
                        @ACTIVITY_ID = ?, 
                        @ACTIVITY_NAME = ?, 
                        @MEETING_ID = ?, 
                        @ACTIVITY_DATE = ?, 
                        @POINTS_TYPE_ID = ?, 
                        @MAX_POINTS = ?, 
                        @HAS_ROUNDS = ?, 
                        @ROUNDS = ?, 
                        @TROOP_ID = ?, 
                        @ACTIVITY_MASTER_DETAIL_JSON = ?,
                        @Result = @Result OUTPUT;
                    SELECT @Result AS Result;
                """,
                payload.Form_Name,
                payload.User_ID,
                payload.User_ID,
                payload.Activity_ID,
                payload.Activity_Name,
                payload.Meeting_ID,
                payload.Activity_Date,
                payload.Points_Type_ID,
                payload.Max_Points,
                int(payload.Has_Rounds),
                payload.Rounds,
                payload.Troop_ID,
                payload.Activity_Master_Detail  #a JSON string
                )

                while cursor.nextset():
                    if cursor.description:
                        break

                row = cursor.fetchone()
                return row[0]
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/Delete")
def delete_activity(payload: Activity):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                result = cursor.execute("""
                    DECLARE @Result INT;
                    EXEC SPR_ACTIVITY_MASTER_DELETE_PY
                        @FORM_NAME = ?, 
                        @USER_ID = ?, 
                        @ACTIVITY_ID = ?, 
                        @Result = @Result OUTPUT;
                    SELECT @Result AS Result;
                """,
                payload.Form_Name,
                payload.User_ID,
                payload.Activity_ID)

                while cursor.nextset():
                    if cursor.description:
                        break

                row = cursor.fetchone()
                return row[0] if row else 0
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))
