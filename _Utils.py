"""
STATIC METHODS CONTAINER SCRIPT
"""
import copy
import re

import textract
from docx2pdf import convert  # for converting docx to pdf, for page counting


# creates a pdf file from a docx file. uses docx2pdf
def convert_docx_to_pdf(source_file_path):
    convert(source_file_path)

# uses textract to extract text
def extract_text(fpath, extn):
    # TODO: fix .txt implementation (decoding issue??)
    text = textract.process(filename=fpath, extension=extn)
    try:
        if extn != 'txt':
            text=text.decode('UTF-8')
    except():
        text = 'file_not_found'
        print('decode exception')
    finally:
        return text


def process_epub_for_pages(text):
    return text.split('GITGUD_PAGE_NUM_')


def check_file(fname, extn):
    return fname[0] == '~' or fname[0] == '$' or extn == 'txt'


def process_user_inputs(search_parameters):

    search_parameters['ANDS'] = search_parameters['ANDS'].split(' ')
    search_parameters['ORS'] = search_parameters['ORS'].split(' ')
    search_parameters['NOTS'] = search_parameters['NOTS'].split(' ')

    return search_parameters


def get_word_text_slice(document, page_num, and_idx, radius):
    front_of_doc_flag = False
    back_of_doc_flag = False
    custom_punctuation = r"""!"#$%&'*+,-./:;<=>\^`|~"""
    words_front = words_back = []
    text_slice_front = text_slice_back = ''
    char_multiplier = 10
    # page_num -= 1 # comes in indexed from 1 instead of 0

    if document.paginated:
        text = copy.deepcopy(document.paged_text[page_num])
    else:
        text = copy.deepcopy(document.text)

    # ================ FIND FRONT & BACK WORD ==================#

    progress_flag = False
    while not progress_flag:
        char_pad = (radius+2) * char_multiplier

        # 2a. ==== FIND FRONT WORD ====

        # Start with finding the front word using the estimation index value (char_pad)
        text_slice_front = text[max(0,(and_idx - char_pad)):and_idx]
        # if the length of the sliced string we end up with is less than char_pad, we know we ran into a text edge (front or back)
        if len(text_slice_front) < char_pad:
            # handle this exception for paginated files
            # first, declare the end of text input for non-paged files, or for paged files if you the AND is located in page 1 (0 index)
            if not document.paginated or page_num == 0:
                front_of_doc_flag = True
            else:
                page_tracker = 1
                char_counter = len(text_slice_front)
                if page_num > 0:
                    char_counter += len(document.paged_text[page_num - page_tracker])
                while (char_counter < char_pad) and not front_of_doc_flag:
                    page_tracker += 1
                    if (page_num - page_tracker) >= 0:
                        char_counter += len(document.paged_text[page_num - page_tracker])
                    else:
                        front_of_doc_flag = True

                text_slice_front = ' '.join(document.paged_text[page_tracker:(page_num+1)])

        # 'text_slice_front_repl' is a temporary variable copy of the front text slice
        #   we use text_slice_front_repl during parsing instead of self.__text_slice_front__ because we dont want to
        #   permanently modify self.__text_slice_front__
        text_slice_front_repl=text_slice_front

        # remove all punctuation characters from the copy of self.__text_slice_front__ captured in text_slice_front_repl
        for x in list(custom_punctuation):
            text_slice_front_repl = text_slice_front_repl.replace(x,' ')

        # some of the replacements from above will cause double space chars to occur. these next 2 lines removes them
        while text_slice_front_repl.find('  ') > -1:
            text_slice_front_repl = text_slice_front_repl.replace('  ', ' ')

        # more processing
        preprocessed_text = " ".join(text_slice_front_repl.split())  # Remove extra spaces, tabs, and new lines (retains parenthesis)

        # now, the text just looks like alphanumerics separated by spaces. So, if we split them with the space char token
        #   we end up with a list of all the words, with our 'And' word at the end
        words_front = preprocessed_text.split(' ')
        # we'll pick back up the words_front obj and our pursuit of the front word in a few lines..

        # 2b. ==== FIND BACK WORD ====

        # Start with finding the back word using the estimation index value (char_pad)
        text_slice_back = text[and_idx:(and_idx + char_pad)]
        # if the length of the sliced string we end up with is less than char_pad, we know we ran into a text edge (front or back)
        if len(text_slice_back) < char_pad:
            if not document.paginated or page_num == len(document.paged_text):
                back_of_doc_flag = True
            else:
                last_page = len(document.paged_text)-1
                page_tracker = 1
                char_counter = len(text_slice_back)
                if page_num < last_page:
                    char_counter += len(document.paged_text[page_num + page_tracker])
                while (char_counter < char_pad) and not back_of_doc_flag:
                    page_tracker += 1
                    if (page_num + page_tracker) <= last_page:
                        char_counter += len(document.paged_text[page_num + page_tracker])
                    else:
                        page_tracker -= 1
                        back_of_doc_flag = True

                text_slice_back = ' '.join(document.paged_text[page_num:(page_num + page_tracker + 1)])

        # 'text_slice_back_repl' is a temporary variable copy of the front text slice
        #   we use text_slice_back_repl during parsing instead of self.__text_slice_back__ because we dont want to
        #   permanently modify self.__text_slice_back__
        text_slice_back_repl = text_slice_back
        for x in list(custom_punctuation):
            text_slice_back_repl = text_slice_back_repl.replace(x, ' ')
        while text_slice_back_repl.find('  ') > -1:
            text_slice_back_repl = text_slice_back_repl.replace('  ', ' ')

        # more processing
        preprocessed_text = " ".join(
            text_slice_back_repl.split())  # Remove extra spaces, tabs, and new lines (retains parenthesis)

        # now, the text just looks like alphanumerics separated by spaces. So, if we split them with the space char token
        #   we end up with a list of all the words, with our 'And' word at the end
        words_back = preprocessed_text.split(' ')

        # ================ FAILSAFE CHECK ==================#

        # 2c. Fix insufficient estimations

        # sometimes its necessary to increase our char_pad estimation for a wider guess to capture all words required by user input
        #    punctuation and other non-alphanumerics do not count as words, but they do as chars. This is the most common
        #    reason for having to run this subroutine
        if ((len(words_front) < radius) and not front_of_doc_flag) or (
                (len(words_back) < radius) and not back_of_doc_flag):
            radius += (radius - len(words_front))
            progress_flag = False
        else:
            progress_flag = True
        # ============== END: FAILSAFE CHECK ================#
    # ============== END: FIND FRONT & BACK WORD ================#


    # ============== TIE TOGETHER FRONT & BACK TEXT ================#

    # 2d. Find the narrowed text_slice_front based on word_front

    # enter here if not at the front of a body of text:
    if not front_of_doc_flag:
        # work
        word_front = words_front[-radius + 2]
        # if word_front is nothing but special chars, find the word immediately preceding it and check again
        #       for a valid word
        j = 1
        while (len(re.findall(f"[^A-Za-z0-9]", word_front)) > 0) and len(words_front) - (-radius + 2 - j) >= 0:
            word_front = words_front[-radius + 2 - j]
            j += 1
        # the standalone str.find method from nltk word tokenizing the original string is ineffective.
        #       It ends up pulling partial finds. However, this compliment regex pattern fills the gap
        # TODO: line below is highly problematic
        if not text_slice_front.find(word_front) == 0:
            regex_match = re.findall(f"[^A-Za-z0-9]{word_front}[^A-Za-z0-9]", text_slice_front)
            if len(regex_match) > 0:
                regex_return = regex_match[0]
                front_idx = text_slice_front.find(regex_return)
            else:
                front_idx = 0
            text_slice_front = text_slice_front[front_idx:].strip()
        else:
            text_slice_front = text_slice_front.strip()

    elif front_of_doc_flag:
        text_slice_front = text_slice_front.strip()

    elif not back_of_doc_flag:
        word_back = words_back[radius - 2]
        j = 1
        while (len(re.findall(f"[^A-Za-z0-9]", word_back)) > 0) and (radius - 2 + j) <= len(words_back) :
            word_back = words_back[radius - 2 + j]
            j += 1

        if not text_slice_back.find(word_back) >= len(text_slice_back)-len(word_back):
            regex_match = re.findall(f"[^A-Za-z0-9]{word_back}[^A-Za-z0-9]", text_slice_back)[0]
            if len(regex_match) > 0:
                regex_return = regex_match[0]
                back_idx = len(text_slice_back) - (text_slice_back[::-1].find(regex_return[::-1]))
            else:
                back_idx = len(text_slice_back)-1
            text_slice_back = text_slice_back[:back_idx].strip()
        else:
            text_slice_back = text_slice_back.strip()

    elif back_of_doc_flag:
        text_slice_back = text_slice_back.strip()

    else:
        print('front_of_doc_flag, back_of_doc_flag nonsense')

    text_slice_whole = (text_slice_front + ' ' + text_slice_back).strip()

    # if len(text_slice_whole) < 30:
    #     text_short = text_slice_whole
    # else:
    #     text_short = text_slice_whole[
    #         max(0, len(text_slice_front)-15) : min(len(text_slice_whole), len(text_slice_front)+15)]

    return text_slice_whole#, text_short


