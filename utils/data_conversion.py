from collections import namedtuple
import re

def convert_to_namedtuple(input):
    match = re.match(r"(\w+)\((.+)\)", input)
    if not match:
        raise ValueError("The string format is invalid!")
    namedtuple_name = match.group(1)  
    fields_str = match.group(2) 

    fields = {}
    for field in fields_str.split(","):
        key, value = field.split("=")
        fields[key.strip()] = int(value.strip()) 

    return namedtuple(namedtuple_name, fields.keys())(**fields)
