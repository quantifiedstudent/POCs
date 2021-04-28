import zipfile
import requests
import json
import time
import os
import re
from zipfile import ZipFile


SAVE_PATH = ""
STUDENT_ID = ""

class Canvas():

    def __init__(self, apikey, save_path):
        self.apikey = apikey
        self.save_path = save_path
        self.headers = {"Authorization" : "Bearer " + apikey}
        self.targetURL = "https://fhict.instructure.com/api/v1/"

    def get_account(self):
        tmp = requests.get(self.targetURL + "lti/accounts/{}".format(""))

        
    """ Retrieves a list with all modules from the FHICT Instructure API """
    def get_modules(self, course_id):
        tmp = requests.get(self.targetURL + "courses/{c_id}/modules".format(c_id = course_id), headers=self.headers)
        print(tmp)
        return json.loads(tmp.text)

    """ Retrieves a list with all assignments from the FHICT Instructure API """
    def get_assignments(self, course_id, ):
        tmp = requests.get(self.targetURL + "courses/{c_id}/assignments?per_page=100".format(c_id = course_id), headers = self.headers)
        return json.loads(tmp.text)

    """ Retrieves a list with all submissions from the FHICT Instructure API """
    def get_submissions(self, course_id, assignment_id):
        tmp = requests.get(self.targetURL + "courses/{c_id}/assignments/{a_id}/submissions".format(c_id = course_id, a_id = assignment_id), headers = self.headers)
        return json.loads(tmp.text)

    """" Gets all enrolled courses of the user of who the apikey is being used"""
    def get_courses(self):
        tmp = requests.get(self.targetURL + "courses", headers=self.headers)
        return json.loads(tmp.text)

    """ Gets the file and write it in chunks to the designated filepath """
    def download_url(self, url, path, chunk_size=128):
        r = requests.get(url, stream=True, headers=self.headers)                     # Create web request, specify STREAMING option
        with open(path, "wb") as fd:                                            # Open file as wb (binary) to start writing chunks towards it
            for chunk in r.iter_content(chunk_size=chunk_size):
                fd.write(chunk)                                                 # Write byte chunks to file

    """ Download all files which got handed in during the assignment """
    def get_all_assignment_handins(self, attachments, assignment):
        for attachment in attachments:
            savedir = re.sub("[^0-9a-zA-Z,]+", "", assignment['name'],)         # Generate save directory for assignment
            filepath =  SAVE_PATH + "/{}".format(savedir)                       # Update save path to be inside of the assignment folder
            print("saving file to {}".format(filepath))        
            if not os.access(filepath, os.W_OK):    
                os.mkdir(filepath)
            print("Downloading.... {d_url}".format(d_url = attachment['display_name']))
            self.download_url(attachment['url'], filepath + "/{name}".format(name=attachment['display_name']))

    """ Updates the default save path of handed-in files """
    def update_save_path(self, student_id):
        global SAVE_PATH                                                        # Import global save path
        SAVE_PATH = self.save_path                                           # Reset save path to default, to prevent chaining    
        SAVE_PATH += "/{}".format(student_id)                                   # Update save path to append studentID        
        if not os.access(SAVE_PATH, os.W_OK):                                   
                os.makedirs(SAVE_PATH)

    """ Loop through all of the saved files recursively and extract them from zip if necessary"""
    def extract_zips(self):
        for items in os.walk(self.save_path):
            for walkedfile in items[2]:
                if walkedfile.endswith(".zip"):                                 # Zip file is found
                    zip_file = zipfile.ZipFile(items[0] + '/' +  walkedfile)    # Create ZipFile instance
                    zip_file.extractall(items[0])                               # Extract all items from zip
                    zip_file.close()                                            # Close zip file
                    time.sleep(1)                                               # TODO Is this sleep necessary? 
                    os.remove(items[0] + '/' +  walkedfile)                     # Remove zip file, as content is now extracted

