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

We only need the text-based ones.
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

"""
STATIC METHODS and OBJECTS
"""
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

# searches the walk_directory output for files of a particular file-type extension,
# returns a list of the files ending in the passed 'extn' string
#       e.g. find_file_ext(example_file_list, 'docx') returns all files
#       ending in 'docx'
def find_file_ext(file_name_list, extn):
    extn_list = []
    for name in file_name_list:
        if (name.find('.') > -1) & (name.split('.')[-1] == extn):
            extn_list.append(name)
    return extn_list


# pulls ALL matching files from a given directory and its subdirectories
def walk_directory(root_path):
    file_name_list = []
    for root, dirs, files in os.walk(root_path, topdown=False):
        for name in files:
            if (name.find('.') > -1) & (name.split('.')[-1] in compatible_types):
                file_name_list.append(os.path.join(root, name))
    return file_name_list

# list of document file types we can parse:
compatible_types = ['html', 'txt', 'doc', 'docx', 'pdf', 'epub', 'pptx', 'rtf']

"""
END STATIC METHODS
"""


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


# handles storage of each keyword match instance
class AndSearch:
    keyword = ""
    char_index = -1
    line_count = -1
    word_count = -1
    sentence_count = -1
    page_count = -1

    #page_ct is optional since some results will not contain this value
    def __init__(self, kw, char_idx=-1, line_ct=-1, word_ct=-1, sent_ct=-1, page_ct=-1):
        self.keyword = kw
        self.char_index = char_idx
        self.line_count = line_ct
        self.word_count = word_ct
        self.sentence_count = sent_ct
        self.page_count = page_ct

    # counts carriage returns/line feeds/combos (crLF)
    def count_CRs(self, in_text):
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

    def count_words(self, in_text):
        proc_text = preprocess_text_remove_punc(in_text)
        return len(proc_text.split(' '))

    def count_sentences(self, text):
        sentences = nltk.sent_tokenize(text)
        return len(sentences)

    # def perform_initial_search(self, doc):


    def perform_search_nopage(self, text, in_keywords):
        file_keyword_search_results = []
        for keyword in in_keywords:  # do the following subroutine for each keyword in the list 'keywords'
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
                    cr_count = self.count_CRs(trunc_text) + prev_CR_count
                    prev_CR_count = cr_count  # keep track of previous CR counts to optimize next run CR counting operation

                    """ count words """
                    word_count = prev_word_count + self.count_words(trunc_text)
                    prev_word_count = word_count

                    """ count sentences """
                    sentence_count = prev_sentence_count + self.count_sentences(trunc_text)
                    prev_sentence_count = sentence_count

                    """ store results """
                    result = AndSearch(keyword, prev_char_find_index,
                               cr_count,  word_count, sentence_count)
                    print(result)
                    file_keyword_search_results.append(result)

                    """ setup the next run """
                    text_body = text_body[char_find_index + 1:]  # truncate the text body to exclude this run's found keyword
        return file_keyword_search_results


    def perform_search_with_page(self, page_text, keywords):
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
                        cr_count = self.count_CRs(trunc) + prev_CR_count
                        prev_CR_count = cr_count  # keep track of previous CR counts to optimize next run CR counting operation

                        """ count words """
                        word_count = prev_word_count + self.count_words(trunc)
                        prev_word_count = word_count

                        """ count sentences """
                        sentence_count = prev_sentence_count + self.count_sentences(trunc)
                        prev_sentence_count = sentence_count

                        """ store results """
                        result = ({'keyword': keyword, 'page_num': page_num+1, 'char_index': prev_char_find_index,
                                   'line_count': cr_count, 'word_count': word_count, 'sentence_count': sentence_count})
                        print(result)
                        file_keyword_search_results.append(result)

                        """ setup the next run """
                        text_body = text_body[char_find_index + 1:]  # truncate the text body to exclude this run's found keyword
        return file_keyword_search_results


    def count_paragraphs(self, docx_file):
        return len(docx_file.paragraphs)

#handle storage for overall file results (Zayn Severance)
class FileResult:
    filename = ""
    scoring  = 0
    filetype = ""
    matches  = []
    def __init__(self, file_name, file_type, score): #modified 'type' to 'file_type' due to overshadow of python built-in kw 'type'
        #this would basically be scored off
        self.filename = file_name
        self.filetype = file_type
        self.scoring  = score

    def add_match(self, result):
        self.matches.append(result)


class Document:
    paginated = False
    file_results = FileResult
    text = ''
    fpath = r''
    fname = ''
    extn = ''
    paged_text = []
    original_extn = ''

    def __init__(self, fpath=r''):
        self.fpath = fpath
        self.fname = (self.fpath.split('\\')[-1])
        self.extn = self.fname.split('.')[-1]
        self.original_extn = self.extn #created to keep track of converted docx files
        #pdf files and epub files text should always be paginated
        if self.extn=='pdf' or self.extn=='epub':
            self.paginated=True

    def check_file(self):
        return not(self.fname[0]=='~' or self.fname[0]=='$' or self.extn=='txt')

    def __process_epub_for_pages__(self):
        self.paged_text=self.text.split('GITGUD_PAGE_NUM_')

    # creates a pdf file from a docx file. uses docx2pdf
    def __convert_docx_to_pdf__(self, source_file_path):
        return convert(source_file_path)

    # uses textract to extract text
    def __extract_text__(self):
        # text = textract.process(filename=self.fpath, text=textract.process(self.fpath, extension=self.extn))
        text = textract.process(filename=self.fpath, extension=self.extn)
        try:
            if self.extn != 'txt':
                text=text.decode('UTF-8')
        except():
            text = 'file_not_found'
            print('decode exception')
        finally:
            self.text = text

    def convert_docx_params(self):
        self.fname = (self.fpath.split('\\')[-1])
        self.fpath = self.fpath.replace('.docx', '.pdf')
        self.extn = self.fname.split('.')[-1]

    def process_doc_for_text(self, page_req_flag=False):
        if page_req_flag or self.paginated:
            if self.extn == 'pdf':
                pdfFileObj = open(self.fpath, 'rb')  # create a file handler for reading in a pdf file object
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  # Call/initialize the PyPDF2 library
                num_pages = len(pdfReader.pages)  # read # of pages from the pdf doc
                page_text = []
                for page in range(int(num_pages)):  # use int to make sure it's a whole number value
                    page_text.append(
                        pdfReader.getPage(page).extractText())  # append each page's text to a new index in page_text list
                self.paged_text = page_text

            elif self.extn == 'docx':
                self.paginated=True
                self.__convert_docx_to_pdf__(self.fpath)
                self.convert_docx_params()
                self.process_doc_for_text(page_req_flag=True)

            elif self.extn == 'epub':
                self.__extract_text__()
                self.__process_epub_for_pages__()

        else:
            self.__extract_text__()





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