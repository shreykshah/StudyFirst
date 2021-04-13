lot of college courses are percentile based, but don't give out percentile rankings easily - made this to estimate percentile with the data that Canvas provides students

Due to the abysmally low amount of data given to students, this will usually estimate a student closer to the median than they likely are. If needed, one could probably add an adjustment factor to estimate at a much greater accuracy (ask the prof one's true percentile and calibrate the program off of that for that class).

The Canvas API for students pulls less data than is given graphically. This can probably be reverse engineered if needed. Should move to Selenium scraping or Canvas API as it's too hard to use otherwise

FAIL if inaccurate group weight - some professors don't input group weights into Canvas

Can probably be a proper product if bundled with rest of university toolkit and given nice polish (UI), where you have each person generate a token once through Canvas API or login via Selenium and all data is pulled (no longer need last name). Can also implement a feature where you compare against cutoffs (user inputted) for the course to maximize GPA rather than percentiles in the course
