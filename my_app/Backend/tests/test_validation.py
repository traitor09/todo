"""
Unit tests for input validation utilities.
"""

import pytest
from utils.validation import (
    validate_candidate_profile,
    validate_top_n,
    sanitize_string,
    validate_internship_data
)
from utils.exceptions import ValidationError


class TestValidateCandidateProfile:
    """Test suite for candidate profile validation."""

    def test_valid_profile_with_required_fields(self):
        """Test validation with only required fields."""
        profile = {
            "Skills": ["Python", "Flask", "MongoDB"]
        }
        result = validate_candidate_profile(profile)
        assert result["Skills"] == ["Python", "Flask", "MongoDB"]

    def test_valid_profile_with_all_fields(self):
        """Test validation with all optional fields."""
        profile = {
            "Skills": ["Python", "Flask"],
            "Location": "Remote",
            "Eligibility": "3rd year",
            "Degree": "B.Tech",
            "Sector": "Technology"
        }
        result = validate_candidate_profile(profile)
        assert result["Skills"] == ["Python", "Flask"]
        assert result["Location"] == "Remote"
        assert result["Eligibility"] == "3rd year"

    def test_profile_not_dict(self):
        """Test that non-dict input raises ValidationError."""
        with pytest.raises(ValidationError, match="must be a dictionary"):
            validate_candidate_profile("not a dict")

    def test_missing_skills_field(self):
        """Test that missing Skills field raises ValidationError."""
        profile = {"Location": "Remote"}
        with pytest.raises(ValidationError, match="Skills field is required"):
            validate_candidate_profile(profile)

    def test_skills_not_list(self):
        """Test that non-list Skills raises ValidationError."""
        profile = {"Skills": "Python, Flask"}
        with pytest.raises(ValidationError, match="Skills must be a list"):
            validate_candidate_profile(profile)

    def test_skills_with_non_string_items(self):
        """Test that non-string skill items raise ValidationError."""
        profile = {"Skills": ["Python", 123, "Flask"]}
        with pytest.raises(ValidationError, match="All skills must be strings"):
            validate_candidate_profile(profile)

    def test_empty_skills_list(self):
        """Test that empty skills list raises ValidationError."""
        profile = {"Skills": []}
        with pytest.raises(ValidationError, match="At least one skill is required"):
            validate_candidate_profile(profile)

    def test_skills_with_empty_strings(self):
        """Test that empty strings are removed from skills."""
        profile = {"Skills": ["Python", "", "  ", "Flask"]}
        result = validate_candidate_profile(profile)
        assert result["Skills"] == ["Python", "Flask"]

    def test_skills_whitespace_trimming(self):
        """Test that whitespace is trimmed from skills."""
        profile = {"Skills": ["  Python  ", " Flask "]}
        result = validate_candidate_profile(profile)
        assert result["Skills"] == ["Python", "Flask"]

    def test_location_not_string(self):
        """Test that non-string Location raises ValidationError."""
        profile = {"Skills": ["Python"], "Location": 123}
        with pytest.raises(ValidationError, match="Location must be a string"):
            validate_candidate_profile(profile)

    def test_location_whitespace_trimming(self):
        """Test that whitespace is trimmed from location."""
        profile = {"Skills": ["Python"], "Location": "  Remote  "}
        result = validate_candidate_profile(profile)
        assert result["Location"] == "Remote"

    def test_eligibility_not_string(self):
        """Test that non-string Eligibility raises ValidationError."""
        profile = {"Skills": ["Python"], "Eligibility": 3}
        with pytest.raises(ValidationError, match="Eligibility must be a string"):
            validate_candidate_profile(profile)

    def test_degree_not_string(self):
        """Test that non-string Degree raises ValidationError."""
        profile = {"Skills": ["Python"], "Degree": ["B.Tech"]}
        with pytest.raises(ValidationError, match="Degree must be a string"):
            validate_candidate_profile(profile)

    def test_sector_not_string(self):
        """Test that non-string Sector raises ValidationError."""
        profile = {"Skills": ["Python"], "Sector": 123}
        with pytest.raises(ValidationError, match="Sector must be a string"):
            validate_candidate_profile(profile)


