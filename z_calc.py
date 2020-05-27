'''Sorts Canvas classes in order one should study'''
import glob
from bs4 import BeautifulSoup

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

def file_scores(last_name):
    '''Gets grades from saving the "grades" section as HTML'''
    courses = {}
    bstat = [0.0, 0.0, 0.0, 0.0]
    for file in glob.glob("*.html"):
        soup = BeautifulSoup(open(file), 'html.parser')
        grades = {}
        num_tests = 0
        for assignment in soup.find_all('td', {'class': 'assignment_score'}):
            try:
                bstat[3] = float(assignment.find('span', {"class":'original_points'}).text.strip())
                group = assignment.find('span', {"class":'assignment_group_id'}).text.strip()
                stats = (assignment.find_next('tr',
                                              {"class":'comments grade_details assignment_graded'})
                         .find_next('div')["title"].split(", "))
                bstat[0] = float(stats[0][5:])
                bstat[1] = float(stats[1][5:])
                bstat[2] = float(stats[2][4:])

                if group not in grades:
                    grades[group] = {
                        "high": 0.0,
                        "mean": 0.0,
                        "low": 0.0,
                        "usr_score": 0.0,
                    }
                grades[group]["high"] += bstat[1]
                grades[group]["mean"] += bstat[0]
                grades[group]["low"] += bstat[2]
                grades[group]["usr_score"] += bstat[3]
                num_tests += 1
            except ValueError:
                pass
        bstat[0] = bstat[1] = bstat[2] = bstat[3] = 0.0
        for group in grades:
            multiplier = (float(soup.find('tr', {"id":{"submission_group-"+group}})
                                .find_next('span', {'class':'group_weight'}).text.strip())/100)
            bstat[1] += grades[group]["high"] * multiplier
            bstat[0] += grades[group]["mean"] * multiplier
            bstat[2] += grades[group]["low"] * multiplier
            bstat[3] += grades[group]["usr_score"] * multiplier
        file_name_split = file.split(" ")
        course_code = file_name_split[file_name_split.index(last_name.upper()) + 1]
        courses[course_code] = ([z_calc(num_tests, bstat[3], bstat[1], bstat[2], bstat[0]),
                                 percentile_calc(bstat[3], bstat[1], bstat[2], bstat[0])])
    return courses

def print_course_inorder(courses):
    '''prints the courses inorder (sorted on key) given a dictionary of courses'''
    ordered_courses = sorted(courses, key=courses.get)
    ret_string = "\nStudy order:\n"
    for course in ordered_courses:
        ret_string += course + " (" + str(ordinalize(int(courses[course][1]*100))) +" percentile)\n"
        # ret_string += (course + " (" +str(int(courses[course][0]*-100)) +
        #                ","+ str(int(courses[course][1]*100))+")\n")
    print(ret_string)

def ordinalize(num):
    '''add ordinal number suffix to numbers'''
    return str(num)+("th" if 4 <= num%100 <= 20 else {1:"st", 2:"nd", 3:"rd"}.get(num%10, "th"))
