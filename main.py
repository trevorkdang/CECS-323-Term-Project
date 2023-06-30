import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from datetime import datetime, date
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
from department import DEPARTMENT_VALIDATOR
from courses import COURSE_VALIDATOR
from sections import SECTION_VALIDATOR
from students import STUDENT_VALIDATOR
from bson.objectid import ObjectId


def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)

def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)

def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)
    

# all the add defintions, including some used from previous assignments
def add_department(db):
    collection = db["departments"]
    office: int
    while True:
        try:
            #inputs for the following will be saved
            departmentName = input("Department Name(10 - 50 characters)--> ")
            abbreviation = input("Abbreviation(Max 6 characters)--> ")
            chairName = input("Chair Name(Max 80 characters)--> ")
            building = input("Building--> ")
            office = int(input("Office #(1 - 999)--> "))
            description = input("Description--> ")

            department = {
                "name": departmentName,
                "abbreviation": abbreviation,
                "chair_name": chairName,
                "building": building,
                "office": office,
                "department_description": description
            }  
            collection.insert_one(department)
            break
        except pymongo.errors.PyMongoError as error:
            pprint(error)
            print("Please try again-->")
        except ValueError as error:
            print(error)
            print("Please try again-->")


def add_course(db):
    collection = db["courses"]
    while True:
        try:
            department = select_department(db)
            courseNumber = int(input("Course Number-->"))
            courseName = input("Course Name--> ")
            courseDescription = input("Course Description--> ")
            units = int(input("Units--> "))
            course = {
                "department_abbreviation": department["abbreviation"],
                "course_number": courseNumber,
                "course_name": courseName,
                "course_description": courseDescription,
                "units": units
            }
            collection.insert_one(course)
            # updates the courses in the departments collection
            course = collection.find_one(course)
            departments = db["departments"]
            departments.update_one({"name": department["name"]}, {"$push": {"courses": course["course_name"]}})
            break
        except pymongo.errors.PyMongoError as error:
            pprint(error)
            print("Please try again-->")
        except ValueError as error:
            print(error)
            print("Please try again-->")


def add_section(db):
    collection = db["sections"]
    while True:
        try:
            # selects the course we will add a section to
            # then input the fields needed for said section
            course = select_course(db)
            sectionNumber = int(input("Section Number--> "))
            year = int(input("Year--> "))
            semester = input("Semester[Fall, Spring, Winter, Summer I, Summer II, Summer III]--> ")
            building = input("Building--> ")
            room = int(input("Room--> "))
            schedule = input("Schedule('MW', 'TuTh', 'MWF', 'F', 'S')--> ")
            start_time = input("Time(HH:MM)am/pm '8:00am to 7:30pm'--> ")
            instructor = input("Instructor--> ")
            section = {
                "department_abbreviation": course["department_abbreviation"],
                "course_number": course["course_number"],
                "course_name": course["course_name"],
                "section_number": sectionNumber,
                "semester": semester,
                "year": year,
                "building": building,
                "room": room,
                "schedule": schedule,
                "start_time": start_time,
                "instructor": instructor,
            }
            collection.insert_one(section)
            # adds a reference to the section_id in course's sections array
            section = collection.find_one(section)
            courses = db["courses"]
            courses.update_one({"department_abbreviation": course["department_abbreviation"], "course_number": course["course_number"]},
                               {"$push": {"sections": ObjectId(section["_id"])}})
            break
        except pymongo.errors.PyMongoError as error:
            pprint(error)
            print("Please try again-->")
        except ValueError as error:
            print(error)
            print("Please try again-->")


def add_major(db):
    collection = db["departments"]
    while True:
        try:
            # must choose a valid department to add major to
            department = select_department(db)
            majorName = input("Major Name--> ")
            majorDescription = input("Major Description--> ")
            # here the major is an object, this will allow us to add into department major array
            major = {"major_name": majorName, "major_description": majorDescription}
            query = {"name": department["name"]}
            update = {"$push": {"majors": major}}
            collection.update_one(query, update)
            break
        except pymongo.errors.PyMongoError as error:
            pprint(error)
            print("Please try again-->")
            

def add_student(db):
    collection = db["students"]
    firstName: str = ''
    lastName: str = ''
    email: str = ''

    while True:
        try:
            firstName = input("First Name--> ")
            lastName = input("Last Name--> ")
            email = input("email--> ")

            student = {
                "first_name": firstName,
                "last_name": lastName,
                "email": email,
            }  
            collection.insert_one(student)
            break
        except pymongo.errors.PyMongoError as error:
            pprint(error)
            print("Please try again-->")
    

