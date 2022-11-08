"""
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
from docx2pdf import convert  # for converting docx to pdf, to support page counting
import re
import pandas as pd
import Document as Doc
import _Utils


class SearchEngine:
    """
    MEMBER ATTRIBUTES

    """
    # list of file types this app aims to support:
    compatible_types = ['html', 'txt', 'doc', 'docx', 'pdf', 'epub', 'pptx', 'rtf']
    first_run = True

    # keyword search parameters
    search_parameters = {}

    # file tree details
    dir_path        = r''
    file_dict       = {}
    df_column_names = ['fpath',      'fname',      'AND_keyword',  'doc_AND_score',   'page_number',
                       'text_short', 'text_long',  'search_score', 'Document_object', 'AND_char_idx']

    #results DataFrame
    results_df = pd.DataFrame()

    """
    MEMBER FUNCTIONS

    """
    def __init__(self, search_parameters):
        self.search_parameters  = _Utils.process_user_inputs(search_parameters)
        self.dir_path           = search_parameters['dir_path']
        self.results_df         = pd.DataFrame(columns=self.df_column_names)
        self.first_run          = True
        self.file_dict          = {}


    def _walk_directory_(self, refresh=False):
        """
        Pulls ALL matching files from a given directory and its subdirectories
            initializes or updates the self.file_dict object depending on refresh flag

        :param refresh:
        :return:
        """
        for root, dirs, files in os.walk(self.dir_path, topdown=False):
            for name in files:
                if (name.find('.') > -1) & (name.split('.')[-1] in self.compatible_types):
                    fpath = os.path.join(root, name)
                    if refresh and (not self.first_run) and (not (self.file_dict.get(fpath) is None)):
                        # if a key already exists and needs comparing:
                        # TODO: check self.file_dict for differences, change list iff required
                        pass
                    else:
                        # create a new record for file found at fpath
                        tmp_docObj = Doc.Document(fpath)
                        self.file_dict.update(
                                                {fpath:
                                                   {
                                                        self.df_column_names[0] : fpath,     # 'fpath'
                                                        self.df_column_names[1] : name,      # 'fname'
                                                        self.df_column_names[8] : tmp_docObj # 'Document_object'
                                                   }
                                                }
                                             )


    def get_filename_list(self):
        return list(self.results_df.fname)

    # for refreshing the directory file dictionary
    def refresh_file_list(self):
        self._walk_directory_(refresh=True)


    def search_next(self):
        """
        def search_next(self):
        This function returns a single row of results with which to update the results_dataframe

        keeps track of which search is next
            conduct an 'AND' search on all Documents in the list first
                check for docs which have already been searched
            conduct 'OR' and 'NOT' searches based on highest scoring Documents (based on # of 'AND' matches)

        """
        EOS_flag = False

        # SearchEngine class object first run behavior:
        #       walk the directory to collect all file information
        #       setup the df for filling with results information
        if len(self.file_dict) == 0 and self.first_run:
            self.initialize_df()
            EOS_flag = False
            """
              (returns nothing, but saves results to a fresh self.results_df with the following items filled in:
              
                                df column name   | filled data
                            {
                                    self.df_column_names[0]: res['fpath'],          # 'fpath'
                                    self.df_column_names[1]: res['fname'],          # 'fname'
                                    self.df_column_names[2]: res['AND_keyword'],    # 'AND_keyword'
                                    self.df_column_names[3]: doc_AND_score,         # 'doc_AND_score'
                                    self.df_column_names[4]: res['page_number'],    # 'page_number'
                                    self.df_column_names[8]: doc_obj,               # 'Document_object'
                                    self.df_column_names[9]: res['AND_char_idx'],   # 'AND_char_idx'
                            }
            
            This provides everything needed to progress in the search_next() method:
                1. fills in the results_df with initial AND data, 
                2. calculates and sorts by doc_AND_score, finally
                3. allows search_next() to perform its follow-on series of or/not_searches()
                4. The only remaining item for completing results_df is 'search_score'
            
            """

        elif len(self.file_dict) == 0:
            # TODO: print a warning dialog box to the user when this condition is met
            # print('No compatible documents found in this directory.')
            EOS_flag = True

        else:
            # TODO:
            #   1. perform or not search on a single self.results_df row,
            #       1a. check for end-of-df (or/not_index == len(df) )
            #   2. calculate score for that row based on or and not matches
            #   3. update that row in self.results_df
            #   4. re-sort the df based on the search score,
            #   5. return the self.results_df to the front-end with 'text_short', 'text_long', & 'search score' filled in

            #check for loop completion (no more non-matched df rows available)
            filtered_df = self.results_df[self.results_df.search_score.isnull()]
            # do NOT loop through the results_df, just filter them and choose the top row
            if len(filtered_df) > 0:
                """
                    df_column_names = ['fpath',      'fname',      'AND_keyword',  'doc_AND_score',   'page_number',
                                       'text_short', 'text_long',  'search_score', 'Document_object', 'AND_char_idx']
                """
                top_row = filtered_df.iloc[0]
                index = top_row.name
                doc_obj = top_row.Document_object
                page_num = top_row.page_number-1

                if page_num < 0:
                    score = 0
                else:
                    score = doc_obj.get_nextOrNot(
                        page_num,
                        top_row.AND_char_idx,
                        self.search_parameters,
                    )

                self.results_df['search_score'][index] = score
                self.results_df.sort_values('search_score', inplace=True, ascending=False)

                EOS_flag = False
            else:
                EOS_flag = True

        print('EOS_Flag: '.format(str(EOS_flag)))
        return self.results_df, EOS_flag


    def initialize_df(self):
        self.refresh_file_list()
        self.conduct_initial_andSearch()


    def save_AND_results_to_df(self, result, ANDS_list, doc_obj):

        doc_AND_score = len(result)
        # print('Saving results for file: {}'.format(doc_obj.fname))

        if not result:
            for AND_kw in ANDS_list:
                self.results_df = \
                    pd.concat(
                        [self.results_df, pd.DataFrame
                            (
                                {
                                    self.df_column_names[0]: doc_obj.fpath, # 'fpath'
                                    self.df_column_names[1]: doc_obj.fname, # 'fname'
                                    self.df_column_names[2]: AND_kw,        # 'AND_keyword'
                                    self.df_column_names[3]: doc_AND_score, # 'doc_AND_score'
                                    self.df_column_names[4]: -1,            # 'page_number'
                                    self.df_column_names[5]: '',            # 'text_short'
                                    self.df_column_names[6]: '',            # 'text_long'
                                    # self.df_column_names[7]: -1,            # 'search_score'
                                    self.df_column_names[8]: doc_obj,       # 'Document_object'
                                    self.df_column_names[9]: -1,            # 'AND_char_idx'
                                }, index=[0]
                            )
                        ],
                    ignore_index=True)

        else:
            for res in result:
                self.results_df = \
                    pd.concat(
                        [self.results_df, pd.DataFrame
                            (
                                {
                                    self.df_column_names[0]: res['fpath'],          # 'fpath'
                                    self.df_column_names[1]: res['fname'],          # 'fname'
                                    self.df_column_names[2]: res['AND_keyword'],    # 'AND_keyword'
                                    self.df_column_names[3]: doc_AND_score,         # 'doc_AND_score'
                                    self.df_column_names[4]: res['page_number'],    # 'page_number'
                                    self.df_column_names[5]: res['text_short'],     # 'text_short'
                                    self.df_column_names[6]: '',                    # 'text_long'
                                    # self.df_column_names[7]: -1,                    # 'search_score'
                                    self.df_column_names[8]: doc_obj,               # 'Document_object'
                                    self.df_column_names[9]: res['AND_char_idx'],   # 'AND_char_idx'
                                }, index=[0]
                            )
                        ],
                    ignore_index=True)

        # print('Results saved for file: {}'.format(doc_obj.fname))
    # END initialize_df() METHOD

    def conduct_initial_andSearch(self):
        """
        input: self.file_dict, defined at __init__ as:

                self.file_dict.update(
                                {fpath:
                                   {
                                        self.df_column_names[0] : fpath,     # 'fpath'
                                        self.df_column_names[1] : name,      # 'fname'
                                        self.df_column_names[8] : tmp_docObj # 'Document_object'
                                   }
                                }
                             )

        :return:
        The purpose of this method is to conduct and update the results_df with each document's AND matches
            and related information to each AND match

                    return from Document class 'get_nextAnd' method:
                        result.append(
                            {
                                'fpath'             : self.fpath,
                                'fname'             : self.fname,
                                'AND_keyword'       : AND_kw,
                                'page_number'       : page_num,
                                'AND_char_idx'      : char_find_index
                            }
                        )

        """

        for key in self.file_dict:
            tmp_dict = self.file_dict[key]
            # Check file first
            if _Utils.check_file(tmp_dict['Document_object'].fname, tmp_dict['Document_object'].extn) \
                    or tmp_dict['Document_object'].completed_AND_srch:
                # reject these files
                tmp_dict['Document_object'].completed_AND_srch = True
                continue

            # Find all AND matches in a given file:
            result = tmp_dict['Document_object'].get_nextAnd(self.search_parameters['ANDS'],
                                                        self.search_parameters['case_sens'])

            self.save_AND_results_to_df(result, self.search_parameters['ANDS'], tmp_dict['Document_object'])

            # back to 'for key in self.file_dict:' loop
            tmp_dict['Document_object'].completed_AND_srch = True

        self.results_df.sort_values(['doc_AND_score', 'page_number', 'AND_char_idx'],
                                    ascending=[False,True,True], inplace=True)

        # debug:
        # print(self.results_df.to_string())

    """
    pandas DataFrame updating example code:
    
    
    
    result is a list of dictionary objects
        each dictionary contains:
        
                            'fpath'             : self.fpath,
                            'fname'             : self.fname,
                            'AND_keyword'       : AND_kw,
                            'page_number'       : page_num,
                            'Document_object'   : doc_obj,
                            'AND_char_idx'      : char_find_index
                            
        we simply add up all of the dictionary's entries to calculate the total doc score


    1. Call df.fpath.unique() to get a list of all documents,
    2. Then, add up the number of rows which match each fpath, in succession (looped).
    3. Assign each of the return rows that number of rows value; this value is the doc_AND_score

    perform this function using the following style of dataframe call (df.loc[])
        e.g.:
    ---------------

        # 1. initialize an example df:

    import pandas as pd
    df = pd.DataFrame(columns=['file', 'data'])
    df.loc[:,'file'] = list('aabbccddefg')

        # 2. where the column 'file' is equal to the value 'a', retrieve all associated rows.
        # 3. assign those rows the value = 10

    df.loc[df.file == 'a','data'] = 10

        # 4. output:

    > >>df
       file data
    0     a   10
    1     a   10
    2     b  NaN
    3     b  NaN
    4     c  NaN
    5     c  NaN
    6     d  NaN
    7     d  NaN
    8     e  NaN
    9     f  NaN
    10    g  NaN

    df.loc[df.file == 'a','data'] = 10
    df.loc[df.file == 'b','data'] = 11
    df.loc[df.file == 'c','data'] = 14
    df.loc[df.file == 'd','data'] = 1
    df.loc[df.file == 'e','data'] = 6

    df.sort_values('data', inplace=True)
    """









