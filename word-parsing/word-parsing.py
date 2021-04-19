# ===================================================
# DOCUMENT FROM DOCX
# ===================================================

from docx import Document

doc = Document(".\data\document-1.docx")
paragraphs = doc.paragraphs
print(paragraphs)

file = open("output-docx.txt", "w+")

for par in paragraphs:
    text = par.text
    if len(text) > 0:
        print(text)
        file.write(text + "\n")

file.close()



# ===================================================
# PYPANDOC
# ===================================================

import pypandoc

output = pypandoc.convert_file("./data/document-1.docx", "plain", outputfile="output-pypandoc.txt")
assert output == ""



# ===================================================
# GROUPDOCS API
# ===================================================

import groupdocs_conversion_cloud
from shutil import copyfile

client_id = "ENTER CLIENT ID HERE"
client_key = "ENTER CLIENT SECRET HERE"

convert_api = groupdocs_conversion_cloud.ConvertApi.from_keys(client_id, client_key)

try:
    request = groupdocs_conversion_cloud.ConvertDocumentDirectRequest("txt", "./data/document-1.docx")
    result = convert_api.convert_document_direct(request)
    copyfile(result, 'output-groupdocs.txt')

    request = groupdocs_conversion_cloud.ConvertDocumentDirectRequest("txt", "./data/document-1.pdf")
    result = convert_api.convert_document_direct(request)
    copyfile(result, 'output-groupdocs-pdf.txt')

except groupdocs_conversion_cloud.ApiException as e:
    print("Exception when calling get_supported_conversion_types: {0}".format(e.message))