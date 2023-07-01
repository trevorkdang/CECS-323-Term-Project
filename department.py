DEPARTMENT_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "description": "A department validator that checks inputs in the departments collection",
        "required": ["_id", "name", "abbreviation", "chair_name", "building", "office", "department_description"],
        "additionalProperties": False,
        "properties": {
            "_id": {
                "bsonType": "objectId"
            },
            "name": {
                "bsonType": "string",
                "description": "The name of the department",
                "minLength": 5,
                "maxLength": 50
            },
            "abbreviation": {
                "bsonType": "string",
                "description": "The abbreviation of the department name",
                "maxLength": 6
            },
            "chair_name": {
                "bsonType": "string",
                "description": "The name of the department chair",
                "maxLength": 80
            },
            "building": {
                "bsonType": "string",
                "description": "The building where the department is located",
                "enum": ["ANAC", "CDC", "DC", "ECS", "EN2", "EN3", "EN4", "EN5", "ET", "HSCI", "NUR", "VEC"]
            },
            "office": {
                "bsonType": "int",
                "description": "An integer value of where the office of the department is located",
                "minimum": 1,
                "maximum": 9999
            },
            "department_description": {
                "bsonType": "string",
                "description": "A description that generally describes the department",
                "maxLength": 80
            },
            "courses": {
                "bsonType": "array",
                "uniqueItems": True,
                "additionalProperties": False,
                "items": {
                    "bsonType": "string"
                }
            },
            "majors": {
                "bsonType": "array",
                "description": "This is an array of objects that holds both the Major name and description of the major",
                "uniqueItems": True,
                "additionalProperties": False,
                "items": {
                    "bsonType": "object",
                    "required": ["major_name", "major_description"],
                    "additionalProperties": False,
                    "properties": {
                        "major_name": {
                            "bsonType": "string",
                        },
                        "major_description": {
                            "bsonType": "string"
                        }
                    }
                }
            }
        }
    }
}