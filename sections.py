SECTION_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "description": "A section validator that checks inputs in the sections collection",
        "required": ["_id", "department_abbreviation", "course_number", "course_name","section_number", "semester", "year", "building", "room", "schedule", "start_time", "instructor"],
        "additionalProperties": False,
        "properties": {
            "_id": {
                "bsonType": "objectId"
            },
            "department_abbreviation": {
                "description": "A string abbreviation of a specific career of a specific discipline",
                "bsonType": "string"
            },
            "course_number": {
                "description": "An integer value representing a specific subject within a department, must exist before section can be added",
                "bsonType": "int",
                "minimum": 1
            },
            "course_name": {
                "description": "The name of the course, must exist before a section can be added",
                "bsonType": "string"
            },
            "section_number": {
                "description": "An integer value representing a specific class within a course",
                "bsonType": "int"
            },
            "semester": {
                "description": "A string representing the time the class will be held",
                "enum": ["Fall", "Spring", "Winter", "Summer I", "Summer II", "Summer III"],
                "bsonType": "string"
            },
            "year": {
                "description": "An integer representation of the year the class is being held, is not lower than 1969",
                "bsonType": "int",
                "minimum": 1969,
                "exclusiveMinimum": True
            },
            "building": {
                "description": "A string that determines the building in which the class is located",
                "bsonType": "string",
                "enum": ["ANAC", "CDC", "DC", "ECS", "EN2", "EN3", "EN4", "EN5", "ET", "HSCI", "NUR", "VEC"]
            },
            "room": {
                "description": "Room number where class will be held, should be "
                               "between 0 and less than 1000(1 < room < 1000)",
                "bsonType": "int",
                "minimum": 1,
                "maximum": 9999
            },
            "schedule": {
                "description": "Days class is scheduled, Only allow in ('MW', 'TuTh', 'MWF', 'F', 'S')",
                "bsonType": "string"
            },
            "start_time": {
                "description": "Time class starts, should only be 8:00am to 7:30pm inclusive",
                "bsonType": "string"
            },
            "instructor": {
                "description": "Name of the instructor",
                "bsonType": "string"
            },
            "students": {
                "bsonType": "array",
                "description": "This student array will hold the student_id's of all the students enrolled in the class",
                "uniqueItems": True,
                "additionalProperties": False,
                "items": {
                    "bsonType": "object",
                    "required": ["last_name", "first_name", "type"],
                    "additionalProperties": False,
                    "properties":{
                        "student_id": {
                            "bsonType": "objectId"
                        },
                        "last_name": {
                            "bsonType": "string"
                        },
                        "first_name": {
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
                                "declaration_date": {
                                    "bsonType": "date"
                                },
                                "min_satisfactory": {
                                    "bsonType": "string",
                                    "enum": ["A", "B", "C"]
                                }
                            },
                            "oneOf": [
                                {
                                    "properties": {
                                        "type_name": { "enum": ["PassFail"] }
                                    },
                                    "required": ["type_name", "application_date"]
                                },
                                {
                                    "properties": {
                                        "type_name": { "enum": ["LetterGrade"] }
                                    },
                                    "required": ["type_name", "min_satisfactory"]
                                }
                            ]

                        }
                    }

                }
            }
        }
    }
}
