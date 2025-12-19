# app/routers/ITS_API_controller.py
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.its_api import ITSAPIRequest, ITSAPIResponse
from app.auth import get_current_user
import requests
import traceback
import logging
import os
from dotenv import load_dotenv
import json
import xml.etree.ElementTree as ET

load_dotenv()
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ITS-API", tags=["ITS External API"])


# ============================================================================
# CONFIGURATION - Load from environment variables
# ============================================================================

# HandlerB2 Configuration
HANDLERB2_URL = os.getenv("HANDLERB2_URL", "https://api.its52.com/Services.asmx/HandlerB2")
HANDLERB2_AUTH_TOKEN = os.getenv("HANDLERB2_AUTH_TOKEN", "")
HANDLERB2_HCODE = os.getenv("HANDLERB2_HCODE", "")
HANDLERB2_DATA_OUTPUT = os.getenv("HANDLERB2_DATA_OUTPUT", "JSON")

# HandlerE1 Configuration
HANDLERE1_URL = os.getenv("HANDLERE1_URL", "https://api.its52.com/Services.asmx/HandlerE1")
HANDLERE1_AUTH_TOKEN = os.getenv("HANDLERE1_AUTH_TOKEN", "")
HANDLERE1_HCODE = os.getenv("HANDLERE1_HCODE", "")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_xml_response(xml_string: str) -> dict:
    """
    Parse XML response to dictionary
    Handles SOAP/XML responses from ITS API
    """
    try:
        # Remove XML declaration and parse
        root = ET.fromstring(xml_string)
        
        # Extract text content
        result = {}
        for child in root:
            result[child.tag] = child.text
        
        return result
    except Exception as e:
        logger.error(f"XML parsing error: {str(e)}")
        return {"raw": xml_string}


def parse_json_response(response_text: str) -> dict:
    """
    Parse JSON response
    """
    try:
        return json.loads(response_text)
    except Exception as e:
        logger.error(f"JSON parsing error: {str(e)}")
        return {"raw": response_text}


# ============================================================================
# ENDPOINT 1: HandlerB2
# ============================================================================

@router.post("/HandlerB2", response_model=ITSAPIResponse)
async def call_handlerb2_api(
    payload: ITSAPIRequest
    # current_user: dict = Depends(get_current_user)
):
    try:
        its_id = payload.its_id
        
        # Log the request
        # logger.info(f"HandlerB2 API called by user {current_user.get('its_id')} for ITS ID: {its_id}")
        
        # Validate configuration
        if not HANDLERB2_AUTH_TOKEN or not HANDLERB2_HCODE:
            logger.error("HandlerB2 API credentials not configured")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="External API credentials not configured. Contact administrator."
            )
        
        # Prepare request data
        request_data = {
            "Auth_Token": HANDLERB2_AUTH_TOKEN,
            "HCode": HANDLERB2_HCODE,
            "Data_Output": HANDLERB2_DATA_OUTPUT,
            "Param1": its_id
        }
        
        # Call external API
        logger.info(f"Calling HandlerB2 API: {HANDLERB2_URL}")
        
        response = requests.post(
            HANDLERB2_URL,
            data=request_data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            timeout=30  # 30 seconds timeout
        )
        
        # Log response status
        logger.info(f"HandlerB2 API response status: {response.status_code}")
        
        # Check if request was successful
        if response.status_code == 200:
            response_text = response.text
            
            # Parse response based on Data_Output format
            if HANDLERB2_DATA_OUTPUT.upper() == "JSON":
                parsed_data = parse_json_response(response_text)
            else:
                parsed_data = parse_xml_response(response_text)
            
            return ITSAPIResponse(
                success=True,
                message="Data retrieved successfully from HandlerB2",
                its_id=its_id,
                data=parsed_data,
                raw_response=response_text
            )
        else:
            # API returned error status
            logger.error(f"HandlerB2 API error: {response.status_code} - {response.text}")
            
            return ITSAPIResponse(
                success=False,
                message=f"External API returned error: {response.status_code}",
                its_id=its_id,
                data=None,
                raw_response=response.text
            )
    
    except requests.exceptions.Timeout:
        logger.error(f"HandlerB2 API timeout for ITS ID: {its_id}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="External API request timed out. Please try again."
        )
    
    except requests.exceptions.ConnectionError:
        logger.error(f"HandlerB2 API connection error for ITS ID: {its_id}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cannot connect to external API. Please try again later."
        )
    
    except Exception as ex:
        logger.error(f"HandlerB2 API error: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# ENDPOINT 2: HandlerE1
# ============================================================================

@router.post("/HandlerE1", response_model=ITSAPIResponse)
async def call_handlere1_api(
    payload: ITSAPIRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        its_id = payload.its_id
        
        # Log the request
        logger.info(f"HandlerE1 API called by user {current_user.get('its_id')} for ITS ID: {its_id}")
        
        # Validate configuration
        if not HANDLERE1_AUTH_TOKEN or not HANDLERE1_HCODE:
            logger.error("HandlerE1 API credentials not configured")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="External API credentials not configured. Contact administrator."
            )
        
        # Prepare request data
        request_data = {
            "Auth_Token": HANDLERE1_AUTH_TOKEN,
            "HCode": HANDLERE1_HCODE,
            "Param1": its_id
        }
        
        # Call external API
        logger.info(f"Calling HandlerE1 API: {HANDLERE1_URL}")
        
        response = requests.post(
            HANDLERE1_URL,
            data=request_data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            timeout=30  # 30 seconds timeout
        )
        
        # Log response status
        logger.info(f"HandlerE1 API response status: {response.status_code}")
        
        # Check if request was successful
        if response.status_code == 200:
            response_text = response.text
            
            # Parse response (typically XML from SOAP)
            parsed_data = parse_xml_response(response_text)
            
            return ITSAPIResponse(
                success=True,
                message="Data retrieved successfully from HandlerE1",
                its_id=its_id,
                data=parsed_data,
                raw_response=response_text
            )
        else:
            # API returned error status
            logger.error(f"HandlerE1 API error: {response.status_code} - {response.text}")
            
            return ITSAPIResponse(
                success=False,
                message=f"External API returned error: {response.status_code}",
                its_id=its_id,
                data=None,
                raw_response=response.text
            )
    
    except requests.exceptions.Timeout:
        logger.error(f"HandlerE1 API timeout for ITS ID: {its_id}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="External API request timed out. Please try again."
        )
    
    except requests.exceptions.ConnectionError:
        logger.error(f"HandlerE1 API connection error for ITS ID: {its_id}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cannot connect to external API. Please try again later."
        )
    
    except Exception as ex:
        logger.error(f"HandlerE1 API error: {str(ex)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(ex)}"
        )


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def its_api_health_check():
    """
    Health check for ITS API endpoints
    
    Public endpoint - no authentication required
    """
    return {
        "status": "healthy",
        "service": "ITS External API Integration",
        "endpoints": {
            "handlerb2": HANDLERB2_URL,
            "handlere1": HANDLERE1_URL
        },
        "configured": {
            "handlerb2": bool(HANDLERB2_AUTH_TOKEN and HANDLERB2_HCODE),
            "handlere1": bool(HANDLERE1_AUTH_TOKEN and HANDLERE1_HCODE)
        }
    }