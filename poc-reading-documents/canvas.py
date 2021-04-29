import zipfile
import requests
import json
import time
import os
import re
from zipfile import ZipFile

apikey = "DvA4kMN3DDAWT2f8VD5YDMCoFR1RyaJJpJeqNLXUpeSGS09WpH6bngfZHK8OHyQv"

targetURL = "https://fhict.instructure.com/api/v1/"
DEFAULT_SAVE_PATH = "poc-reading-documents/downloads" 
SAVE_PATH = ""

""" Authentication headers used for communicating with Instructure"""
headers = {"Authorization" : "Bearer " + apikey}

""" Retrieves a list with all modules from the FHICT Instructure API """
def get_modules(course_id):
    tmp = requests.get(targetURL + "courses/{c_id}/modules".format(c_id = course_id), headers=headers)
    return json.loads(tmp.text)

""" Retrieves a list with all assignments from the FHICT Instructure API """
def get_assignments(course_id, ):
    tmp = requests.get(targetURL + "courses/{c_id}/assignments".format(c_id = course_id), headers = headers)
    return json.loads(tmp.text)

""" Retrieves a list with all submissions from the FHICT Instructure API """
def get_submissions(course_id, assignment_id):
    tmp = requests.get(targetURL + "courses/{c_id}/assignments/{a_id}/submissions".format(c_id = course_id, a_id = assignment_id), headers = headers)
    return json.loads(tmp.text)

"""" Gets all enrolled courses of the user of who the apikey is being used"""
def get_courses():
    tmp = requests.get(targetURL + "courses", headers=headers)
    return json.loads(tmp.text)

""" Gets the file and write it in chunks to the designated filepath """
def download_url(url, path, chunk_size=128):
    r = requests.get(url, stream=True, headers=headers)
    with open(path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

""" Download all files which got handed in during the assignment """
def get_all_assignment_handins(attachments, assignment):
    for attachment in attachments:
        savedir = re.sub("[^0-9a-zA-Z,]+", "", assignment['name'],)
        filepath =  SAVE_PATH + "/{}".format(savedir)
        if not os.access(filepath, os.W_OK):
            os.mkdir(filepath)
        print("Downloading.... {d_url}".format(d_url = attachment['display_name']))
        download_url(attachment['url'], filepath + "/{name}".format(name=attachment['display_name']))

""" Updates the default save path of handed-in files """
def update_save_path(student_id):
    global SAVE_PATH
    SAVE_PATH = DEFAULT_SAVE_PATH
    SAVE_PATH += "/{}".format(student_id)
    if not os.access(SAVE_PATH, os.W_OK):
            os.mkdir(SAVE_PATH)

""" Loop through all of the saved files recursively and extract them from zip if necessary"""
def extract_zips():
    for items in os.walk(DEFAULT_SAVE_PATH):
        for walkedfile in items[2]:
            if walkedfile.endswith(".zip"):
                zip_file = zipfile.ZipFile(items[0] + '/' +  walkedfile)
                zip_file.extractall(items[0])
                zip_file.close()
                time.sleep(2)
                os.remove(items[0] + '/' +  walkedfile)

if __name__ == "__main__":
    for course in get_courses():
        for assignment in get_assignments(course['id']):
            for submission in get_submissions(course['id'], assignment['id']):
                if('attachments' in submission):
                    update_save_path(submission['user_id'])
                    get_all_assignment_handins(submission['attachments'], assignment)

    extract_zips()