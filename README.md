# StudyFirst
Detect which courses you should study for first from Canvas.

To use:
1) Navigate to Canvas's "grades" subpage for your desired course
2) Click "⌘S" and select "Webpage, HTML only" and save the file to the repository
3) Run the program in the command line (navigate to your command line interface and run "python runner.py")
4) Enter last name of student when prompted

The program will calculate the order in which the student should study, giving highest preference to the course the student is the most behind in. It will then attempt to calculate the student's percentile, although this number is simply a rough estimate given to show a little more data than just ordinality (also so one may determine how much time to spend on each subject). The list is in decending order, where the first item is the one the student should study for first.