def add_section_student(db):
    collection = db["students"]
    # the following will add a section to student/used for vice-versa as well (add_student_section)
    while True:
        try:
            # checks for student
            student = select_student(db)
            # checks for section
            section = select_section(db)
            # adds a new input for passfail or lettergrade
            passOrLetter = input("PassFail or LetterGrade--> ")
            if passOrLetter == "PassFail":
                applicationDate = input("Enter declaration date in format 'YYYY-MM-DD'--> ")
                # datetime object
                datetime_obj = datetime.combine(datetime.strptime(applicationDate, "%Y-%m-%d"), datetime.min.time())
                type = {"type_name": passOrLetter, "application_date": datetime_obj}
            if passOrLetter == "LetterGrade":
                letterGrade = input("Please input a min letter grade required--> ")
                type = {"type_name": passOrLetter, "min_satisfactory": letterGrade}
            # Uses a dictionary to make sure the info is inserted properly
            sectionToAdd = {"section_id": ObjectId(section["_id"]),
                                "department_abbreviation": section["department_abbreviation"],
                                 "course_name": section["course_name"], "course_number": section["course_number"], "section_number": section["section_number"],
                                 "year": section["year"], "semester": section["semester"], "type": type}
            query = {"first_name": student["first_name"], "last_name": student["last_name"]}
            update = {"$push": {"student_sections": sectionToAdd}}
            collection.update_one(query, update)
            # Now we must update the section's student array with the newly added student
            student = collection.find_one({"last_name": student["last_name"], "first_name": student["first_name"]})
            sections = db["sections"]
            studentToAdd = {"student_id": ObjectId(student["_id"]), "last_name": student["last_name"], "first_name": student["first_name"], "type": type}
            sections.update_one(section, {"$push": {"students": studentToAdd}})
            break
        except pymongo.errors.PyMongoError as error:
            pprint(error)
            print("Please try again--> ")
        except ValueError as error:
            pprint(error)
            print("Please try again-->")


def add_student_section(db):
    collection = db["students"]
    # same format as add_section_student(db), just selects the section first
    while True:
        try:   
            section = select_section(db)
            student = select_student(db)
            # we must ask for PassFail or LetterGrade
            passOrLetter = input("PassFail or LetterGrade--> ")
            if passOrLetter == "PassFail":
                applicationDate = input("Enter declaration date in format 'YYYY-MM-DD'--> ")
                # date wizardry
                datetime_obj = datetime.combine(datetime.strptime(applicationDate, "%Y-%m-%d"), datetime.min.time())
                type = {"type_name": passOrLetter, "application_date": datetime_obj}
            if passOrLetter == "LetterGrade":
                letterGrade = input("Please input a min letter grade required--> ")
                type = {"type_name": passOrLetter, "min_satisfactory": letterGrade}

            sectionToAdd = {"section_id": ObjectId(section["_id"]),
                                "department_abbreviation": section["department_abbreviation"],
                                 "course_name": section["course_name"], "course_number": section["course_number"], "section_number": section["section_number"],
                                 "year": section["year"], "semester": section["semester"], "type": type}
            query = {"first_name": student["first_name"], "last_name": student["last_name"]}
            update = {"$push": {"student_sections": sectionToAdd}}
            collection.update_one(query, update)
            # Now we must update the section's student array with the newly added student
            student = collection.find_one({"last_name": student["last_name"], "first_name": student["first_name"]})
            sections = db["sections"]
            studentToAdd = {"student_id": ObjectId(student["_id"]), "last_name": student["last_name"], "first_name": student["first_name"], "type": type}
            sections.update_one(section, {"$push": {"students": studentToAdd}})
            break
        except pymongo.errors.PyMongoError as error:
            pprint(error)
            print("Please try again--> ")
        except ValueError as error:
            pprint(error)
            print("Please try again-->")


def add_major_student(db):
    collection = db["students"]
    while True:
        try:
            # checks for valid student
            student = select_student(db)
            # checks for major
            majorName = select_major(db)
            declarationDate = input("Enter declaration date in format 'YYYY-MM-DD'--> ")
            # datetime
            datetime_obj = datetime.combine(datetime.strptime(declarationDate, "%Y-%m-%d"), datetime.min.time())
            major = {"major_name": majorName, "declaration_date": datetime_obj}
            query = {"first_name": student["first_name"], "last_name": student["last_name"]}
            update = {"$push": {"major": major}}
            collection.update_one(query, update)
            break
        except pymongo.errors.PyMongoError as error:
            print(error)
            print("Please try again-->")
        except ValueError as error:
            print(error)
            print("Please try again-->")


