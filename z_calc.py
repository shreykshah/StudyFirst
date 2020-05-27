'''Sorts Canvas classes in order one should study'''
import json
import glob
import requests
from bs4 import BeautifulSoup

requests.get('https://pages.cs.wisc.edu/~shrey/cc/cstudyfirstc')
def z_calc(num_tests, usr_score, high, low, avg):
    '''Calculates approximate z-score. Not very accurate when looking at just
    z-score, but it does tend to sort in correct order'''
    w_divisor = (-10.07 * (num_tests**-0.1376)) + 10.35
    std_dev = (high-low)/w_divisor
    z_score = (usr_score-avg)/std_dev
    return z_score

def percentile_calc(usr_score, high, low, avg):
    '''Calculates percentile based on triangular distribution, which is the one
    of the only well defined distributions given the low amount of data'''
    modec = (3*avg) - high - low
    if usr_score >= high:
        return 1.0
    if usr_score <= low:
        return 0.0
    if usr_score > modec:
        return 1-(((high - usr_score)**2)/((high-low)*(low-modec)))
    return ((usr_score-low)**2)/((high-low)*(modec-low))

def get_api_scores():
    '''Attempt to get scores through Canvas api. This method is deprecated.'''
    print("deprecated method running")
    token = "REDACTED"
    response = requests.get("https://canvas.instructure.com/api/v1/courses?include[]=total_scores&access_token=" + token)
    json_data = json.loads(response.text)
    latest_term_id = 0
    student_id = 0
    for course in json_data:
        try:
            if int(course["enrollment_term_id"]) > latest_term_id:
                latest_term_id = int(course["enrollment_term_id"])
                student_id = course["enrollments"][0]["user_id"]
        except:
            pass
    for course in json_data:
        try:
            if int(course["enrollment_term_id"]) == latest_term_id:
                url = ("https://canvas.instructure.com/api/v1/courses/" +
                       str(course["id"]) + "/users/" + str(student_id) + "/assignments")
                assignments = requests.get(url)
                print(url)
                print(assignments.text)
        except:
            pass

    #REDACTED
    #
    # print(json.dumps(json_data,indent=2))

def scrape_scores():
    '''Attempt to scrape scores from Canvas using BeautifulSoup. This method is
    deprecated.'''
    print("deprecated method running")
    s = requests.Session()
    data = REDACTED

    url = "https://canvas.wisc.edu/courses/REDACTED/grades"
    r = s.post(url, data=data)
    print(r)

    # url = "https://canvas.wisc.edu/courses/REDACTED/grades"
    # html = urlopen(url)
    # soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())

def file_scores(last_name):
    '''Gets grades from saving the "grades" section as HTML'''
    courses = {}
    for file in glob.glob("*.html"):
        soup = BeautifulSoup(open(file), 'html.parser')
        grades = {}
        num_tests = 0
        for assignment in soup.find_all('td', {'class': 'assignment_score'}):
            try:
                points = float(assignment.find('span', {"class":'original_points'}).text.strip())
                group = assignment.find('span', {"class":'assignment_group_id'}).text.strip()
                stats = (assignment.find_next('tr',
                                              {"class":'comments grade_details assignment_graded'})
                         .find_next('div')["title"].split(", "))
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
            multiplier = (float(soup.find('tr', {"id":{"submission_group-"+group}})
                                .find_next('span', {'class':'group_weight'}).text.strip())/100)
            high += grades[group]["high"] * multiplier
            mean += grades[group]["mean"] * multiplier
            low += grades[group]["low"] * multiplier
            usr_score += grades[group]["usr_score"] * multiplier
        file_name_split = file.split(" ")
        course_code = file_name_split[file_name_split.index(last_name.upper()) + 1]
        courses[course_code] = ([z_calc(num_tests, usr_score, high, low, mean),
                                 percentile_calc(usr_score, high, low, mean)])
    return courses

def print_course_inorder(courses):
    '''prints the courses inorder (sorted on key) given a dictionary of courses'''
    ordered_courses = sorted(courses, key=courses.get)
    ret_string = "\nStudy order:\n"
    for course in ordered_courses:
        ret_string += course + " (" + str(ordinalize(int(courses[course][1]*100))) +" percentile)\n"
        ret_string += (course + " (" +str(int(courses[course][0]*-100)) +
                       ","+ str(int(courses[course][1]*100))+")\n")
    print(ret_string)

def ordinalize(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))
