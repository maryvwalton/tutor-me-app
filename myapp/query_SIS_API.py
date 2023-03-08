import requests
import json


def check_if_year_valid(year):
    if (len(str(year)) != 2) or (type(year) is not int):
        raise Exception("The entered year must be a two digit integer, like 22 or 23")


def check_if_semester_valid(semester):
    if semester not in ["fall", "spring"]:
        raise Exception("The entered semester must either be 'fall' or 'spring'")


def validate_input(year, semester):
    check_if_year_valid(year)
    check_if_semester_valid(semester)


def return_all_department_mnemonics(year, semester):
    # Input handling
    semester = semester.lower()  # ensures "Spring" is treated the same as "SPRING" and "spring"
    validate_input(year, semester)

    # URL building
    semester_to_url_mapping = {"fall": "8", "spring": "12"}
    base_url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula" \
               ".IScript_ClassSearchOptions?institution=UVA01&term=1"
    full_url = base_url + str(year) + semester_to_url_mapping[semester]

    # requesting data
    r = requests.get(full_url)
    json_data = r.json()

    # JSON parsing
    list_of_search_fields = json_data["subjects"]

    mnemonics_list = []
    for entry in list_of_search_fields:
        mnemonics_list.append(entry["subject"])

    return mnemonics_list


def return_courses_by_instructor(year, semester, instructor_name):
    pass


print(return_all_department_mnemonics(22, "fall"))
