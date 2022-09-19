"""
-------------------------------
nltk install procedure:

see: https://www.nltk.org/install.html
first, upgrade your pip installer as necessary:
       python.exe -m pip install --upgrade pip
then, install nltk using pip
       pip install --user -U nltk
now, Numpy
       pip install --user -U numpy
finally, run this cmd in your python console
       nltk.download('punkt')
-------------------------------

pip install PyPDF2

-------------------------------


-------------------------------
NLTK Example Code:

1 -------------------------------
    SENTENCE TOKENIZE:
sentences = nltk.sent_tokenize(text)
for sent in sentences:
    print(sent, '\n')
-------------------------------






old archived code:

1 -------------------------------
import pdfquery

test_pdf_file = pdfquery.PDFQuery(pdf_files[-1])
test_pdf_file.load()
VERY SLOW
-------------------------------
import PyPDF2

EXAMPLE CODE

pdfFileObj = open(pdf_files[-1], 'rb')  # create a file handler for reading in a pdf file object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  # Call/initialize the PyPDF2 library
num_pages = len(pdfReader.pages)  # read # of pages from the pdf doc
page_text = []

for page in range(int(num_pages / 5)):  # use int to make sure it's a whole number value
    page_text.append(pdfReader.getPage(page).extractText())  # append each page's text to a new index in page_text list
# much faster than pdfquery

-------------------------------


textract documentation
https://textract.readthedocs.io/en/stable/python_package.html

handles the following file types:
.csv via python builtins
.doc via antiword
.docx via python-docx2txt
.eml via python builtins
.epub via ebooklib
.gif via tesseract-ocr
.jpg and .jpeg via tesseract-ocr
.json via python builtins
.html and .htm via beautifulsoup4
.mp3 via sox, SpeechRecognition, and pocketsphinx
.msg via msg-extractor
.odt via python builtins
.ogg via sox, SpeechRecognition, and pocketsphinx
.pdf via pdftotext (default) or pdfminer.six
.png via tesseract-ocr
.pptx via python-pptx
.ps via ps2text
.rtf via unrtf
.tiff and .tif via tesseract-ocr
.txt via python builtins
.wav via SpeechRecognition and pocketsphinx
.xlsx via xlrd
.xls via xlrd

We obviously only need the text-based ones.
It is interesting to see it can handle audio/speech recognition and image-text recognition
    May be a stretch goal here
"""

import nltk
import os
import re
from string import punctuation
import textract  # for doc and docx file formats


def preprocess_text(text):
    text = text.lower()  # Lowercase text
    text = re.sub(f"[{re.escape(punctuation)}]", "", text)  # Remove punctuation
    text = " ".join(text.split())  # Remove extra spaces, tabs, and new lines (retains parenthesis)
    return text


def extract_text(filepath, extn):
    text = textract.process(filename=filepath, text=textract.process(filepath, extension=extn))
    return text


def walk_directory(root_path):
    compatible_types = ['doc', 'docx', 'pdf', 'epub', 'html', 'pptx', 'rtf', 'txt']
    file_name_list = []
    for root, dirs, files in os.walk(root_path, topdown=False):
        for name in files:
            if (name.find('.') > -1) & (name.split('.')[-1] in compatible_types):
                file_name_list.append(os.path.join(root, name))
    return file_name_list


def find_file_ext(file_name_list, extn):
    extn_list = []
    for name in file_name_list:
        if (name.find('.') > -1) & (name.split('.')[-1] == extn):
            extn_list.append(name)
    return extn_list


fpath_pdf = r'D:\books\Sapiens_ A Brief History of Humankind - Yuval Noah Harari.pdf'
fpath_docx = r'C:\Users\Scragg Family\OneDrive - Florida State University\Fall 2022\CEN4090L\Prospectus Submission\Proj_Prospectus_II_v03.docx'
fpath_1 = r'D:\books'

text_files = []
keyword = "charm"

test_extn = 'pdf'
file_list = walk_directory(fpath_1)
pdf_list = find_file_ext(file_list, test_extn)
test_text = preprocess_text(str(extract_text(pdf_list[0], test_extn)))
print(test_text)

"""
FIND THE LOCATIONS OF KEYWORDS IN A GIVEN BODY OF TEXT
keyword matches on the sanitized data set will not yield much in the way of location data.
    It will yield page #, but not word #, due to false-positive word parsing of punctuation and other factors.
    
We will eventually need to feed back some parameters of the search result into 
"""
# j = 0
# for i in range(len(sentences)):
#     # sentences_punc = re.sub(f"[{re.escape(punctuation)}]", "", sentences)  # Remove punctuation
#     # words = nltk.word_tokenize(sentences[i])
#     words = nltk.word_tokenize(sentences)
#     words_split = sentences.split(' ')
#     for word in words:
#         if word in keyword:
#             # need to save the word and page index here of both the keyword and context matches
#             print("found another, total: {}".format(j))
#             j += 1
#


# text = 'Due to the lack of an enhanced search functionality available for standalone text sources, ' \
#        'our team (gitgud) proposes a multi-format compatible search engine designed to enhance user ' \
#        'search precision. This search engine will take PDF, DOCX, TXT, RTF, HTML, etc. files contained ' \
#        'within a directory and present the user with several prompts to narrow down their search. ' \
#        'The primary prompt will accept main target keywords tied to Boolean operators. Then, a ' \
#        'secondary gitgud-unique section, called the “Context” section, will request additional supplemental ' \
#        'keywords and/or categories from the user with the goal to provide additional context to the primary ' \
#        'search parameters. This is achieved by filtering and scoring results based on proximity, relevance, ' \
#        'and other factors. Proximity will be measured via grammatical structures like words, sentences, ' \
#        'paragraphs, and/or pages while relevance seeks to connect meaning between selected “categories” ' \
#        'and primary keywords. Importantly, search results will be displayed to the user in an intuitive ' \
#        'interface which plainly expresses the score of each result. Selectable options will be available ' \
#        'within each result which allow the user to see “more like this”, view context category ' \
#        'recommendations for improving precision further, view in-depth graphical analysis of the ' \
#        'search process, and save user search progress to a file.'
