from tika.tika import parse
from POCs.DocumentParsingPOC.submissionparser import parse_file
from POCs import canvas


def get_student_dataset(canvas_student_id):
    student_data = {}

    # Get canvas assignments of student
    # Download all possible assignments from student (NOT ALL SUBSCRIBED COURSES FROM STUDENT)
    # Loop over all downloaded assignments and extract from zip where necessary
    # Loop over all assignments and parse them respectively

    submissions = []
    for hand_in in assignments:
        # TODO check if only folder and not file
        for submission in hand_in:
            # TODO check if only file and not folder
            submissions.append(parse_student_submission(submission))
            
    # Return all parsed documents in dictionary or JSON
    student_data["hand-ins"] = submissions
    pass


def parse_student_submission(filename):             # Filename is expected to be the static location of the file 
    return parse_file(filename)