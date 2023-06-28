STUDENT_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "description": "A student validator that checks inputs in the students collection",
        "required": ["_id", "first_name", "last_name", "email"],
        "additionalProperties": False,
        "properties": {
            "_id": {
                "bsonType": "objectId"
            },
            "first_name": {
                "description": "Student's first name",
                "bsonType": "string"
            },
            "last_name": {
                "description": "Student's last name",
                "bsonType": "string"
            },
            "email": {
                "description": "Student's email",
                "bsonType": "string"
            },
            "major": {
                "description": "An array of string and a date values student is currently pursuing, must exist in departments before adding to array",
                "bsonType": "array",
                "uniqueItems": True,
                "additionalProperties": False,
                "items": {
                    "type": "object",
                    "properties": {
                        "major_name": {
                            "bsonType": "string",
                        },
                        "declaration_date": {
                            "bsonType": "date"
                        }
                    }
                }
            },
            "student_sections": {
                "bsonType": "array",
                "description": "Array of objects, will hold student's sections, must be unique",
                "uniqueItems": True,
                "additionalProperties": False,
                "items": {
                    "bsonType": "object",
                    "required": ["section_id","department_abbreviation", "course_name", "section_number", "year", "semester", "type"],
                    "additionalProperties": False,
                    "properties": {
                        "section_id": {
                            "bsonType": "objectId"
                        },
                        "department_abbreviation": {
                            "bsonType": "string"
                        },
                        "course_name": {
                            "bsonType": "string"
                        }, 
                        "course_number": {
                            "bsonType": "int"
                        },
                        "section_number": {
                            "bsonType": "int"
                        },
                        "year": {
                            "bsonType": "int"
                        },
                        "semester": {
                            "bsonType": "string"
                        },
                        "type": {
                            "description": "Can either be a PassFail(date <= today), or LetterGrade(A, B, C)",
                            "bsonType": "object",
                            "additionalProperties": False,
                            "properties": {
                                "type_name": {
                                    "bsonType": "string",
                                    "enum": ["PassFail", "LetterGrade"]
                                },
                                "application_date": {
                                    "bsonType": "date"
                                },
                                "min_satisfactory": {
                                    "bsonType": "string",
                                    "enum": ["A", "B", "C"]
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}