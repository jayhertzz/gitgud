"""
-------------------------------
NO LONGER USING NLTK in this project as of: 10/17/2022
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


NLTK Example Code:

    SENTENCE TOKENIZE:
sentences = nltk.sent_tokenize(text)
for sent in sentences:
    print(sent, '\n')

EXAMPLE CODE
# words = nltk.word_tokenize()
# sentences = nltk.sent_tokenize()
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

# import nltk # disabled this because it was only being used in sentence tokenization
import PyPDF2
import os
from string import punctuation
import textract
from docx2pdf import convert  # for converting docx to pdf, for page counting
import re
# import Frontend as FE

"""
STATIC METHODS and OBJECTS
"""
# condition text: lower-case, remove punctuation, remove some misc. items
def preprocess_text_remove_punc(text):
    text = text.lower()  # Lowercase text
    text = re.sub(f"[{re.escape(punctuation)}]", "", text)  # Remove punctuation
    text = " ".join(text.split())  # Remove extra spaces, tabs, and new lines (retains parenthesis)
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
        self.andQuery = ands.split(' ')
        self.orQuery  = ors.split(' ')
        self.notQuery = nots.split(' ')
        self.radius   = [rad1, rad2, rad3]

    def Confidence(self):
        confidence = 0
        #if contains all keywords
        confidence += 70
        #confidence += (number of matched ors / total ors) * 30
        #confidence -= (number of matched nots) * 25
        return confidence


# handles storage of each keyword match instance
def count_paragraphs(docx_file):
    return len(docx_file.paragraphs)


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
    # sentences = nltk.sent_tokenize(text)
    # return len(sentences)
    return -1


class AndSearch:
    iter_i = 0
    keywords = []
    and_matches = []
    page_count = -1

    def __init__(self, Search_obj):
        self.keywords = Search_obj.andQuery
        self.and_matches = []
        self.Search_obj = Search_obj
        self.iter_i = 0


    def perform_search(self, document):
        if document.paginated:
            self.perform_search_with_page(document)
        else:
            self.perform_search_nopage(document)


    def perform_search_nopage(self, document):
        for keyword in self.keywords:  # do the following subroutine for each keyword in the list 'keywords'
            keyword = keyword.lower()
            text_body = document.text.lower() # case-insensitive initial search:
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

                    """ perform or/not search """
                    temp_and_matches =      {'keyword'        : keyword,
                                             'char_ct'        : prev_char_find_index,
                                             'line_ct'        : cr_count,
                                             'word_ct'        : word_count,
                                             'sent_ct'        : sentence_count,
                                             'page_ct'        : self.page_count}
                    temp_OrNotSearch_obj = OrNotSearch(self.Search_obj, temp_and_matches)
                    temp_OrNotSearch_obj.perform_search(document)
                    temp_and_matches.update({'OrNotSearch_obj': temp_OrNotSearch_obj})

                    """ store results """
                    self.and_matches.append(temp_and_matches)

                    """ setup the next run """
                    text_body = text_body[char_find_index + 1:]  # truncate the text body to exclude this run's found keyword


    def perform_search_with_page(self, document):
        for i in range(len(document.paged_text)):  # do the following subroutine for each page
            page_num = i  # intuitive var name to hold page number for result storage

            for keyword in self.keywords:  # do the following subroutine for each keyword in the list 'keywords'
                text_body = document.paged_text[i].lower() # case insensitive initial search:
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
                        self.and_matches.append({'keyword': keyword,
                                                 'char_ct': prev_char_find_index,
                                                 'line_ct': cr_count,
                                                 'word_ct': word_count,
                                                 'sent_ct': sentence_count,
                                                 'page_ct': (page_num+1)})

                        """ setup the next run """
                        text_body = text_body[char_find_index + 1:]  # truncate the text body to exclude this run's found keyword

"""
This class is a subsidiary class of the AndSearch class.
    meaning one OrNotSearch class obj per dict entry within the AndSearch class obj)
