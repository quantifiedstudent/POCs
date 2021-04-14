import json
from bs4 import BeautifulSoup



file = "assignments.json"

parsedJson = None
with open(file, encoding="utf8") as json_file:
    parsedJson = json.load(json_file)

assignmentsAllText = []
for assignment in parsedJson:
    assignmentAllText = ""
    assignmentAllText += " " + assignment["name"]
    assignmentAllText += " " + BeautifulSoup(assignment["description"], "lxml").get_text()
    if "rubric" in assignment:
        for criteria in assignment["rubric"]:
            assignmentAllText += " " + criteria["description"]
            if criteria["long_description"]:
                if criteria["long_description"][0] == "<":
                    description_KPI = BeautifulSoup(criteria["long_description"], "lxml").get_text()
                    assignmentAllText += " " + description_KPI
            for rating in criteria["ratings"]:
                long_description = rating["long_description"]
                assignmentAllText += " " + rating["long_description"]
        assignmentsAllText.append(assignmentAllText)
print(assignmentsAllText)