# all the select() definitions, similar to the SQLAlchemy assignments
def select_student(db, show: bool = True):
    if show == True:
        list_student(db)
    # Create a connection to the students collection from this database
    collection = db["students"]
    found: bool = False
    lastName: str = ''
    firstName: str = ''

    while not found:
        lastName = input("Student's last name--> ")
        firstName = input("Student's first name--> ")
        name_count: int = collection.count_documents({"last_name": lastName, "first_name": firstName})
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    found_student = collection.find_one({"last_name": lastName, "first_name": firstName})
    return found_student


def select_department(db):
    list_department(db)
    collection = db["departments"]
    found: bool = False
    departmentName: str = ''
    while not found:
        departmentName = input("Department Name--> ")
        name_count: int = collection.count_documents({"name": departmentName})
        found = name_count == 1
        if not found:
            print("No department found by that name. Try again.")
    found_department = collection.find_one({"name": departmentName})
    return found_department


def select_course(db):
    list_course(db)
    collection = db["courses"]
    found: bool = False
    while not found:
        departmentAbbreviation = input("Department Abbreviation--> ")
        try:
            courseNumber = int(input("Course Number--> "))
        except ValueError as error:
            print(ValueError)
            print("Please try again-->")
            continue
        name_count: int = collection.count_documents({"department_abbreviation": departmentAbbreviation,
                                                      "course_number": courseNumber})
        found = name_count == 1
        if not found:
            print("There are no such Courses. Try again.")
    found_course = collection.find_one({"department_abbreviation": departmentAbbreviation,
                                        "course_number": courseNumber})
    return found_course


def select_section(db, show: bool = True):
    if show == True:
        list_section(db)
    collection = db["sections"]
    found: bool = False
    while not found:
        # to select section, need valid inputs
        departmentAbbreviation = input("Department Abbreviation--> ")
        try:
            courseNumber = int(input("Course Number--> "))
            sectionNumber = int(input("Section Number--> "))
            year = int(input("Year--> "))
        except ValueError as error:
            print(ValueError)
            print("Please try again-->")
            continue
        semester = input("Semester[Fall, Spring, Winter, Summer I, Summer II, Summer III]--> ")
        name_count: int = collection.count_documents({"department_abbreviation": departmentAbbreviation,
                                                      "course_number" : courseNumber, "section_number": sectionNumber,
                                                      "year": year, "semester": semester})
        found = name_count == 1
        if not found:
            print("Section not found. Try again.")
    found_section = collection.find_one({"department_abbreviation": departmentAbbreviation,
                                            "course_number" : courseNumber, "section_number": sectionNumber,
                                            "year": year, "semester": semester})
    return found_section


def select_major(db):
    
    collection = db["departments"]
    found: bool = False
    while not found:
        # searches for a major from the department's majors array
        department = select_department(db)
        majorName = input("Major Name--> ")
        name_count = collection.count_documents({"name": department["name"], "majors.major_name": majorName})
        found = name_count == 1
        if not found:
            print("Major not found. Try again.")
    found_major = collection.find_one({"name": department["name"], "majors.major_name": majorName})
    # returns major name
    return majorName




# all the delete() definitions, including some used from previous assignments

def delete_department(db):
    department = select_department(db)
    departments = db["departments"]
    # we must delete all sections that are under this department
    sections = db["sections"]
    for course in department["courses"]:
        sections.delete_many({"course_name": course})
    # we must delete all courses that fall under the specific department
    courses = db["courses"]
    courses.delete_many({"department_abbreviation": department["abbreviation"]})
    # now actually delete the department
    deleted = departments.delete_one({"_id": department["_id"]})
    print(f"We just deleted: {deleted.deleted_count} departments. ")

    
def delete_course(db):
    course = select_course(db)
    courses = db["courses"]
    # cascade deletes all the sections under the course
    sections = db["sections"]
    sections.delete_many({"course_number": course["course_number"]})
    departments = db["departments"]
    departments.update_one({"abbreviation": course["department_abbreviation"]}, {"$pull": {"courses": course["course_name"]}})
    deleted = courses.delete_one({"_id": course["_id"]})
    print(f"We just deleted: {deleted.deleted_count} courses. ")


def delete_section(db):
    section = select_section(db)
    sections = db["sections"]
    students = db["students"]
    students.update_many({}, {"$pull":{"student_sections": 
                                       {"department_abbreviation": section["department_abbreviation"],
                                        "course_name": section["course_name"],
                                        "section_number": section["section_number"],
                                        "year": section["year"],
                                        "semester": section["semester"]}}})
    # We must also remember to delete the reference to that section from courses sections array
    courses = db["courses"]
    courses.update_many({}, {"$pull": {"sections": ObjectId(section["_id"])}})
    deleted = sections.delete_one({"_id": section["_id"]})
    print(f"We just deleted: {deleted.deleted_count} sections.")



