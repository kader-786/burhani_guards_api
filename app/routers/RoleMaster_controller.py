from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import pyodbc
import traceback
from app.db import get_db_connection
from app.models.RoleMaster import RoleMaster, Details

router = APIRouter(prefix="/RoleMaster", tags=["RoleMaster"])

def execute_sp_with_results(conn, sp_name: str, params: dict = None) -> List[Dict[str, Any]]:
    """Execute stored procedure and return results as list of dictionaries"""
    with conn.cursor() as cursor:
        sql = f"EXEC {sp_name}"
        param_values = []

        if params:
            for param, value in params.items():
                sql += f" {param}=?,"
                param_values.append(value)
            sql = sql.rstrip(',')

        cursor.execute(sql, param_values if params else None)

        columns = [column[0] for column in cursor.description] if cursor.description else []

        results = []
        for row in cursor.fetchall():
            row_dict = {}
            for i, column in enumerate(columns):
                value = row[i]
                if value is None:
                    row_dict[column] = None
                elif isinstance(value, (bytes, bytearray)):
                    row_dict[column] = value.hex()
                else:
                    row_dict[column] = value
            results.append(row_dict)

        return results

# API endpoints

@router.get("/role-get-module", response_model=List[Dict[str, Any]])
def get_module():
    try:
        with get_db_connection() as conn:
            results = execute_sp_with_results(conn, "COM_SPR_ROLE_MASTER", {
                "@Query_Type": "MODULE-SELECT-ALL"
            })
            return results
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/role-get-all", response_model=List[Dict[str, Any]])
def get_all_roles():
    try:
        with get_db_connection() as conn:
            results = execute_sp_with_results(conn, "COM_SPR_ROLE_MASTER", {
                "@Query_Type": "SELECT-ALL"
            })
            return results
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/role-by-id", response_model=List[Dict[str, Any]])
def get_role_by_id(payload: RoleMaster):
    try:
        with get_db_connection() as conn:
            results = execute_sp_with_results(conn, "COM_SPR_ROLE_MASTER", {
                "@Query_Type": "SELECT-BY-ID",
                "@ROLE_ID": payload.RoleId
            })
            return results if isinstance(results, list) else [results]
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/role-insert")
def insert_role(payload: RoleMaster):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                is_admin = 1 if str(payload.IsAdmin).strip().lower() in ("1", "true") else 0

                cursor.execute("""
                    DECLARE @Result NUMERIC;
                    EXEC COM_SPR_ROLE_MASTER_INSERT 
                        @Result = @Result OUTPUT,
                        @Form_Name = ?,
                        @UserID = ?,
                        @ROLE_ID = ?,
                        @ROLE_NAME = ?,
                        @ACCESS_RIGHTS = ?,
                        @IS_ADMIN = ?,
                        @REMARKS = ?;
                    SELECT @Result;
                """,
                payload.details.formName,
                payload.details.userId,
                payload.RoleId,
                payload.RoleName,
                payload.AccessRights,
                is_admin,
                payload.Remark
                )

                while cursor.nextset():
                    try:
                        result = cursor.fetchone()
                        if result:
                            return int(result[0])
                    except pyodbc.ProgrammingError:
                        continue

                return 0
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))

@router.put("/role-update")
def update_role(payload: RoleMaster):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                is_admin = 1 if str(payload.IsAdmin).strip().lower() in ("1", "true") else 0

                # Declare and execute the stored procedure
                cursor.execute("""
                    DECLARE @Result NUMERIC;
                    EXEC COM_SPR_ROLE_MASTER_UPDATE 
                        @Result = @Result OUTPUT,
                        @Form_Name = ?,
                        @UserID = ?,
                        @ROLE_ID = ?,
                        @ROLE_NAME = ?,
                        @ACCESS_RIGHTS = ?,
                        @IS_ADMIN = ?,
                        @REMARKS = ?;
                    SELECT @Result AS Result;
                """,
                payload.details.formName,
                payload.details.userId,
                payload.RoleId,
                payload.RoleName,
                payload.AccessRights,
                is_admin,
                payload.Remark
                )

                # Ensure we're on the final result set with SELECT @Result
                while cursor.nextset():
                    try:
                        row = cursor.fetchone()
                        if row and "Result" in cursor.description[0][0]:
                            return int(row[0])
                    except pyodbc.ProgrammingError:
                        continue

                return 0  # Default/fallback if nothing is returned
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/role-delete")
def delete_role(payload: RoleMaster):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Combine declaration, execution, and result selection in one statement
                sql = """
                DECLARE @Result INT;
                EXEC COM_SPR_ROLE_MASTER_DELETE 
                    @Result = @Result OUTPUT,
                    @Form_Name = ?,
                    @UserID = ?,
                    @ROLE_ID = ?;
                SELECT @Result AS Result;
                """
                
                # Execute all statements together
                cursor.execute(sql,
                    payload.details.formName,
                    payload.details.userId,
                    payload.RoleId
                )
                
                # Skip any empty result sets (from the EXEC)
                while cursor.nextset():
                    try:
                        result_row = cursor.fetchone()
                        if result_row and result_row[0] is not None:
                            return (int(result_row[0]))
                    except pyodbc.ProgrammingError:
                        continue
                
                return "0"
                
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))