def get_page_text_slice(document, and_page_num, radius):#, and_idx):
    # handle for paginated files:
    if document.paginated:
        front_page = and_page_num - radius
        if front_page < 0:
            front_page = 0

        back_page = and_page_num + radius
        last_page = len(document.paged_text) - 1
        if back_page > last_page:
            back_page = last_page

        text = copy.deepcopy(document.paged_text[front_page:back_page+1])

        # if len(text) < 30:
        #     text_short = text
        # else:
        #     text_short = document.paged_text[and_page_num] \
        #     [
        #         max(0, len(document.paged_text[and_page_num][:and_idx])-15)
        #         :
        #         min(len(document.paged_text[and_page_num]), len(document.paged_text[and_page_num][:and_idx])+15)
        #     ]


    # non-paginated files:
    else:
        text = copy.deepcopy(document.text)

        # if len(text) < 30:
        #     text_short = text
        # else:
        #     text_short = text[
        #         max(0, len(text[:and_idx])-15) : min(len(text), len(text[:and_idx])+15)]

    return copy.deepcopy(text)#, text_short


# def short_text_page(document, and_page_num, and_idx):
#     if document.paginated:
#         text_short = document.paged_text[and_page_num] \
#                  [
#                      max(0, len(document.paged_text[and_page_num][:and_idx]) - 15)
#                      :
#                      min(len(document.paged_text[and_page_num]), len(document.paged_text[and_page_num][:and_idx]) + 15)
#                  ]
#     else:
#         text_short = document.text[
#                      max(0, len(document.text[:and_idx]) - 15)
#                      :
#                      min(len(document.text), len(document.text[:and_idx]) + 15)]
#
#     return text_short