class TestValidateTopN:
    """Test suite for top_n parameter validation."""

    def test_none_returns_default(self):
        """Test that None returns default value of 10."""
        assert validate_top_n(None) == 10

    def test_valid_integer(self):
        """Test that valid integer is returned."""
        assert validate_top_n(5) == 5
        assert validate_top_n(50) == 50

    def test_not_integer(self):
        """Test that non-integer raises ValidationError."""
        with pytest.raises(ValidationError, match="must be an integer"):
            validate_top_n("10")
        with pytest.raises(ValidationError, match="must be an integer"):
            validate_top_n(10.5)

    def test_less_than_one(self):
        """Test that value less than 1 raises ValidationError."""
        with pytest.raises(ValidationError, match="must be at least 1"):
            validate_top_n(0)
        with pytest.raises(ValidationError, match="must be at least 1"):
            validate_top_n(-5)

    def test_greater_than_max(self):
        """Test that value greater than 100 raises ValidationError."""
        with pytest.raises(ValidationError, match="cannot exceed 100"):
            validate_top_n(101)
        with pytest.raises(ValidationError, match="cannot exceed 100"):
            validate_top_n(1000)

    def test_boundary_values(self):
        """Test boundary values."""
        assert validate_top_n(1) == 1
        assert validate_top_n(100) == 100


class TestSanitizeString:
    """Test suite for string sanitization."""

    def test_valid_string(self):
        """Test that valid string is returned trimmed."""
        assert sanitize_string("  Hello World  ") == "Hello World"

    def test_not_string(self):
        """Test that non-string raises ValidationError."""
        with pytest.raises(ValidationError, match="must be a string"):
            sanitize_string(123)

    def test_exceeds_max_length(self):
        """Test that string exceeding max length raises ValidationError."""
        long_string = "a" * 1001
        with pytest.raises(ValidationError, match="exceeds maximum length"):
            sanitize_string(long_string)

    def test_custom_max_length(self):
        """Test custom max length parameter."""
        assert sanitize_string("Hello", max_length=10) == "Hello"
        with pytest.raises(ValidationError):
            sanitize_string("Hello World", max_length=5)


class TestValidateInternshipData:
    """Test suite for internship data validation."""

    def test_valid_internship_with_list_skills(self):
        """Test valid internship with skills as list."""
        internship = {
            "Title": "Python Developer Intern",
            "Required Skills": ["Python", "Flask"]
        }
        assert validate_internship_data(internship) is True

    def test_valid_internship_with_string_skills(self):
        """Test valid internship with skills as string."""
        internship = {
            "Title": "Python Developer Intern",
            "Required Skills": "Python, Flask"
        }
        assert validate_internship_data(internship) is True

    def test_missing_title(self):
        """Test that missing title returns False."""
        internship = {
            "Required Skills": ["Python"]
        }
        assert validate_internship_data(internship) is False

    def test_missing_required_skills(self):
        """Test that missing required skills returns False."""
        internship = {
            "Title": "Python Developer Intern"
        }
        assert validate_internship_data(internship) is False

    def test_empty_title(self):
        """Test that empty title returns False."""
        internship = {
            "Title": "",
            "Required Skills": ["Python"]
        }
        assert validate_internship_data(internship) is False

    def test_title_not_string(self):
        """Test that non-string title returns False."""
        internship = {
            "Title": 123,
            "Required Skills": ["Python"]
        }
        assert validate_internship_data(internship) is False

    def test_skills_invalid_type(self):
        """Test that invalid skills type returns False."""
        internship = {
            "Title": "Python Developer Intern",
            "Required Skills": 123
        }
        assert validate_internship_data(internship) is False
