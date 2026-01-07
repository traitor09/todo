"""
Custom exception classes for the Internship Recommendation System.
"""


class ConfigurationError(Exception):
    """
    Raised when there's an issue with application configuration.
    
    This typically occurs when required environment variables are missing
    or have invalid values.
    """
    pass


class ValidationError(Exception):
    """
    Raised when input validation fails.
    
    This occurs when user input doesn't meet the expected format or
    contains invalid data.
    """
    pass


class DatabaseError(Exception):
    """
    Raised when database operations fail.
    
    This includes connection failures, query errors, or data integrity issues.
    """
    pass


class RecommendationError(Exception):
    """
    Raised when the recommendation engine encounters an error.
    
    This could be due to invalid input data, missing required fields,
    or failures in the recommendation algorithms.
    """
    pass