def get_text_slice(document, and_page_num, and_idx, search_parameters, type_srch):
    type_enum = ['byWORD', 'byPAGE', 'byDOC']
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
    """
    text = ''
    # text_short = ''
    orRad = copy.deepcopy(search_parameters['rad2'])
    notRad = copy.deepcopy(search_parameters['rad3'])


    if type_srch == 'OR':
        if search_parameters['OR_srch_type']    == type_enum[0]: # byWORD
            text = get_word_text_slice(document, and_page_num, and_idx, orRad)

        elif search_parameters['OR_srch_type']  == type_enum[1]: # byPAGE
            text = get_page_text_slice(document, and_page_num, orRad)#, and_idx)

        elif search_parameters['OR_srch_type']  == type_enum[2]: # byDOC
            if document.paginated:
                text = ' '.join(copy.deepcopy(document.paged_text))
            else:
                text = copy.deepcopy(document.text)
            # text_short = short_text_page(document, and_page_num, and_idx)

    else:
        if search_parameters['NOT_srch_type']   == type_enum[0]: # byWORD
            text = get_word_text_slice(document, and_page_num, and_idx, notRad)

        elif search_parameters['NOT_srch_type'] == type_enum[1]: # byPAGE
            text = get_page_text_slice(document, and_page_num, orRad)#, and_idx)

        elif search_parameters['NOT_srch_type'] == type_enum[2]: # byDOC
            if document.paginated:
                text = ' '.join(copy.deepcopy(document.paged_text))
            else:
                text = copy.deepcopy(document.text)
            # text_short = short_text_page(document, and_page_num, and_idx)

    return copy.deepcopy(text)#, text_short


def find_matches(text, kws):
    count = 0
    for kw in kws:
        for txt in text:
            count += len(txt.split(kw)) - 1

    return count


def calculate_score(or_matches, not_matches):
    score = (or_matches * 5) - (not_matches * 10)
    return score