def delete_major(db):
    major = select_major(db)
    # we have to remove major from all students that have declared that major
    students = db["students"]
    students.update_many({"major.major_name": major},
                         {"$pull": {"major": {"major_name": major}}})
    # Now we simply remove the major from the list of majors for that particular department
    departments = db["departments"]
    deleted = departments.update_one({"majors.major_name": major},
                                     {"$pull": {"majors": {"major_name": major}}})
    print(f"We just deleted: {deleted.modified_count} majors. ")


def delete_student(db):
    student = select_student(db)
    students = db["students"]
    # should remove any references to that student in the students property of the sections collection
    sections = db["sections"]
    sections.update_many({"students": ObjectId(student["_id"])},
                         {"$pull": {"students": ObjectId(student["_id"])}})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    deleted = students.delete_one({"_id": student["_id"]})
    print(f"We just deleted: {deleted.deleted_count} students.")    


def delete_section_student(db):
    #selects a student first to have a section be removed
    student = select_student(db)
    #checks that a section can be deleted from that student
    if "student_sections" not in student.keys():
        print("That student does not have any section to remove. Try again.")
        return()
    section = select_section(db, False)
    if "students" not in section.keys():
        print("That sections does not have any students to remove. Try again.")
        return()
    students = db["students"]
    deleted = students.update_one({"_id": student["_id"]},
                         {"$pull": {"student_sections": {"department_abbreviation": section["department_abbreviation"],
                         "course_name": section["course_name"]}, "section_number": section["section_number"], "year": section["year"], "semester": section["semester"]}})
    # we must delete the object id reference from the sections array of student
    db.sections.update_one(section, {"$pull": {"students": {"student_id": ObjectId(student["_id"])}}})
    print(f"We just deleted: {deleted.modified_count} from student's section")


def delete_student_section(db):
    #selects a section first to have a student be deleted
    section = select_section(db)
    #checks that a section can be deleted from that student
    if "students" not in section.keys():
        print("That section does not have any student to remove. Try again.")
        return()
    student = select_student(db, False)
    students = db["students"]
    deleted = students.update_one({"_id": student["_id"]},
                         {"$pull": {"student_sections": {"department_abbreviation": section["department_abbreviation"],
                         "course_name": section["course_name"]}, "section_number": section["section_number"], "year": section["year"], "semester": section["semester"]}})
    # we must delete the object id reference from the sections array of student
    db.sections.update_one(section, {"$pull": {"students": {"student_id": ObjectId(student["_id"])}}})
    print(f"We just deleted: {deleted.modified_count} from student's section")


def delete_major_student(db):
    student = select_student(db)
    major = select_major(db)
    students = db["students"]
    deleted = students.update_one({"first_name": student["first_name"], "last_name": student["last_name"]},
                         {"$pull": {"major": {"major_name": major}}})
    print(f"We just deleted: {deleted.modified_count} from student's major")


# the list definitions, including some used from previous assignments
def list_department(db):
    departments = db["departments"].find({}).sort("name", pymongo.ASCENDING)
    print('Current Departments:')
    for department in departments:
        pprint(department)


def list_course(db):
    courses = db["courses"].find({}).sort([("department_abbreviation", pymongo.ASCENDING),
                                          ("course_name", pymongo.ASCENDING)])
    print('Current Courses:')
    for course in courses:
        pprint(course)


def list_section(db):
    sections = db["sections"].find({}).sort([("department_abbreviation", pymongo.ASCENDING),
                                            ("course_name", pymongo.ASCENDING),
                                            ("section_number", pymongo.ASCENDING)])
    print("Current Sections:")
    for section in sections:
        pprint(section)


def list_majors(db):
    departments = db["departments"].find({}).sort("name", pymongo.ASCENDING)
    print('Current Majors:')
    for department in departments:
        if "majors" in department:
            pprint(department["name","majors"])

