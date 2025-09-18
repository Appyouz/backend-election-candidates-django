import re
from rest_framework import serializers
from django.core.validators import RegexValidator


class ValidationErrorCollector:
    """
    Helper class to collect validation errors and raise them in one go.
    """

    def __init__(self):
        self.errors = {}

    def add_error(self, field: str, message: str):
        """
        Adds an error message for a specific field.
        """
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)

    def add_non_field_error(self, message: str):
        """
        Adds a general error not tied to a specific field.
        """
        self.add_error("non_field_errors", message)

    def raise_error(self):
        """
        Raises serializers.ValidationError if any errors have been added.
        """
        if self.errors:
            raise serializers.ValidationError(self.errors)


# Validator for lowercase letters and underscores
# Validator for lowercase letters, numbers, and underscores
lowercase_numbers_underscore_validator = RegexValidator(
    regex=r"^[a-z0-9_]+$",  # Regex pattern for lowercase letters, numbers, and underscores
    message="This field must contain only lowercase letters, numbers, and underscores",
)


# Define the regex for valid Nepal mobile numbers
# From: https://github.com/sbishnu019/nepali-phone-number/blob/31fc90458adbad5e60b1596a4fe240c5b08ab0e6/nepali_phone_number/regexs.py#L2
phone_number_regex = re.compile(
    "^(984|985|986|974|975|980|981|982|961|988|972|963)\d{7}$"
)
# Create the validator using RegexValidator
nepal_phone_number_validator = RegexValidator(
    regex=phone_number_regex,
    message="Enter a valid Nepal mobile number. The number must start with one of the following prefixes: 984, 985, 986, 974, 975, 980, 981, 982, 961, 988, 972, 963, followed by 7 digits.",
)
