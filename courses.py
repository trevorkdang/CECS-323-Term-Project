COURSE_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "description": "A course validator to check inputs in the courses collection",
        "required": ["_id", "department_abbreviation", "course_number", "course_name","course_description", "units"],
        "additionalProperties": False,
        "properties": {
            "_id": {
                "bsonType": "objectId"
            },
            "department_abbreviation": {
                "description": "A department has to exist in order for a course to be offered in that specific department",
                "bsonType": "string"
            },
            "course_number": {
                "bsonType": "int",
                "minimum": 1
            },
            "course_name": {
                "bsonType": "string"
            },
            "course_description": {
                "bsonType": "string"
            },
            "units": {
                "bsonType": "int",
                "minimum": 1,
                "maximum": 4
            },
            "sections": {
                "bsonType": "array",
                "description": "In the implementations, the sections array will contain only the section object ids",
                "uniqueItems": True,
                "additionalProperties": False,
                "items": {
                    "bsonType": "objectId"
                }
            } 
        }
    }
}
