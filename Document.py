import copy

import pdfplumber
import textract
import PyPDF2
import _Utils

class Document:
    # instantiate blanks
    fpath = r''
    fname = ''
    extn = ''
    paginated = False
    paged_text = []
    text = ''
    first_run = True
    completed_AND_srch = False

    # constant declaration
    paginated_extn = ['pdf', 'epub', 'docx']

    # init
    def __init__(self, fpath=r''):
        self.paged_text         = []
        self.text               = ''
        self.first_run          = True
        self.completed_AND_srch     = False

        self.fpath = fpath
        self.fname = (self.fpath.split('\\')[-1])

        if self.extn in self.paginated_extn:
            self.paginated=True
        else:
            self.paginated=False

        # trap for files with no extension (shouldn't have got past the check_file() call)
        fname_spl = self.fname.split('.')
        if len(fname_spl) > 1:
            self.extn = fname_spl[-1]


    def convert_docx_params(self):
        self.fpath = self.fpath.replace('.docx', '.pdf')
        self.fname = (self.fpath.split('\\')[-1])
        self.extn = self.fname.split('.')[-1]


    def process_doc_for_text(self):
        # if self.extn == 'pdf':
        #     self.paginated = True
        #     pdfFileObj = open(self.fpath, 'rb')  # create a file handler for reading in a pdf file object
        #     pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  # Call/initialize the PyPDF2 library
        #     num_pages = len(pdfReader.pages)  # read # of pages from the pdf doc
        #     page_text = []
        #     for page in range(int(num_pages)):  # use int to make sure it's a whole number value
        #         page_text.append(
        #             pdfReader.pages[page].extract_text())  # append each page's text to a new index in page_text list
        #     # print('completed extracting pages from: {}'.format(self.fname))
        #     self.paged_text = page_text

        if self.extn == 'pdf':
            self.paginated = True
            with pdfplumber.open(self.fpath) as pdf:  # create a file handler for reading in a pdf file object
                page_text = []
                for page in pdf.pages:  # use int to make sure it's a whole number value
                    page_text.append(page.extract_text())  # append each page's text to a new index in page_text list

                pdf.close()
                self.paged_text = page_text

        # elif self.extn == 'docx':
        #     self.paginated = True
        #     _Utils.convert_docx_to_pdf(self.fpath)
        #     self.convert_docx_params()
        #     self.process_doc_for_text()

        elif self.extn == 'epub':
            self.paginated = True
            self.text = _Utils.extract_text(self.fpath, self.extn)
            _Utils.process_epub_for_pages(self.text)

        elif self.extn == 'pptx':
            # TODO: build in support for ripping slide numbers off powerpoints (pptx)
            pass

        else:
            # DOES NOT RETURN PAGED TEXT
            self.paginated = False
            self.text = _Utils.extract_text(self.fpath, self.extn)


    def get_nextAnd(self, AND_kws, case_sens):
        """
        def get_nextAND(self)

        This is the single call SearchEngine calls to progress the 'AND' search
        :return:
        result =
        (
        'AND_keyword',
        'page_number',
        'AND_char_idx'
        )
        """
        result = []

        # triple check for first_run indicators
        if self.first_run and self.paged_text == [] and self.text == '':
            self.first_run = False
            #get text
            self.process_doc_for_text()

        # after initial run, perform normal execution:
        if not case_sens:
            if self.paginated:
                text = copy.deepcopy(self.paged_text)
                for i in range(len(text)):
                    text[i] = text[i].lower()
            else:
                text = list(copy.deepcopy(self.text).lower())

        else:
            if self.paginated:
                text = copy.deepcopy(self.paged_text)
            else:
                text = list(copy.deepcopy(self.text))

        # print('headed into AND for loop on: {}'.format(self.fname))

        for i in range(len(text)):  # do the following subroutine for each page
            page_num = i+1  # intuitive var name to hold page number for result storage

            for AND_kw in AND_kws:
                if not case_sens:
                    AND_kw = AND_kw.lower()

                page_keyword_count      = text[i].count(AND_kw)
                if (page_keyword_count == 0) or (len(text[i]) == 0):
                    continue

                prev_char_find_index    = 0

                for j in range(page_keyword_count):
                    char_find_index = text[i].find(AND_kw)  # search a subset of the original text body
                    prev_char_find_index = char_find_index + prev_char_find_index
                    if char_find_index > -1:  # only make a record if a match is found (char_find_index == -1 means no match)

                        """ store results """
                        result.append(
                            {
                                'fpath'             : self.fpath,
                                'fname'             : self.fname,
                                'AND_keyword'       : AND_kw,
                                'page_number'       : page_num,
                                'AND_char_idx'      : char_find_index
                            }
                        )

                        """ setup the next run """
                        # truncate the text body to exclude this run's found keyword
                        text[i] = text[i][char_find_index + 1:]

        return result # returns a list of dictionary objects containing the AND results


    def get_nextOrNot(self, and_page_num, and_idx, search_parameters):
        """
                search_params = {
                        'ANDS'          : ANDS,
                        'ORS'           : ORS,
                        'NOTS'          : NOTS,
                        'rad1'          : num1,
                        'rad2'          : num2,
                        'rad3'          : num3,
                        'OR_srch_type'  : OR_type,
                        'NOT_srch_type' : NOT_type,
                        'dir_path'      : dir_path,
                        'case_sens'     : case_sens
                        }

        :param and_page_num:
        :param and_idx:
        :param search_parameters:
        :return:
        """

        # search_score = 0
        # text_short = text_long = ''
        #    type_enum = ['byWORD', 'byPAGE', 'byDOC']


        text = _Utils.get_text_slice(self, and_page_num, and_idx, search_parameters, 'OR')
        or_matches = _Utils.find_matches(text, search_parameters['ORS'])

        text = _Utils.get_text_slice(self, and_page_num, and_idx, search_parameters, 'NOT')
        not_matches = _Utils.find_matches(text, search_parameters['NOTS'])

        search_score = _Utils.calculate_score(or_matches, not_matches)

        return search_score #, text_short, text_long