def list_student(db):
    students = db["students"].find({}).sort([("last_name", pymongo.ASCENDING),
                                             ("first_name", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    print("Current Students:")
    for student in students:
        pprint(student)


def list_section_students(db):
    sections = db["sections"].find({}).sort([("department_abbreviation", pymongo.ASCENDING),
                                             ("course_name", pymongo.ASCENDING),
                                             ("section_number", pymongo.ASCENDING)])
    for section in sections:
        if "students" in section.keys() and len(section["students"]) > 0:
            print(section["course_name"], section["section_number"], section["students"])
        else: print(f'{section["course_name"]} {section["section_number"]}, has no students')


def list_student_sections(db):
    students = db["students"].find({}).sort([("last_name", pymongo.ASCENDING),
                                             ("first_name", pymongo.ASCENDING)])
    for student in students:
        #checks if a student are enrolled in section or not before calling their sections
        if "student_sections" in student.keys() and len(student["student_sections"]) > 0:
            print(student["last_name"], student["first_name"], student["student_sections"])
        else: print(f'{student["last_name"]} {student["first_name"]}, has no sections')


def list_student_major(db):
    students = db["students"].find({}).sort([("last_name", pymongo.ASCENDING),
                                             ("first_name", pymongo.ASCENDING)])
    for student in students:
        if "major" in student:
            print(student["last_name"], student["first_name"], student["major"])
         

if __name__ == '__main__':
    password = "029014893"
    username = "trevordang01"
    project = "Cluster0"
    hash_name = "xm9bw6i"
    cluster = f"mongodb+srv://{username}:{password}@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority"
    print(f"Cluster: mongodb+srv://{username}:********@{project}.{hash_name}.mongodb.net/?retryWrites=true&w=majority")
    client = MongoClient(cluster)
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["Demonstration"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())

    db["departments"].drop()
    db["courses"].drop()
    db["sections"].drop()
    db["students"].drop()
    db.create_collection("departments", validator=DEPARTMENT_VALIDATOR)
    db.create_collection("courses", validator=COURSE_VALIDATOR)
    db.create_collection("sections", validator=SECTION_VALIDATOR)
    db.create_collection("students", validator=STUDENT_VALIDATOR)
    departments = db["departments"]
    # # create uniqueness constraints
    departments.create_index("name", unique=True)
    departments.create_index("abbreviation", unique=True)
    departments.create_index("chair_name", unique=True)
    departments.create_index([("building", pymongo.ASCENDING), ("office", pymongo.ASCENDING)], unique=True)
    # boilerplate data
    department = {
        "name": "Computer Engineering and Computer Science",
        "abbreviation": "CECS",
        "chair_name": "Mehrdad Aliasgari",
        "building": "ECS",
        "office": 100,
        "department_description": "The Computer Science Department of CSULB",
        "courses": ["Database Fundamentals"],
        "majors": [
            {
                "major_name": "Computer Science",
                "major_description": "This major focuses on software development and computer systems"
            },
            {
                "major_name": "Computer Engineering",
                "major_description": "This major focuses on computer hardware and digital systems"
            }
        ]
    }
    db.departments.insert_one(department)
    course = {
        "department_abbreviation": "CECS",
        "course_number": 323,
        "course_name": "Database Fundamentals",
        "course_description": "Learn the fundamentals of relational databases",
        "units": 3
    }
    db.courses.insert_one(course)
    section = {
        "department_abbreviation": "CECS",
        "course_number": 323,
        "course_name": "Database Fundamentals",
        "section_number": 1,
        "semester": "Summer I",
        "year": 2023,
        "building": "ECS",
        "room": 405,
        "schedule": "TuTh",
        "start_time": "9:00am",
        "instructor": "David Brown"
    }
    db.sections.insert_one(section)
    db.courses.update_one(
        {"department_abbreviation": section["department_abbreviation"], "course_number": section["course_number"]},
        {"$push": {"sections": ObjectId(section["_id"])}})
    student = {
        "first_name": "Trevor",
        "last_name": "Dang",
        "email": "tdang@gmail.com",
        "major": [{
            "major_name": "Computer Science",
            "declarations_date": "2023-06-28"
        }]
    }
    db.students.insert_one(student)

    students = db["students"]
    student_count = students.count_documents({})
    print(f"Students in the collection so far: {student_count}")

    # Set up the students collection
    students_indexes = students.index_information()
    if 'students_last_and_first_names' in students_indexes.keys():
        print("first and last name index present.")
    else:
    # Create a single UNIQUE index on BOTH the last name and the first name
        students.create_index([('last_name', pymongo.ASCENDING), ('first_name', pymongo.ASCENDING)],
                              unique=True,
                              name="students_last_and_first_names")
    if 'students_e_mail' in students_indexes.keys():
        print("e-mail address index present.")
    else:
    # Create a UNIQUE index on just the e-mail address
        students.create_index([('e_mail', pymongo.ASCENDING)], unique=True, name='students_e_mail')
    pprint(students.index_information())

    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)

 