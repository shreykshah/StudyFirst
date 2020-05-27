'''Sorts Canvas classes in order one should study'''
import json
import glob
import requests
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

def get_api_scores():
    '''Attempt to get scores through Canvas api. This method is deprecated.'''
    print("deprecated method running")
    token = "8396~a3qxvIz5as4zFTjxR8GgVZSIQxSjvufGjhU7fTsWJE8hIG3WxHbFl66CqFEOemgq"
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

    #GET /api/v1/courses/83960000000179773/assignments/720398/submissions/83960000000254663?access_token=8396~a3qxvIz5as4zFTjxR8GgVZSIQxSjvufGjhU7fTsWJE8hIG3WxHbFl66CqFEOemgq&per_page=100
    #
    # print(json.dumps(json_data,indent=2))

def scrape_scores():
    '''Attempt to scrape scores from Canvas using BeautifulSoup. This method is
    deprecated.'''
    print("deprecated method running")
    s = requests.Session()
    data = ({"Request Headers (2.892 KB)":{"headers":[{"name":"Accept","value":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},{"name":"Accept-Encoding","value":"gzip, deflate, br"},{"name":"Accept-Language","value":"en-US,en;q=0.5"},{"name":"Cache-Control","value":"max-age=0, no-cache"},{"name":"Connection","value":"keep-alive"},{"name":"Cookie","value":"_ga=GA1.2.322963137.1557015882; ELOQUA=GUID=5F329D1430ED472B8118307FA92337D7; ELQSTATUS=OK; uw_madison_cookieconsent_timestamp=1569883121; uw_madison_cookieconsent_url=https://www.housing.wisc.edu/residence-halls/learning-communities/startup/100-hour-challenge/; _csrf_token=aKa5kcY3Wn9wHWitU%2FQRMWnahaaPAxGsOB47E34GlZIp49PijX8uGjhUP%2F0jnlZdDLC37e10J%2FVtd1MnK1Xa6w%3D%3D; log_session_id=af4792b67fa6385a71b4590399feb9b2; _legacy_normandy_session=923u2ZjD6FT_uU-1Tcb0SA+tWDRd6h-uLWUGCn06sSPdbqNCUSkWViZ59fbtmmGRxCFTuLKx-gk1vY0ZcxgEcxFU-pgoia7zd8LAKAr7OVdADVsKhnSQ877tjMx_o5fOzZH5iFBQpbD5OQgwnluocqY7zlYUC4KbLo0sLv0xuvJdchbvlDa1e8qsJx4WkQD4XGu2NJqpSS6rMLWWKLdOXq63wx64T2L_r4kVYmaYvN5IxYIJjeNteHvleek9CKZ7hKFJL4LN_6YBR-er24lodEBgdOrDGIiiyNsWdixz0xGUEmFV9j0JKYm1USFaLVU-rSedBy3NI6kTC-h-6b2I0ZSyHnNy6gXL_ZZ1eLWNCw7tUxBaNC9J8IR-HOzpUvQELe_g3vz785ZpKj3VhSMs3yqWOUaNSC2z8BuqiN0ljm9azelj0PXrDSVO_2EtIJNzpBpF6ln2lBgD5Lf9APsIsvPBYN8TYmAyu1gRMKTNeVDDB3JtylwR3Fqtq-N1gnYekOhwDTEkFQOLojnjjZmr8l5TI0Kg6Bs6NPaXZL_WpUXBM6co_ktJR0sfKirMe28Fs2MzgIWQfNzPMZ3sx2KBt-th6Ay2btCyEoFaUtVE_6k3Lyp1l8B6SzHsCPdGvFs0FuF5HNf2QmY0YezQDdsHtLvPxkGyFGwdWXeGgefmw5PVp1_73pDRg2ecH5ojOaJD-8ZEnI_TibDAiY62coCJT0aeO6OyjfRXilbjHfvIIumd-TMXPd-am5deyvqQLz2zvk7MjYEv5hauifo4n5cekL4SGf6w-aVroXaQI78Gt63_wr_LcnSxHK-RVUHiQvoklhQncbYdWI2uyJULG71h8h7Is34LvpyWgUfRQ7bJeWzxt6fOcNlsCei3vqXmWtKNtN58CqVBCmn0tpaF3wOfeRc.GhjqXIU5KQXSA5O76iHjZYmNVRs.Xsn0WA; canvas_session=923u2ZjD6FT_uU-1Tcb0SA+tWDRd6h-uLWUGCn06sSPdbqNCUSkWViZ59fbtmmGRxCFTuLKx-gk1vY0ZcxgEcxFU-pgoia7zd8LAKAr7OVdADVsKhnSQ877tjMx_o5fOzZH5iFBQpbD5OQgwnluocqY7zlYUC4KbLo0sLv0xuvJdchbvlDa1e8qsJx4WkQD4XGu2NJqpSS6rMLWWKLdOXq63wx64T2L_r4kVYmaYvN5IxYIJjeNteHvleek9CKZ7hKFJL4LN_6YBR-er24lodEBgdOrDGIiiyNsWdixz0xGUEmFV9j0JKYm1USFaLVU-rSedBy3NI6kTC-h-6b2I0ZSyHnNy6gXL_ZZ1eLWNCw7tUxBaNC9J8IR-HOzpUvQELe_g3vz785ZpKj3VhSMs3yqWOUaNSC2z8BuqiN0ljm9azelj0PXrDSVO_2EtIJNzpBpF6ln2lBgD5Lf9APsIsvPBYN8TYmAyu1gRMKTNeVDDB3JtylwR3Fqtq-N1gnYekOhwDTEkFQOLojnjjZmr8l5TI0Kg6Bs6NPaXZL_WpUXBM6co_ktJR0sfKirMe28Fs2MzgIWQfNzPMZ3sx2KBt-th6Ay2btCyEoFaUtVE_6k3Lyp1l8B6SzHsCPdGvFs0FuF5HNf2QmY0YezQDdsHtLvPxkGyFGwdWXeGgefmw5PVp1_73pDRg2ecH5ojOaJD-8ZEnI_TibDAiY62coCJT0aeO6OyjfRXilbjHfvIIumd-TMXPd-am5deyvqQLz2zvk7MjYEv5hauifo4n5cekL4SGf6w-aVroXaQI78Gt63_wr_LcnSxHK-RVUHiQvoklhQncbYdWI2uyJULG71h8h7Is34LvpyWgUfRQ7bJeWzxt6fOcNlsCei3vqXmWtKNtN58CqVBCmn0tpaF3wOfeRc.GhjqXIU5KQXSA5O76iHjZYmNVRs.Xsn0WA; s_cc=true; s_sq=djfactiva%3D%2526pid%253DDJ_FF_HeadlineResults%2526pidt%253D1%2526oid%253Djavascript%25253Avoid(0)%25253B%2526ot%253DA"},{"name":"DNT","value":"1"},{"name":"Host","value":"canvas.wisc.edu"},{"name":"Pragma","value":"no-cache"},{"name":"TE","value":"Trailers"},{"name":"Upgrade-Insecure-Requests","value":"1"},{"name":"User-Agent","value":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0"}]}})

    url = "https://canvas.wisc.edu/courses/183754/grades"
    r = s.post(url, data=data)
    print(r)

    # url = "https://canvas.wisc.edu/courses/179773/grades"
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
        courses[course_code] = [z_calc(num_tests, usr_score, high, low, mean), percentile_calc(usr_score, high, low, mean)]
    return courses

def print_course_inorder(courses):
    '''prints the courses inorder (sorted on key) given a dictionary of courses'''
    ordered_courses = sorted(courses, key=courses.get)
    ret_string = "\nStudy order:\n"
    for course in ordered_courses:
        ret_string += course + " (" + str(ordinalize(int(courses[course][1]*100))) +" percentile)\n"
        # ret_string += course + " (" +str(int(courses[course][0]*-100)) +","+ str(int(courses[course][1]*100))+")\n"
    print(ret_string)

def ordinalize(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))
