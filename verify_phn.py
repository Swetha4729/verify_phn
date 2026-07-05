from typing import Any, Dict
import phonenumbers
from phonenumbers import geocoder, carrier
from fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP(name="Verify UK Phone Number", version="1.0.0")

@mcp.tool(
    description=(
        "Verifies a UK phone number using the libphonenumber library (phonenumbers package). "
        "Returns whether the number is valid, its formatted version, and carrier/region info if available."
    )
)
def verify_uk_phn(phone_number: str) -> Dict[str, Any]:
    """Verify a UK phone number and return details."""
    try:
        # "GB" is the ISO 3166-1 alpha-2 country code for the United Kingdom
        parsed_number = phonenumbers.parse(phone_number, "GB")
        
        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)
        
        if is_valid:
            # Get formatted versions of the number
            formatted_e164 = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            formatted_national = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
            formatted_international = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            
            # Get geographical and carrier info
            region = geocoder.description_for_number(parsed_number, "en")
            provider = carrier.name_for_number(parsed_number, "en")
            
            return {
                "status": "success",
                "isValid": is_valid,
                "isPossible": is_possible,
                "formatted": {
                    "e164": formatted_e164,
                    "national": formatted_national,
                    "international": formatted_international
                },
                "region": region,
                "carrier": provider,
                "countryCode": parsed_number.country_code,
                "nationalNumber": parsed_number.national_number
            }
        else:
            return {
                "status": "success",
                "isValid": False,
                "isPossible": is_possible,
                "message": "The phone number is not valid."
            }
            
    except phonenumbers.NumberParseException as e:
        return {
            "status": "error",
            "isValid": False,
            "message": f"Failed to parse phone number: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
