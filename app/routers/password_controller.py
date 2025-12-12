from fastapi import APIRouter, HTTPException
from app.models.password import Password, Details
from app.db import get_db_connection
import pyodbc
import traceback
from typing import List, Dict, Any
import json
import math
from decimal import Decimal

router = APIRouter(prefix="/Password", tags=["Password"])

# def execute_sp_with_results(conn, proc_name: str, params: dict) -> List[List[Dict]]:
#     """Execute SP and return all result sets as lists of dictionaries"""
#     results = []
#     with conn.cursor() as cursor:
#         sql = f"EXEC {proc_name}"
#         param_values = []

#         for param, value in params.items():
#             sql += f" {param}=?,"
#             param_values.append(value)
#         sql = sql.rstrip(',')

#         cursor.execute(sql, param_values)

#         while True:
#             if cursor.description:
#                 columns = [column[0] for column in cursor.description]
#                 table_data = []
#                 for row in cursor.fetchall():
#                     row_dict = {}
#                     for i, column in enumerate(columns):
#                         value = row[i]
#                         if value is None:
#                             row_dict[column] = None
#                         elif isinstance(value, (Decimal, float)):
#                             if math.isinf(value):
#                                 row_dict[column] = "Infinity"
#                             elif math.isnan(value):
#                                 row_dict[column] = "NaN"
#                             else:
#                                 row_dict[column] = float(value)
#                         else:
#                             row_dict[column] = str(value)
#                     table_data.append(row_dict)
#                 results.append(table_data)

#             if not cursor.nextset():
#                 break

#     return results


def execute_sp_with_results(conn, proc_name: str, params: dict) -> List[List[Dict]]:
    """Execute stored procedure and return all result sets as lists of dictionaries."""
    
    results = []
    param_values = list(params.values())
    param_names = [f"{name}=?" for name in params.keys()]
    sql = f"EXEC {proc_name} {', '.join(param_names)}" if params else f"EXEC {proc_name}"

    with conn.cursor() as cursor:
        cursor.execute(sql, param_values)

        while True:
            if not cursor.description:
                if not cursor.nextset():
                    break
                continue

            columns = [column[0] for column in cursor.description]
            table_data = [
                {
                    column: (row[i])
                    for i, column in enumerate(columns)
                }
                for row in cursor.fetchall()
            ]
            results.append(table_data)

            if not cursor.nextset():
                break

    return results

def _convert_value(value):
    """Convert database values to appropriate Python types."""
    if value is None:
        return None
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, float):
        if math.isinf(value):
            return "Infinity"
        if math.isnan(value):
            return "NaN"
    return str(value)

@router.post("/user-by-id")
def get_user_by_id(payload: Password):
    try:
        with get_db_connection() as conn:
            tables = execute_sp_with_results(conn, "COM_SPR_LOGIN", {
                "@Query_Type": "CHECK_LOGIN",
                "@User_Name": payload.UserName,
                "@Password": payload.Pass
            })


            response_data = {
                "Table1": tables[0] if len(tables) > 0 else [],
                "Table2": tables[1] if len(tables) > 1 else []
            }

            return response_data

    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/load-by-id")
def get_by_id(payload: Password):
    try:
        with get_db_connection() as conn:
            tables = execute_sp_with_results(conn, "COM_SPR_USER_MASTER", {
                "@Query_Type": "SELECT-BY-ID",
                "@USER_ID": payload.details.userId
            })

            return {"Table1": tables[0] if tables else []}

    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))


# With-context added here too
# @router.put("/password-update")
# def update_password(payload: Password):
#     try:
#         with get_db_connection() as conn:
#             with conn.cursor() as cursor:
#                 cursor.execute("""
#                     DECLARE @Result INT;
#                     EXEC COM_SPR_CHANGE_PASSWORD
#                         @Form_Name=?,
#                         @UserID=?,
#                         @USER_ID=?,
#                         @PASSWORD=?,
#                         @OLD_PASSWORD=?,
#                         @FULL_NAME=?,
#                         @MOBILE=?,
#                         @EMAIL=?,
#                         @Result=@Result OUTPUT;
#                     SELECT @Result AS Result;
#                     """,
#                     payload.details.formName,
#                     payload.details.userId,
#                     payload.details.userId,
#                     payload.New_Password or None,
#                     payload.Txt_Current_Password or None,
#                     payload.txt_FullName,
#                     payload.txt_mob,
#                     payload.txt_email
#                 )

#                 result = cursor.fetchone()
#                 return result[0] if result else 0

#     except Exception as ex:
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(ex))


# @router.post("/forget-password")
# def forget_password(payload: Password):
#     try:
#         with get_db_connection() as conn:
#             with conn.cursor() as cursor:
#                 cursor.execute("EXEC COM_SPR_FORGET_PASSWORD @Query_Type=?, @USER_NAME=?", 
#                             "RetrievePassword", payload.UserName)
#                 return 1

#     except Exception as ex:
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(ex))
