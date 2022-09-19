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


EXAMPLE CODE
# words = nltk.word_tokenize()
# sentences = nltk.sent_tokenize()
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
import PyPDF2
import os
import re
from string import punctuation
import textract  # for doc and docx file formats


def preprocess_text(text):
    text = text.lower()  # Lowercase text
    # text = re.sub(f"[{re.escape(punctuation)}]", "", text)  # Remove punctuation
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


"""
TEST FLAGS
"""
# compatible_types = ['doc', 'docx', 'pdf', 'epub', 'html', 'pptx', 'rtf', 'txt']
doc_flag = docx_flag = pdf_flag = epub_flag = html_flag = pptx_flag = rtf_flag = txt_flag = False
pdf_flag = True

"""
END TEST FLAGS
"""


fpath_1 = r'D:\applications\PyCharm Projects\gitgud_01\test_documents_01'
page_text = ''  # initialize variable to hold text for testing
text_files = []

file_list = walk_directory(fpath_1)

"""
RTF TESTING SECTION
"""

test_extn_rtf = 'rtf'
rtf_list = find_file_ext(file_list, test_extn_rtf)
if rtf_list and rtf_flag:  # check for empty lists first
    test_text_rtf = preprocess_text(str(extract_text(rtf_list[0], test_extn_rtf)))
    print(test_text_rtf)
    test_text = test_text_rtf

"""
PDF TESTING SECTION
"""

test_extn_pdf = 'pdf'
pdf_list = find_file_ext(file_list, test_extn_pdf)
if pdf_list and pdf_flag:  # check for empty lists first
    """
    FIRST TEST HERE IS WITH TEXTRACT LIBRARY
    """
    # test_text_pdf = ((extract_text(pdf_list[1], test_extn_pdf)).decode('UTF-8'))
    # # test_text_pdf = preprocess_text((extract_text(pdf_list[1], test_extn_pdf)).decode('UTF-8'))
    # print(test_text_pdf)
    # test_text = test_text_pdf

    """
    SECOND TEST HERE IS WITH PYPDF2 LIBRARY
    """
    pdfFileObj = open(pdf_list[1], 'rb')  # create a file handler for reading in a pdf file object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  # Call/initialize the PyPDF2 library
    num_pages = len(pdfReader.pages)  # read # of pages from the pdf doc
    page_text = []

    for page in range(int(num_pages)):  # use int to make sure it's a whole number value
        page_text.append(
            pdfReader.getPage(page).extractText())  # append each page's text to a new index in page_text list

"""
DOC/DOCX TESTING SECTION
"""
docx_test_file_name = r'Sample_Prospectus_2.docx'
docx_test_file_path = r'D:\applications\PyCharm Projects\gitgud_01\test_documents\docx'
docx_test_file = os.path.join(docx_test_file_path, docx_test_file_name)

test_extn_docx = 'docx'
docx_list = find_file_ext(file_list, test_extn_docx)
if docx_list and docx_flag:  # check for empty lists first
    # test_text_docx = preprocess_text((extract_text(docx_test_file, test_extn_docx)).decode('UTF-8'))
    test_text_docx = ((extract_text(docx_test_file, test_extn_docx)).decode('UTF-8'))
    print(test_text_docx)
    test_text = test_text_docx

"""
HTML TESTING SECTION
"""

test_extn_html = 'html'
html_list = find_file_ext(file_list, test_extn_html)
if html_list and html_flag:  # check for empty lists first
    test_text_html = ((extract_text(html_list[102], test_extn_html)).decode('UTF-8'))
    print(test_text_html)
    test_text = test_text_html

"""
MISC DEBUG SECTION
"""





"""
FIND THE LOCATIONS OF KEYWORDS IN A GIVEN BODY OF TEXT
keyword matches on the sanitized data set will not yield much in the way of location data.
    It will yield page #, but not word #, due to false-positive word parsing of punctuation and other factors.
    
We will eventually need to feed back some parameters of the search result into 
"""
keywords = ['adopt']

# TODO: Make this search algorithm into a callable definition/method. Possibly a recursive implementation
results = []
for i in range(len(page_text)):
    page_num = i  # intuitive var name to hold page number for result storage

    for keyword in keywords:
        page_keyword_count = page_text[i].lower().count(keyword.lower())
        prev_CR_count = 0
        text_body = page_text[i].lower()

        for ja in range(page_keyword_count):
            new_index = text_body.find(keyword.lower())  # search a subset of the original text body
            if new_index > -1:  # only make a record if a match is found (new_index == -1 means no match)
                """ count CRs """
                trunc = text_body[:new_index]
                # count the number of carriage returns to keep track of line num.
                # TODO: capture \r and \r\n also
                cr_count = prev_CR_count + trunc.count('\n')

                """ store results """
                # TODO: capture results- need to include word, sentence counts as well
                result = (keyword, page_num, new_index, cr_count)
                results.append(result)

                """ setup the next run """
                prev_CR_count = cr_count  # keep track of previous CR counts to optimize next run CR counting operation
                text_body = text_body[new_index+1:]  # truncate the text body to exclude this run's found keyword






















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
