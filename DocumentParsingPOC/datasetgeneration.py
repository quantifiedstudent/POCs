from tika.tika import parse

from modules.submissionparser import parse_file
from modules.canvas import Canvas
import os
import json


DOWNLOAD_PATH = "../Quantified-Student/POCs/DocumentParsingPOC/downloads"
STUDENT_API_KEY = "DvA4kMN3DDAWT2f8VD5YDMCoFR1RyaJJpJeqNLXUpeSGS09WpH6bngfZHK8OHyQv"

""" Generate a dataset from the student_id"""
def get_student_dataset(canvas_student_id):
    student_data = {}

    # TODO extract this to a unique method in `Canvas.py`, 
        # TODO 1.1 Find out to find personal courses based on API key
    canvas =  Canvas(STUDENT_API_KEY, DOWNLOAD_PATH)                                                        # Create new Canvas instance with the Studnet API key
    for course in canvas.get_courses():
        if "Niek" in course['name']:                                                                        #TODO Fix hardcoded check
            for assignment in canvas.get_assignments(course['id']):
                for submission in canvas.get_submissions(course['id'], assignment['id']):
                    if('attachments' in submission):
                        canvas.update_save_path(submission['user_id'])
                        canvas.get_all_assignment_handins(submission['attachments'], assignment)
    # TODO extract dit naar een methode ergens ofzo lol
    # TODO Waarom extract een zip naar een subfolder?? 
    canvas.extract_zips()

    # Create a list of all folders in the download directory, which can be looped over. #TODO Only loop over personal course when there is a collection of courses
    tmp = [name for name in os.listdir(DOWNLOAD_PATH) if os.path.isdir(os.path.join(DOWNLOAD_PATH+ "/{}".format(name)))]
    for student_folder in tmp:
        student_data[student_folder] = {}
        hand_ins_folder = os.path.join(DOWNLOAD_PATH+ "/{}".format(student_folder))
        for assignment in os.listdir(hand_ins_folder):
            student_data[student_folder][assignment] = {}
            submissions = []
            # TODO Fix the hand_ins column to append to the greater dictionary
            hand_ins = [dname for dname in os.listdir(hand_ins_folder + "/{}".format(assignment))]    
            for submission in hand_ins:
                file_submission = hand_ins_folder + "/{assignment}/{submission}".format(assignment=assignment, submission=submission)
                if(os.path.isfile(file_submission)):
                    submissions.append(parse_file(file_submission))
            student_data[student_folder][assignment]["hand-ins"] = submissions

    print(student_data)

    student_data["hand-ins"] = submissions

    """ Generating JSON file with all student data """
    with open("test.json", "w+") as outfile:
        json.dump(student_data, outfile)
    # for hand_in in assignments:
    #     # TODO check if only folder and not file
    #     for submission in hand_in:
    #         # TODO check if only file and not folder
    #         submissions.append(parse_student_submission(submission))

    # # Return all parsed documents in dictionary or JSON
    pass

def parse_student_submission(filename):             # Filename is expected to be the static location of the file 
    return parse_file(filename)

get_student_dataset(1)