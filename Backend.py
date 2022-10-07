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

*****************************************

docx manipulation
https://automatetheboringstuff.com/chapter13/
https://python-docx.readthedocs.io/en/latest/


"""

import nltk
import PyPDF2
import os
from string import punctuation
import textract
from docx2pdf import convert  # for converting docx to pdf, for page counting
import re

#search result class (Zayn Severance)
class Search:
    andQuery = []
    orQuery  = []
    notQuery = []
    radius   = [None, None, None]

    def __init__(self, ands, ors, nots, rad1, rad2, rad3):
        self.andQuery = ands.split()
        self.orQuery  = ors.split()
        self.notQuery = nots.split()
        self.radius   = [rad1, rad2, rad3]

    def Confidence(self, fileIn):
        confidence = 0
        #if contains all keywords
        confidence += 70
        #confidence += (number of matched ors / total ors) * 30
        #confidence -= (number of matched nots) * 25
        return confidence

#handle storage for results (Zayn Severance)
class result:
    filename = ""
    scoring  = 0
    filetype = ""
    def __init__(self, file, type, score):
        #this would basically be scored off
        self.filename = file
        self.filetype = type
        self.scoring  = score




# condition text: lower-case, remove punctuation, remove some misc. items



def preprocess_text_remove_punc(text):
    text = text.lower()  # Lowercase text
    text = re.sub(f"[{re.escape(punctuation)}]", "", text)  # Remove punctuation
    text = " ".join(text.split())  # Remove extra spaces, tabs, and new lines (retains parenthesis)
    return text


# conditions text: lower-case, remove some misc. items
def preprocess_text_keep_punc(text):
    text = text.lower()  # Lowercase text
    # text = re.sub(f"[{re.escape(punctuation)}]", "", text)  # Remove punctuation
    # text = " ".join(text.split())  # Remove extra spaces, tabs, and new lines (retains parenthesis)
    return text


# uses textract to extract text
def extract_text(filepath, extn):
    text = textract.process(filename=filepath, text=textract.process(filepath, extension=extn))
    return text


# pulls ALL matching files from a given directory and its subdirectories
def walk_directory(root_path):
    file_name_list = []
    for root, dirs, files in os.walk(root_path, topdown=False):
        for name in files:
            if (name.find('.') > -1) & (name.split('.')[-1] in compatible_types):
                file_name_list.append(os.path.join(root, name))
    return file_name_list


# searches the walk_directory output for files of a particular file-type extension, returns a list of those files
def find_file_ext(file_name_list, extn):
    extn_list = []
    for name in file_name_list:
        if (name.find('.') > -1) & (name.split('.')[-1] == extn):
            extn_list.append(name)
    return extn_list


# counts carriage returns/line feeds/combos (crLF)
def count_CRs(in_text):
    # count the various styles of LineFeeds and Carriage Returns
    cr_count = int(in_text.count('\n'))
    crLF_count = int(in_text.count('\r\n'))
    LF_count = int(in_text.count('\r'))
    # if any CRLF combos are found, reduce the cr and LF individual counts by the same amount
    # removes redundant counting
    if crLF_count > 0:
        cr_count -= crLF_count
        LF_count -= crLF_count
    # sum and send out
    return cr_count + crLF_count + LF_count


def count_words(in_text):
    proc_text = preprocess_text_remove_punc(in_text)
    return len(proc_text.split(' '))


def count_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return len(sentences)


# creates a pdf file from a docx file. uses docx2pdf
def convert_docx_to_pdf(docx_file_path):
    return convert(docx_file_path)


def perform_search_nopage(text, keywords):
    file_keyword_search_results = []
    for keyword in keywords:  # do the following subroutine for each keyword in the list 'keywords'
        keyword = keyword.lower()
        text_body = preprocess_text_keep_punc(text)
        keyword_count = text_body.count(keyword)
        prev_CR_count = 0  # initialize the carriage return counter var
        prev_word_count = 0  # initialize the word count var
        prev_sentence_count = 0  # initialize the word count var
        prev_char_find_index = 0

        for j in range(keyword_count):
            char_find_index = text_body.find(keyword)  # search a subset of the original text body
            prev_char_find_index = char_find_index + prev_char_find_index
            if char_find_index > -1:  # only make a record if a match is found (char_find_index == -1 means no match)
                """ count CRs """
                trunc_text = text_body[:char_find_index]
                # count the number of carriage returns to keep track of line num.
                cr_count = count_CRs(trunc_text) + prev_CR_count
                prev_CR_count = cr_count  # keep track of previous CR counts to optimize next run CR counting operation

                """ count words """
                word_count = prev_word_count + count_words(trunc_text)
                prev_word_count = word_count

                """ count sentences """
                sentence_count = prev_sentence_count + count_sentences(trunc_text)
                prev_sentence_count = sentence_count

                """ store results """
                result = ({'keyword': keyword, 'char_index': prev_char_find_index,
                           'line_count': cr_count, 'word_count': word_count, 'sentence_count': sentence_count})
                print(result)
                file_keyword_search_results.append(result)

                """ setup the next run """
                text_body = text_body[char_find_index + 1:]  # truncate the text body to exclude this run's found keyword
    return file_keyword_search_results


def perform_search_with_page(page_text, keywords):
    file_keyword_search_results = []
    for i in range(len(page_text)):  # do the following subroutine for each page
        page_num = i  # intuitive var name to hold page number for result storage

        for keyword in keywords:  # do the following subroutine for each keyword in the list 'keywords'
            text_body = preprocess_text_keep_punc(page_text[i])
            keyword = keyword.lower()
            page_keyword_count = text_body.count(keyword)
            prev_CR_count = 0  # initialize the carriage return counter var
            prev_word_count = 0  # initialize the word count var
            prev_sentence_count = 0  # initialize the word count var
            prev_char_find_index = 0

            for j in range(page_keyword_count):
                char_find_index = text_body.find(keyword)  # search a subset of the original text body
                prev_char_find_index = char_find_index + prev_char_find_index
                if char_find_index > -1:  # only make a record if a match is found (char_find_index == -1 means no match)
                    """ count CRs """
                    trunc = text_body[:char_find_index]
                    # count the number of carriage returns to keep track of line num.
                    cr_count = count_CRs(trunc) + prev_CR_count
                    prev_CR_count = cr_count  # keep track of previous CR counts to optimize next run CR counting operation

                    """ count words """
                    word_count = prev_word_count + count_words(trunc)
                    prev_word_count = word_count

                    """ count sentences """
                    sentence_count = prev_sentence_count + count_sentences(trunc)
                    prev_sentence_count = sentence_count

                    """ store results """
                    result = ({'keyword': keyword, 'page_num': page_num+1, 'char_index': prev_char_find_index,
                               'line_count': cr_count, 'word_count': word_count, 'sentence_count': sentence_count})
                    print(result)
                    file_keyword_search_results.append(result)

                    """ setup the next run """
                    text_body = text_body[char_find_index + 1:]  # truncate the text body to exclude this run's found keyword
    return file_keyword_search_results


def count_paragraphs(docx_file):
    return len(docx_file.paragraphs)


def get_text(file_path, file_extn, page_req_flag=False):
    if page_req_flag:
        # switch matrix for file extension handling
        if file_extn == 'pdf':
            pdfFileObj = open(pdf_list[1], 'rb')  # create a file handler for reading in a pdf file object
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  # Call/initialize the PyPDF2 library
            num_pages = len(pdfReader.pages)  # read # of pages from the pdf doc
            page_text = []
            for page in range(int(num_pages)):  # use int to make sure it's a whole number value
                page_text.append(
                    pdfReader.getPage(page).extractText())  # append each page's text to a new index in page_text list
            return page_text

        elif file_extn == 'docx':
            convert_docx_to_pdf(file_path)
            new_file_path = file_path.replace('.docx', '.pdf')
            return get_text(new_file_path, 'pdf', True)

        elif file_extn == 'epub':
            epub_text = process_epub_for_pages(get_text(file_path, file_extn))
            return epub_text

    else:
        # TODO: build a section here to decode the text based on input file format e.g. .decode('UTF-8')
        return (extract_text(file_path, file_extn)).decode('UTF-8')


def process_epub_for_pages(epub_text):
    return epub_text.split('GITGUD_PAGE_NUM_')


"""
USER INPUTS
&
TEST FLAGS
"""
# enable your debugging sections using these flags
doc_flag = docx_flag = pdf_flag = epub_flag = txt_flag = \
    pptx_flag = rtf_flag = html_flag = docx_conv_flag = False

pdf_flag = True
# # doc_flag = True
# docx_flag = True
# epub_flag = True

nopage_results_str = '(keyword, char_find_index, cr_count, word_count, sentence_count)'
paged_results_str = '(keyword, page_num, char_find_index, cr_count, word_count, sentence_count)'

# user inputs for word(s) matching + context words
keywords = ['var']  # small set used for testing. guaranteed hits
context_keywords = ['the']  # small set used for testing. guaranteed hits
min_sentence_filter = 0  # user input for filtering results containing context words
max_sentence_filter = 5  # same as above
min_word_filter = 0  # same as above
max_word_filter = 10  # same as above
backward_word_count = 10  # how many words to capture for quick-result displays in results UI
forward_word_count = 10  # same as above



"""
END TEST FLAGS
"""

# change this file path (fpath) to your test document repo directory. Be sure to retain the 'r' in front
test_fpath = r'D:\applications\PyCharm Projects\gitgud_01\test_documents_01'

# initialize variable to hold text for testing
page_text = ''

# list of document file types we can parse:
compatible_types = ['html', 'txt', 'doc', 'docx', 'pdf', 'epub', 'pptx', 'rtf']

# find all files in a directory:
file_list = walk_directory(test_fpath)
paged_results = []
nopage_results = []

"""
RTF TESTING SECTION
"""

test_extn_rtf = 'rtf'
rtf_list = find_file_ext(file_list, test_extn_rtf)
if rtf_list and rtf_flag:  # check for empty lists first
    rtf_file_path = rtf_list[0]
    # test_text_rtf = str(extract_text(rtf_list[0], test_extn_rtf))
    # print(test_text_rtf)
    # test_text = test_text_rtf
    rtf_text = get_text(rtf_file_path, test_extn_rtf)
    rtf_nopage_results = perform_search_nopage(rtf_text, keywords)

"""
.TXT TESTING SECTION
"""

test_extn_txt = 'txt'
txt_list = find_file_ext(file_list, test_extn_txt)
if txt_list and txt_flag:  # check for empty lists first
    txt_file_path = txt_list[0]
    # test_text_txt = str(extract_text(txt_list[0], test_extn_txt))
    # print(test_text_txt)
    # test_text = test_text_txt
    txt_text = get_text(txt_file_path, test_extn_txt)
    txt_nopage_results = perform_search_nopage(txt_text, keywords)

"""
PDF TESTING SECTION
"""

test_extn_pdf = 'pdf'
pdf_list = find_file_ext(file_list, test_extn_pdf)
if pdf_list and pdf_flag:  # check for empty lists first
    pdf_paged_text = get_text(pdf_list[1], test_extn_pdf, True)
    pdf_paged_results = perform_search_with_page(pdf_paged_text, keywords)

    pdf_nopage_text = get_text(pdf_list[1], test_extn_pdf)
    pdf_nopage_results = perform_search_nopage(pdf_nopage_text, keywords)

    paged_results = pdf_paged_results
    nopage_results = pdf_nopage_results

"""
DOCX TESTING SECTION
"""
pdf_creation_list = []  # keep track of created pdfs for destruction later
test_extn_docx = 'docx'
docx_list = find_file_ext(file_list, test_extn_docx)
if docx_list and docx_flag:  # check for empty lists first
    docx_file_path = docx_list[1]
    # test_text_docx = preprocess_text((extract_text(docx_test_file, test_extn_docx)).decode('UTF-8'))

    """python-docx code"""
    # test_docx = docx.Document(docx_list[1])
    # print('The number of paragraphs in this document is: {}'.format(count_paragraphs(test_docx)))

    pdf_creation_list.append(docx_file_path)
    docx_paged_text = get_text(docx_file_path, test_extn_docx, True)  # this will create a pdf of the docx file first
    docx_paged_results = perform_search_with_page(docx_paged_text, keywords)
    """end python-docx code"""

    """textract code"""
    # test_text_docx = ((extract_text(docx_file_path, test_extn_docx)).decode('UTF-8'))
    # print(test_text_docx)
    # test_text = test_text_docx
    docx_nopage_text = get_text(docx_file_path, test_extn_docx)
    docx_nopage_results = perform_search_nopage(docx_nopage_text, keywords)

    """end textract code"""

"""
HTML TESTING SECTION
"""

test_extn_html = 'html'
html_list = find_file_ext(file_list, test_extn_html)
if html_list and html_flag:  # check for empty lists first
    html_file = html_list[0]
    html_text = get_text(html_file, test_extn_html)

"""
PPTX TESTING SECTION
"""

test_extn_pptx = 'pptx'
pptx_list = find_file_ext(file_list, test_extn_pptx)
if pptx_list and pptx_flag:  # check for empty lists first
    pptx_file = pptx_list[0]
    pptx_nopage_text = get_text(pptx_file, test_extn_pptx)

"""
EPUB TESTING SECTION
"""

test_extn_epub = 'epub'
epub_list = find_file_ext(file_list, test_extn_epub)
if epub_list and epub_flag:  # check for empty lists first
    epub_file = epub_list[0]

    """ebooklib code - expensive operation to extract page numbers- only execute if keyword match found and page 
    requested in results"""
    epub_paged_text = get_text(epub_file, test_extn_epub, True)
    epub_paged_results = perform_search_with_page(epub_paged_text, keywords)
    """end ebooklib code"""

    """textract code - quick run to search for keyword matches, less info"""
    epub_nopage_text = (get_text(epub_file, test_extn_epub)).decode('UTF-8')
    epub_nopage_results = perform_search_nopage(epub_nopage_text, keywords)
    """end textract code"""
    paged_results = epub_paged_results
    nopage_results = epub_nopage_results

"""
MISC DEBUG SECTION
"""

# print('\n\n\n*******PAGED RESULTS*******\n{}\n\n'.format(paged_results_str))
# # empty
# if paged_results:
#     for result in paged_results:
#         print(str(result) + '\n')
#
# print('\n\n\n*******NO PAGE RESULTS*******\n{}\n\n'.format(nopage_results_str))
# if nopage_results:
#     for result in nopage_results:
#         print(str(result) + '\n')

"""
FIND THE LOCATIONS OF KEYWORDS IN A GIVEN BODY OF TEXT
"""

# see each document section



"""
TODO SECTION
I made this section to capture some of the other things we need to take care of in back-end
"""
# TODO: integrate epub file-type handling
#           working on it (zayn & matt)
# TODO: handle boolean search parameters (constrained to: and/or/not)
# TODO: indexing results (hash table?) & caching result - store previous search results for faster future searches
#   including category assignments
# TODO: Document category assignment algorithm (ML?)
# TODO: for doc and docx, only convert documents with found keywords to pdf
#   keep track of which documents are converted to delete them later (but save pdf page results results)
# TODO: figure out how to open a document/ then, open it to a specific page
# TODO: implement context word searching
# TODO: implement scoring / include score in results storage tuple
# TODO: continue testing other file types with textract/other libraries
# TODO: include the filepath in the results storage tuple
# TODO: exception handling when a document read fails (skip the file/print an error to the user?)
# TODO: multithreading/parallel processing
# TODO: multi-thread/parallel process the document search as a background process while we focus the
#   main program on the available results
# TODO: open documents at a specific area in results
# TODO:
# TODO: use our current textraction method, which is very fast, to find the subset of docx files containing the requested text
#   if its a large number, we can choose to just convert the highest scoring results to pdf and check page numbers
#   and dont display page numbers for any other docx results unless its asked for, then the program can run and perform the search
#   we would probably want the search results to display consistently too.. so none of the result would initially have page numbers.
#   only upon expansion maybe.. like a '+' button the user has to hit on each result

"""end TODO section"""

"""test text body"""
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