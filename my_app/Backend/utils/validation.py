"""
Input validation utilities for the Internship Recommendation System.
"""

from typing import Dict, List, Any, Optional
from utils.exceptions import ValidationError


def validate_candidate_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate the candidate profile structure and data.
    
    Args:
        profile: Dictionary containing candidate information
        
    Returns:
        Validated and sanitized profile dictionary
        
    Raises:
        ValidationError: If validation fails
        
    Example:
        >>> profile = {"Skills": ["Python", "Flask"], "Location": "Remote"}
        >>> validated = validate_candidate_profile(profile)
    """
    if not isinstance(profile, dict):
        raise ValidationError("Candidate profile must be a dictionary")
    
    # Validate Skills field
    if "Skills" in profile:
        skills = profile["Skills"]
        if not isinstance(skills, list):
            raise ValidationError("Skills must be a list")
        
        # Ensure all skills are strings
        if not all(isinstance(skill, str) for skill in skills):
            raise ValidationError("All skills must be strings")
        
        # Remove empty strings and strip whitespace
        profile["Skills"] = [skill.strip() for skill in skills if skill.strip()]
        
        if not profile["Skills"]:
            raise ValidationError("At least one skill is required")
    else:
        # Skills is required
        raise ValidationError("Skills field is required")
    
    # Validate Location field (optional)
    if "Location" in profile:
        location = profile["Location"]
        if not isinstance(location, str):
            raise ValidationError("Location must be a string")
        profile["Location"] = location.strip()
    
    # Validate Eligibility field (optional)
    if "Eligibility" in profile:
        eligibility = profile["Eligibility"]
        if not isinstance(eligibility, str):
            raise ValidationError("Eligibility must be a string")
        profile["Eligibility"] = eligibility.strip()
    
    # Validate Degree field (optional)
    if "Degree" in profile:
        degree = profile["Degree"]
        if not isinstance(degree, str):
            raise ValidationError("Degree must be a string")
        profile["Degree"] = degree.strip()
    
    # Validate Sector preference (optional)
    if "Sector" in profile:
        sector = profile["Sector"]
        if not isinstance(sector, str):
            raise ValidationError("Sector must be a string")
        profile["Sector"] = sector.strip()
    
    return profile


def validate_top_n(top_n: Optional[int] = None) -> int:
    """
    Validate the top_n parameter for recommendations.
    
    Args:
        top_n: Number of recommendations to return
        
    Returns:
        Validated top_n value (defaults to 10 if None)
        
    Raises:
        ValidationError: If top_n is invalid
    """
    if top_n is None:
        return 10
    
    if not isinstance(top_n, int):
        raise ValidationError("top_n must be an integer")
    
    if top_n < 1:
        raise ValidationError("top_n must be at least 1")
    
    if top_n > 100:
        raise ValidationError("top_n cannot exceed 100")
    
    return top_n


def sanitize_string(value: str, max_length: int = 1000) -> str:
    """
    Sanitize a string input by removing potentially harmful characters.
    
    Args:
        value: String to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
        
    Raises:
        ValidationError: If string is too long
    """
    if not isinstance(value, str):
        raise ValidationError("Value must be a string")
    
    # Strip whitespace
    value = value.strip()
    
    # Check length
    if len(value) > max_length:
        raise ValidationError(f"String exceeds maximum length of {max_length}")
    
    return value


def validate_internship_data(internship: Dict[str, Any]) -> bool:
    """
    Validate internship data structure.
    
    Args:
        internship: Dictionary containing internship information
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["Title", "Required Skills"]
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in internship:
            return False
    
    # Validate Title
    if not isinstance(internship.get("Title"), str) or not internship["Title"].strip():
        return False
    
    # Validate Required Skills
    skills = internship.get("Required Skills")
    if not isinstance(skills, (list, str)):
        return False
    
    return True
