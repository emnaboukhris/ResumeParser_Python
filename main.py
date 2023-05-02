from PyPDF2 import PdfReader
import spacy
import json
import re
from pyresparser import ResumeParser
import pandas as pd
import base64
import random
import time
import datetime
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io
import random
from streamlit_tags import st_tags
from PIL import Image


section_headings = ["Education", "Work Experience",
                    "Skills", "Certifications", "Projects", "Personal Projects", "Languages", "Personal Qualities", "Profile"]
nlp = spacy.load('en_core_web_sm')


def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ',
                        resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText


def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(
        resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text


save_image_path = 'new.pdf'

with open('new.pdf', "rb") as f:
    # f.write(pdf_file.getbuffer())
    # show_pdf(save_image_path)
    resume_data = ResumeParser(save_image_path).get_extracted_data()

    if resume_data:
        # Get the whole resume data
        resume_text = pdf_reader(save_image_path)
        cleanedText = cleanResume(resume_text)
        # print(cleanedText)


# Open the PDF file in binary mode
with open('new.pdf', 'rb') as pdf_file:
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

# Clean the extracted text
# text = cleanResume(text)
# print(text)

# Split the text into a list of sentences
doc = nlp(text)
data = ResumeParser(doc.text).get_extracted_data()
# print(data)

sentences = [sent.text.strip() for sent in doc.sents]

# Find the section headings and their positions in the sentence list
section_positions = {}
for heading in section_headings:
    for i, sent in enumerate(sentences):
        if heading in sent:
            section_positions[heading] = i
            break

# Initialize the section dictionary
sections = {heading: [] for heading in section_headings}

# Extract the content of each section
current_section = None
for i, sent in enumerate(sentences):
    # Find the closest section heading above the current sentence
    closest_heading = None
    closest_distance = float('inf')
    for heading, pos in section_positions.items():
        distance = i - pos
        if 0 <= distance < closest_distance:
            closest_heading = heading
            closest_distance = distance

    if closest_heading is not None:
        current_section = closest_heading

    if current_section is not None:
        sections[current_section].append(sent)

# Print the extracted sections as a JSON object
print(json.dumps(sections, indent=4))