"""
class OrNotSearch:
    or_keywords=[]
    not_keywords=[]
    or_rad=-1
    or_matches_words={}
    or_matches_count=-1
    not_rad=-1
    not_matches_words={}
    not_matches_count=-1
    text_slice_whole_or_subset = ''
    text_slice_whole_not_subset = ''
    text_slice_front = ''
    text_slice_back = ''
    text_slice_whole = ''
    text_slice_paged = []
    max_pad_factor=-1
    char_pad=-1
    idx_factor = 10
    temp_and_matches={}

    def __init__(self, Search_obj, temp_and_matches):
        self.or_keywords=Search_obj.orQuery
        self.not_keywords=Search_obj.notQuery
        self.or_rad=Search_obj.radius[1]
        self.not_rad=Search_obj.radius[2]
        self.or_matches_words={}
        self.or_matches_count = -1
        self.not_matches_words={}
        self.not_matches_count = -1
        self.text_slice_front = ''
        self.text_slice_back = ''
        self.text_slice_whole = ''
        self.text_slice_whole_or_subset = ''
        self.text_slice_whole_not_subset = ''
        self.text_slice_paged = []
        self.max_pad_factor = max(self.or_rad, self.not_rad)+2
        self.char_pad = self.max_pad_factor * self.idx_factor
        self.temp_and_matches=temp_and_matches

    def perform_search(self, document):
        if document.paginated:
            # TODO: not yet implemented:
            pass
            # self.perform_search_with_page(document)
        else:
            self.perform_search_nopage(document)

    def find_subset_word_slice(self, words_front, words_back, max_pad_factor):
        word_front = words_front[-max_pad_factor]
        word_back = words_back[max_pad_factor]
        text_slice_front = self.text_slice_front[self.text_slice_front.find(word_front):]
        back_idx = len(self.text_slice_back) - (self.text_slice_back[::-1].find(word_back[::-1]))
        text_slice_back = self.text_slice_back[:back_idx]
        self.text_slice_whole_subset = text_slice_front + text_slice_back

    def perform_search_nopage(self, document):
        # for and_match in document.file_results.AndSrch_obj.and_matches:
        front_flag = False
        back_flag = False
        and_idx = self.temp_and_matches['char_ct']
        custom_punctuation = r"""!"#$%&'*+,-./:;<=>\^`|~"""

        self.text_slice_front = document.text[(and_idx-self.char_pad):and_idx]
        if len(self.text_slice_front) < self.char_pad:
            front_flag = True
        text_slice_front_repl=self.text_slice_front
        for x in list(custom_punctuation):
            text_slice_front_repl = text_slice_front_repl.replace(x,' ')
        text_slice_front_repl = text_slice_front_repl.replace('  ', ' ')

        preprocessed_text = " ".join(text_slice_front_repl.split())  # Remove extra spaces, tabs, and new lines (retains parenthesis)
        words_front = preprocessed_text.split(' ')

        self.text_slice_back = document.text[and_idx:(and_idx+self.char_pad)]
        if len(self.text_slice_back) < len(document.text)-self.char_pad:
            back_flag = True
        text_slice_back_repl=self.text_slice_back
        for x in list(custom_punctuation):
            text_slice_back_repl = text_slice_back_repl.replace(x,' ')
        text_slice_back_repl = text_slice_back_repl.replace('  ', ' ')

        preprocessed_text = " ".join(text_slice_back_repl.split())  # Remove extra spaces, tabs, and new lines (retains parenthesis)
        words_back = preprocessed_text.split(' ')

        if ((len(words_front) < self.max_pad_factor) and not front_flag) or (
            (len(words_back) < self.max_pad_factor) and not back_flag):
            self.max_pad_factor += (self.max_pad_factor-len(words_front))+10
            self.char_pad = self.max_pad_factor * self.idx_factor
            self.perform_search_nopage(document)

        elif not front_flag:
            word_front = words_front[-self.max_pad_factor+2]
            j=1
            # if word_front is nothing but special chars, find the word immediately preceding it and check again
            #       for a valid word
            while len(re.findall(f"[^A-Za-z0-9]", word_front)) > 0:
                word_front = words_front[-self.max_pad_factor + 2 - j]
                j+=1
            # the standalone str.find method from nltk word tokenizing the original string is ineffective.
            #       It ends up pulling partial finds. However, this compliment regex pattern fills the gap
            regex_return = re.findall(f"[^A-Za-z0-9]{word_front}[^A-Za-z0-9]", self.text_slice_front)[0]
            self.text_slice_front = self.text_slice_front[self.text_slice_front.find(regex_return):].strip()

        elif front_flag:
            self.text_slice_front = self.text_slice_front.strip()

        elif not back_flag:
            word_back = words_back[self.max_pad_factor-2]
            j=1
            while len(re.findall(f"[^A-Za-z0-9]", word_back)) > 0:
                word_back = words_back[-self.max_pad_factor + 2 - j]
                j+=1
            regex_return = re.findall(f"[^A-Za-z0-9]{word_back}[^A-Za-z0-9]", self.text_slice_back)[0]
            back_idx = len(self.text_slice_back)-(self.text_slice_back[::-1].find(regex_return[::-1]))
            self.text_slice_back = self.text_slice_back[:back_idx].strip()

        elif back_flag:
            self.text_slice_back = self.text_slice_back.strip()

        else:
            print('front_flag, back_flag nonsense')

        self.text_slice_whole = (self.text_slice_front+' '+self.text_slice_back).strip()

        self.or_matches_count = 0
        self.not_matches_count = 0
        if self.or_rad > self.not_rad:
            for or_kw in self.or_keywords:
                or_match_ct = len(self.text_slice_whole.split(or_kw))-1
                self.or_matches_count += or_match_ct
                self.or_matches_words.update({or_kw:or_match_ct})
            for not_kw in self.not_keywords:
                not_match_ct = len(self.text_slice_whole_not_subset.split(not_kw))-1
                self.not_matches_count += not_match_ct
                self.not_matches_words.update({not_kw:not_match_ct})

        elif self.or_rad < self.not_rad:
            for not_kw in self.not_keywords:
                not_match_ct = len(self.text_slice_whole.split(not_kw))-1
                self.not_matches_count += not_match_ct
                self.not_matches_words.update({not_kw:not_match_ct})
            for or_kw in self.or_keywords:
                or_match_ct = len(self.text_slice_whole_or_subset.split(or_kw)) - 1
                self.or_matches_count += or_match_ct
                self.or_matches_words.update({or_kw: or_match_ct})

        else:
            for not_kw in self.not_keywords:
                not_match_ct = len(self.text_slice_whole.split(not_kw))-1
                self.not_matches_count += not_match_ct
                self.not_matches_words.update({not_kw:not_match_ct})
            for or_kw in self.or_keywords:
                or_match_ct = len(self.text_slice_whole.split(or_kw)) - 1
                self.or_matches_count += or_match_ct
                self.or_matches_words.update({or_kw: or_match_ct})

    def perform_search_with_page(self, document):
        pass


