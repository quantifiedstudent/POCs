from docx import Document

doc = Document(".\data\document-1.docx")
paragraphs = doc.paragraphs
print(paragraphs)

for par in paragraphs:
    text = par.text
    if len(text) > 0:
        print(text)
