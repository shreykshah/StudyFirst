import z_calc
import numpy as np
from scipy.integrate import quad

courses = z_calc.file_scores(input("Please enter your last name: "))
# for course in courses:
#     print(courses[course])
#     zoe_percentile, _ = quad(z_calc.normalProbabilityDensity, np.NINF, courses[course])
#     print('Zoe: ', zoe_percentile)

z_calc.print_course_inorder(courses)
