from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.login import Login
from app.db import get_db_connection
import traceback
from typing import List, Dict, Any
from decimal import Decimal
import math

router = APIRouter(prefix="/Login", tags=["Login"])


def execute_sp(conn, proc_name: str, params: dict) -> list[dict]:
    """Execute a stored procedure and return a list of dictionaries (rows)."""
    param_values = list(params.values())
    param_names = [f"{k}=?" for k in params]
    sql = f"EXEC {proc_name} {', '.join(param_names)}"

    with conn.cursor() as cursor:
        cursor.execute(sql, param_values)

        if not cursor.description:
            return []

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


@router.post("/Checklogin")
def check_login(payload: Login):
    try:
        with get_db_connection() as conn:
            result = execute_sp(conn, "COM_SPR_LOGIN", {
                "@Query_Type": "CHECK_LOGIN",
                "@User_Name": payload.UserName,
                "@Password": payload.Password
            })
            return {"Table": result}
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))