#handle storage for overall file results (Zayn Severance)
class FileResult:
    filename        = ""
    score           = -1
    filetype        = ""
    total_AndMatches= -1
    total_OrMatches = -1

    # modified 'type' to 'file_type' due to overshadow of python built-in kw 'type'
    def __init__(self, document, Search_obj, score = -1):
        self.filename           = document.fname
        self.filetype           = document.extn
        self.score              = score
        self.document           = document
        self.Search_obj         = Search_obj
        self.AndSrch_obj        = AndSearch(Search_obj)
        self.total_AndMatches   = -1
        self.total_OrMatches    = -1
        # self.OrNotSearch_obj  = OrNotSearch(search_params)

    def perform_AndSearch(self):
        self.AndSrch_obj.perform_search(self.document)

    # def perform_OrNotSearch(self):
    #     self.AndSrch_obj.OrNotSearch_obj.perform_search(self.document)

    def print_results(self):
        if len(self.AndSrch_obj.and_matches) > 0:
            print('And match count: ',  len(self.AndSrch_obj.and_matches))
            i = 0
            for and_match in self.AndSrch_obj.and_matches:
                print('\nAnd match #: ',      i)
                print('Or match count: ',   and_match['OrNotSearch_obj'].or_matches_count)
                print('Or match text: ',    and_match['OrNotSearch_obj'].text_slice_whole)
                print('Not match count: ',  and_match['OrNotSearch_obj'].not_matches_count)
                print('Not match text: ',   and_match['OrNotSearch_obj'].text_slice_whole)
                i+=1
        else:
            print('no matches found')


class Document:
    fpath = r''
    fname = ''
    extn = ''
    original_extn = ''
    paginated = False
    paged_text = []
    text = ''

    def __init__(self, Search_obj, fpath=r''):
        self.fpath = fpath
        self.fname = (self.fpath.split('\\')[-1])
        self.extn = self.fname.split('.')[-1]
        self.original_extn = self.extn #created to keep track of converted docx files
        #pdf files and epub files text should always be paginated
        if self.extn=='pdf' or self.extn=='epub':
            self.paginated=True
        else:
            self.paginated=False
        self.file_results = FileResult(self, Search_obj)
        self.paged_text = []
        self.text = ''

    def check_file(self):
        return not(self.fname[0]=='~' or self.fname[0]=='$' or self.extn=='txt' or not(self.extn=='docx'))

    def __process_epub_for_pages__(self):
        self.paged_text=self.text.split('GITGUD_PAGE_NUM_')

    # creates a pdf file from a docx file. uses docx2pdf
    def __convert_docx_to_pdf__(self, source_file_path):
        return convert(source_file_path)

    # uses textract to extract text
    def __extract_text__(self):
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

    def perform_search(self):
        self.file_results.perform_AndSearch()
        # self.file_results.perform_OrNotSearch()

    def print_results(self):
        print(self.fname)
        self.file_results.print_results()


"""
TODO SECTION
I made this section to capture some of the other things we need to take care of in back-end

THIS SECTION IS OUTDATED AS OF 10/17/2022
"""
# TODO: integrate epub file-type handling (COMPLETE)
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