import re
from datetime import datetime

# To check whether a given word has at least one Upper, lower, special character and number
def check_string(word:str):

    # Check for at least one Upper character
    has_upper = re.search(r'[A-Z]',word)

    # Check for at least one Upper character
    has_lower = re.search(r'[a-z]',word)

    # Check for at least one special character
    has_special = re.search(r'[\W_]',word)

    # Check for at least one number

    has_number = re.search(r'[\d]',word)

    return all([has_upper, has_lower, has_special, has_number])

# To change SQLAlchemy returned object to a dictionary
def to_dict(obj):
    result = {}

    for column in obj.__table__.columns:
        value = getattr(obj,column.name)
        # Check if the value is a datetime object, then format it as a string
        if isinstance(value, datetime):
            result[column.name] = value.isoformat()
        else:
            result[column.name] = value



    return result