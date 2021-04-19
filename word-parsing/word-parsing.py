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
