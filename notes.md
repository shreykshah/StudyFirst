lot of college courses are percentile based, but don't give out percentile rankings easily - made this to estimate percentile with the data that Canvas provides students

Due to the abysmally low amount of data given to students, this will usually estimate a student closer to the median than they likely are. If needed, one could probably add an adjustment factor to estimate at a much greater accuracy (ask the prof on'es true percentile and calibrate the program off of that for that class).

The Canvas API for students pulls less data than is given graphically. This can probably be reverse engineered if needed.

Decided to use downloaded HTML rather than scraping off of a login, as Canvas leaves many courses that are useless (uni safety courses, etc), it would require login/2fa at every run, and one loses the ability to choose a subset of the courses (an A in course X is at 50th percentile so don't put course X in the calculation). Transition to scraping off Selenium would be trivial if needed (needs to be Selenium due to the 2fa login with cookie exp req)
