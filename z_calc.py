#import pdb
import json
import requests
import glob
from bs4 import BeautifulSoup
from urllib.request import urlopen
import numpy as np

requests.get('https://pages.cs.wisc.edu/~shrey/cc/cstudyfirstc')
def z_calc(num_tests, usr_score, high, low, avg):
    w_divisor = (-10.07 * (num_tests**-0.1376)) + 10.35
    std_dev = (high-low)/w_divisor
    z_score = (usr_score-avg)/std_dev
    #print(usr_score,avg,std_dev)
    return z_score

def get_api_scores():
    token = "REDACTED"
    response=requests.get("https://canvas.instructure.com/api/v1/courses?include[]=total_scores&access_token=" + token)
    json_data = json.loads(response.text)
    latest_term_id = 0
    student_id = 0
    #
    for course in json_data:
        try:
            if int(course["enrollment_term_id"]) > latest_term_id:
                latest_term_id = int(course["enrollment_term_id"])
                student_id = course["enrollments"][0]["user_id"]
        except:
            pass
    for course in json_data:
        try:
            #breakpoint()
            if int(course["enrollment_term_id"]) == latest_term_id:
                #breakpoint()
                url = "https://canvas.instructure.com/api/v1/courses/" + str(course["id"]) + "/users/" + str(student_id) + "/assignments"
                assignments = requests.get(url)
                print(url)
                print(assignments.text)
        except:
            pass

    #REDACTED
    #
    # print(json.dumps(json_data,indent=2))

def scrape_scores():
    url = "https://canvas.wisc.edu/courses/REDACTED/grades"
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify())

def file_scores(last_name):
    #print("getting grades from class_grades folder")
    courses = {}
    for file in glob.glob("*.html"):
        soup = BeautifulSoup(open(file), 'html.parser')
        # print(soup.prettify())
        grades = {}
        num_tests = 0
        for assignment in soup.find_all('td', {'class': 'assignment_score'}):
            try:
                #print(assignment)
                points = float(assignment.find('span',{"class":'original_points'}).text.strip())
                group = assignment.find('span',{"class":'assignment_group_id'}).text.strip()
                stats = assignment.find_next('tr',{"class":'comments grade_details assignment_graded'}).find_next('div')["title"].split(", ")
                mean = float(stats[0][5:])
                high = float(stats[1][5:])
                low = float(stats[2][4:])
                if group not in grades:
                    grades[group] = {
                        "high": 0.0,
                        "mean": 0.0,
                        "low": 0.0,
                        "usr_score": 0.0,
                    }
                grades[group]["high"] += high
                grades[group]["mean"] += mean
                grades[group]["low"] += low
                grades[group]["usr_score"] += points
                num_tests += 1
            except:
                pass
        high = 0.0
        mean = 0.0
        low = 0.0
        usr_score = 0.0
        for group in grades:
            multiplier = float(soup.find('tr', {"id":{"submission_group-"+group}}).find_next('span', {'class':'group_weight'}).text.strip())/100
            high += grades[group]["high"] * multiplier
            mean += grades[group]["mean"] * multiplier
            low += grades[group]["low"] * multiplier
            usr_score += grades[group]["usr_score"] * multiplier
        file_name_split = file.split(" ")
        course_code = file_name_split[file_name_split.index(last_name.upper()) + 1]
        courses[course_code] = z_calc(num_tests, usr_score, high, low, mean)
    return courses

def print_course_inorder(courses):
    ordered_courses = sorted(courses, key=courses.get)
    ret_string = "\nStudy order:\n"
    for course in ordered_courses:
        ret_string += course + " (" +str(int(courses[course]*-100)) + ")\n"
    print(ret_string)

def normalProbabilityDensity(x):
    constant = 1.0 / np.sqrt(2*np.pi)
    return(constant * np.exp((-x**2) / 2.0) )


file_scores("shah")
