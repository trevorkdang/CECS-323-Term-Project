from Menu import Menu
from Option import Option

"""
This little file just has the menus declared.  Each variable (e.g. menu_main) has 
its own set of options and actions.  Although, you'll see that the "action" could
be something other than an operation to perform.

Doing the menu declarations here seemed like a cleaner way to define them.  When
this is imported in main.py, these assignment statements are executed and the 
variables are constructed.  To be honest, I'm not sure whether these are global
variables or not in Python.
"""

# The main options
menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add", "add(db)"),
    Option("List", "list_objects(db)"),
    Option("Delete", "delete(db)"),
    #    Option("Boilerplate Data", "boilerplate(db)"),
    Option("Exit this application", "pass")
])

add_menu = Menu('add', 'Please indicate what you want to add:', [
    Option("Department", "add_department(db)"),
    Option("Course", "add_course(db)"),
    Option("Section", "add_section(db)"),
    Option("Major", "add_major(db)"),
    Option("Student", "add_student(db)"),
    Option("Section to Student", "add_section_student(db)"),
    Option("Student to Section", "add_student_section(db)"),
    # Option("Student to Major", "add_student_major(db)"),
    Option("Major to Student", "add_major_student(db)"),
    Option("Exit", "pass")
])

delete_menu = Menu('delete', 'Please indicate what you want to delete from:', [
    Option("Department", "delete_department(db)"),
    Option("Course", "delete_course(db)"),
    Option("Section", "delete_section(db)"),
    Option("Major", "delete_major(db)"),
    Option("Student", "delete_student(db)"),
    #    Option("Student to Major", "delete_student_major(db)"),
    Option("Major from Student", "delete_major_student(db)"),
    Option("Section from Student", "delete_section_student(db)"),
    Option("Student from Section", "delete_student_section(db)"),
    Option("Exit", "pass")
])

list_menu = Menu('list', 'Please indicate what you want to list:', [
    Option("Departments", "list_department(db)"),
    Option("Courses", "list_course(db)"),
    Option("Sections", "list_section(db)"),
    Option("Majors", "list_majors(db)"),
    Option("Students", "list_student(db)"),
    Option("Student's Major", "list_student_major(db)"),
    #    Option("Major to Student", "list_major_student(db)"),
    Option("Student's Section", "list_student_sections(db)"),
    Option("Section's Student", "list_section_students(db)"),
    Option("Exit", "pass")
])
