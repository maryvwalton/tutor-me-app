import requests
import json

# from: https://stackoverflow.com/a/73802708
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buildexample.settings")
django.setup()

from myapp.models import Course

def check_if_year_valid(year):
    if (len(str(year)) != 2) or (type(year) is not int):
        raise ValueError("The entered year must be a two digit integer, like 22 or 23")


def check_if_semester_valid(semester):
    if semester not in ["fall", "spring"]:
        raise ValueError("The entered semester must either be 'fall' or 'spring'")


def validate_input(year, semester):
    check_if_year_valid(year)
    check_if_semester_valid(semester)


def get_semester_to_URL_number(semester):
    check_if_semester_valid(semester)
    semester_to_url_mapping = {"fall": "8", "spring": "2"}
    return semester_to_url_mapping[semester]


def return_all_department_mnemonics(year, semester):
    # Input handling
    semester = semester.lower()  # ensures "Spring" is treated the same as "SPRING" and "spring"
    validate_input(year, semester)

    # URL building
    base_url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula" \
               ".IScript_ClassSearchOptions?institution=UVA01"

    term_parameter = "&term=1" + str(year) + get_semester_to_URL_number(semester)
    full_url = base_url + term_parameter

    # requesting data
    r = requests.get(full_url)
    json_data = r.json()

    # JSON parsing
    list_of_search_fields = json_data["subjects"]

    mnemonics_list = []
    for entry in list_of_search_fields:
        mnemonics_list.append(entry["subject"])

    return mnemonics_list


def return_all_courses_from_department(year, semester, department):
    # Input handling
    semester = semester.lower()  # ensures "Spring" is treated the same as "SPRING" and "spring"
    validate_input(year, semester)
    # TODO: should probably validate "department" somehow - maybe make sure it exists in the list returned by
    #  return_all_department_mnemonics() above?

    # URL building
    base_url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula" \
               ".IScript_ClassSearch?institution=UVA01"

    term_parameter = "&term=1" + str(year) + get_semester_to_URL_number(semester)
    subject_parameter = "&subject=" + department

    base_url = base_url + term_parameter + subject_parameter

    current_page = 1  # used to handle getting several pages of json data
    page_parameter = "&page=" + str(current_page)

    # requesting data
    r = requests.get(base_url + page_parameter)
    json_data = r.json()

    while json_data:  # check whether the json response data is an empty or not

        # json parsing
        for entry in json_data:

            coursenum = int(entry["catalog_nbr"])
            title = entry["descr"]
            pnemonic = entry["subject"]

            if Course.objects.filter(title = title):
                continue
            elif coursenum > 4999:
                break

            course = Course(title = title, pnemonic = pnemonic, coursenum = coursenum)
            course.save()

        # incrementation
        current_page += 1
        page_parameter = "&page=" + str(current_page)
        r = requests.get(base_url + page_parameter)
        json_data = r.json()

# WARNING: THIS WILL TAKE AN EXTREMELY LONG TIME TO RUN AND YOU PROBABLY SHOULD NOT RUN IT
# Better to instead use return_all_courses_from_department() and fill database with courses from a single department
# one by one
def populate_database_with_all_courses(year, semester):
    # Input handling
    semester = semester.lower()  # ensures "Spring" is treated the same as "SPRING" and "spring"
    validate_input(year, semester)

    mnemonics_list = return_all_department_mnemonics(year, semester)

    for mnemonic in mnemonics_list:
        return_all_courses_from_department(year, semester, mnemonic)


<<<<<<< HEAD
######### Testing code by printing output of functions ###############
#<<<<<<< HEAD
# print(return_all_department_mnemonics(23, "fall"))
#<<<<<<< HEAD
#print(return_all_courses_from_department(23, "spring", "CS"))
#=======
#=======
#print(return_all_department_mnemonics(23, "fall"))
#>>>>>>> cf84f50368fdcb90a2ea96b3e8e812803a272485
print(return_all_courses_from_department(23, "spring", "CS"))
#>>>>>>> 7ab9528061cec6f723bc23a6e6e61080d8991fb7
=======
def delete_courses():
    for course in Course.objects.all().iterator():
        course.delete()
>>>>>>> aced67298c3ff9eb95bb69c2918b0365d837e815
