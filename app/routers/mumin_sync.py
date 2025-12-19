# app/routers/mumin_sync.py
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import traceback
from datetime import datetime
from typing import Optional
import os

# Import models
from app.models.mumin_sync import MuminSyncRequest, MuminSyncResponse

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/mumin", tags=["Mumin Sync"])

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "your_database")
DB_USER = os.getenv("DB_USER", "your_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")

# HandlerB2 API Configuration
HANDLERB2_URL = os.getenv("HANDLERB2_URL", "http://13.204.161.209:8080/BURHANI_GUARDS_API_TEST/api/ITS-API/HandlerB2")
HANDLERB2_AUTH_TOKEN = os.getenv("HANDLERB2_AUTH_TOKEN", "your_auth_token")
HANDLERB2_HCODE = os.getenv("HANDLERB2_HCODE", "your_hcode")
HANDLERB2_DATA_OUTPUT = os.getenv("HANDLERB2_DATA_OUTPUT", "JSON")


def get_db_connection():
    """Create database connection"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise


def extract_last_4_digits(mobile: str) -> str:
    """Extract last 4 digits from mobile number for password"""
    if not mobile:
        return "0000"
    
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, mobile))
    
    # Get last 4 digits
    if len(digits) >= 4:
        return digits[-4:]
    else:
        # If less than 4 digits, pad with zeros
        return digits.zfill(4)


def call_handlerb2_api(its_id: str) -> dict:
    """Call HandlerB2 API to get member data"""
    try:
        # Prepare request data
        request_data = {
            "Auth_Token": HANDLERB2_AUTH_TOKEN,
            "HCode": HANDLERB2_HCODE,
            "Data_Output": HANDLERB2_DATA_OUTPUT,
            "Param1": its_id
        }
        
        logger.info(f"Calling HandlerB2 API for ITS_ID: {its_id}")
        
        response = requests.post(
            HANDLERB2_URL,
            data=request_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if data exists
            if data and "Table" in data and len(data["Table"]) > 0:
                return data["Table"][0]
            else:
                logger.error(f"No data found for ITS_ID: {its_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No data found for ITS_ID: {its_id}"
                )
        else:
            logger.error(f"HandlerB2 API error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"External API error: {response.status_code}"
            )
            
    except requests.exceptions.Timeout:
        logger.error(f"HandlerB2 API timeout for ITS_ID: {its_id}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="External API request timed out"
        )
    except requests.exceptions.ConnectionError:
        logger.error(f"HandlerB2 API connection error for ITS_ID: {its_id}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cannot connect to external API"
        )


def transform_api_data(api_data: dict) -> dict:
    """Transform API data to match database schema"""
    
    # Extract mobile number for password
    mobile = api_data.get("Mobile", "")
    password = extract_last_4_digits(mobile)
    
    # Convert float IDs to integers
    jamaat_id = api_data.get("Jamaat_ID")
    jamiaat_id = api_data.get("Jamiaat_ID")
    
    # Convert to int, default to 0 if None or invalid
    try:
        jamaat_id = int(float(jamaat_id)) if jamaat_id else 0
    except (ValueError, TypeError):
        jamaat_id = 0
    
    try:
        jamiaat_id = int(float(jamiaat_id)) if jamiaat_id else 0
    except (ValueError, TypeError):
        jamiaat_id = 0
    
    # Build the transformed data dictionary
    transformed_data = {
        "its_id": api_data.get("ITS_ID"),
        "full_name": api_data.get("Fullname"),
        "full_name_arabi": api_data.get("Arabic_Fullname"),
        "prefix": api_data.get("Prefix"),
        "age": api_data.get("Age"),
        "gender": api_data.get("Gender"),
        "marital_status": api_data.get("Marital_Status"),
        "misaq": api_data.get("Misaq"),
        "idara": api_data.get("Idara"),
        "category": api_data.get("Category"),
        "organization": api_data.get("Organization"),
        "email": api_data.get("Email"),
        "mobile": mobile,
        "whatsapp_mobil": api_data.get("WhatsApp_No"),
        "address": api_data.get("Address"),
        "jamaat_id": jamaat_id,
        "jamaat": api_data.get("Jamaat"),
        "jamiaat_id": jamiaat_id,
        "jamiaat": api_data.get("Jamiaat"),
        "nationality": api_data.get("Nationality"),
        "vatan": api_data.get("Vatan"),
        "city": api_data.get("City"),
        "country": api_data.get("Country"),
        # User-specified values
        "team_id": -1,
        "position_id": 10,
        "role_id": 4,
        "joining_date": None,  # NULL
        "status": 1,
        "password": password,
        "pull_date": datetime.now()
    }
    
    return transformed_data


def check_member_exists(conn, its_id: str) -> bool:
    """Check if member already exists in database"""
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT its_id FROM mumin_master WHERE its_id = %s",
                (its_id,)
            )
            result = cursor.fetchone()
            return result is not None
    except Exception as e:
        logger.error(f"Error checking member existence: {str(e)}")
        raise


def insert_member(conn, data: dict) -> None:
    """Insert new member into database"""
    try:
        with conn.cursor() as cursor:
            insert_query = """
                INSERT INTO mumin_master (
                    its_id, full_name, full_name_arabi, prefix, age, gender,
                    marital_status, misaq, idara, category, organization,
                    email, mobile, whatsapp_mobil, address, jamaat_id, jamaat,
                    jamiaat_id, jamiaat, nationality, vatan, city, country,
                    team_id, position_id, role_id, joining_date, status,
                    password, pull_date
                ) VALUES (
                    %(its_id)s, %(full_name)s, %(full_name_arabi)s, %(prefix)s, %(age)s, %(gender)s,
                    %(marital_status)s, %(misaq)s, %(idara)s, %(category)s, %(organization)s,
                    %(email)s, %(mobile)s, %(whatsapp_mobil)s, %(address)s, %(jamaat_id)s, %(jamaat)s,
                    %(jamiaat_id)s, %(jamiaat)s, %(nationality)s, %(vatan)s, %(city)s, %(country)s,
                    %(team_id)s, %(position_id)s, %(role_id)s, %(joining_date)s, %(status)s,
                    %(password)s, %(pull_date)s
                )
            """
            cursor.execute(insert_query, data)
            conn.commit()
            logger.info(f"Member inserted successfully: {data['its_id']}")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error inserting member: {str(e)}")
        raise


def update_member(conn, data: dict) -> None:
    """Update existing member in database"""
    try:
        with conn.cursor() as cursor:
            update_query = """
                UPDATE mumin_master SET
                    full_name = %(full_name)s,
                    full_name_arabi = %(full_name_arabi)s,
                    prefix = %(prefix)s,
                    age = %(age)s,
                    gender = %(gender)s,
                    marital_status = %(marital_status)s,
                    misaq = %(misaq)s,
                    idara = %(idara)s,
                    category = %(category)s,
                    organization = %(organization)s,
                    email = %(email)s,
                    mobile = %(mobile)s,
                    whatsapp_mobil = %(whatsapp_mobil)s,
                    address = %(address)s,
                    jamaat_id = %(jamaat_id)s,
                    jamaat = %(jamaat)s,
                    jamiaat_id = %(jamiaat_id)s,
                    jamiaat = %(jamiaat)s,
                    nationality = %(nationality)s,
                    vatan = %(vatan)s,
                    city = %(city)s,
                    country = %(country)s,
                    team_id = %(team_id)s,
                    position_id = %(position_id)s,
                    role_id = %(role_id)s,
                    status = %(status)s,
                    password = %(password)s,
                    pull_date = %(pull_date)s
                WHERE its_id = %(its_id)s
            """
            cursor.execute(update_query, data)
            conn.commit()
            logger.info(f"Member updated successfully: {data['its_id']}")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error updating member: {str(e)}")
        raise


@router.post("/sync-from-its", response_model=MuminSyncResponse)
async def sync_member_from_its(payload: MuminSyncRequest):
    """
    Sync member data from ITS API to mumin_master table
    
    This endpoint:
    1. Accepts ITS_ID as input
    2. Calls HandlerB2 API to fetch member data
    3. Transforms the data to match database schema
    4. Inserts new member or updates existing member
    5. Returns success/error response
    
    Password is generated from last 4 digits of mobile number.
    """
    conn = None
    
    try:
        its_id = payload.its_id
        
        logger.info(f"Starting sync process for ITS_ID: {its_id}")
        
        # Step 1: Call HandlerB2 API
        api_data = call_handlerb2_api(its_id)
        
        # Step 2: Transform data
        transformed_data = transform_api_data(api_data)
        
        # Step 3: Connect to database
        conn = get_db_connection()
        
        # Step 4: Check if member exists
        member_exists = check_member_exists(conn, its_id)
        
        # Step 5: Insert or Update
        if member_exists:
            update_member(conn, transformed_data)
            operation = "UPDATE"
            message = f"Member data updated successfully for ITS_ID: {its_id}"
        else:
            insert_member(conn, transformed_data)
            operation = "INSERT"
            message = f"Member data inserted successfully for ITS_ID: {its_id}"
        
        # Prepare response data
        response_data = {
            "its_id": transformed_data["its_id"],
            "full_name": transformed_data["full_name"],
            "mobile": transformed_data["mobile"],
            "email": transformed_data["email"],
            "jamaat": transformed_data["jamaat"],
            "jamiaat": transformed_data["jamiaat"]
        }
        
        logger.info(f"Sync completed successfully for ITS_ID: {its_id} - Operation: {operation}")
        
        return MuminSyncResponse(
            success=True,
            message=message,
            its_id=its_id,
            operation=operation,
            data=response_data
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except psycopg2.IntegrityError as e:
        logger.error(f"Database integrity error: {str(e)}")
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Database constraint violation: {str(e)}"
        )
        
    except psycopg2.Error as e:
        logger.error(f"Database error: {str(e)}")
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
        
    except Exception as e:
        logger.error(f"Unexpected error during sync: {str(e)}")
        logger.error(traceback.format_exc())
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
        
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")