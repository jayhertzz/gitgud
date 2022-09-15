"""
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
"""

import nltk
import os
# import pdfquery
import PyPDF2

fpath = r'D:\books\Sapiens_ A Brief History of Humankind - Yuval Noah Harari'
fpath_1 = r'D:\books'

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

# text = 'sentence 1 content here. sentence 2 content here. sentence 3 begin content here etc. sentence 3 end. ' \
#        'sentence 5 content here. sentence 6 content here. sentence 7 content here. '
# sentences = text.split('. ')
# print(sentences)
compatible_types = ['pdf']  # , 'txt', '', '', '', '', '']
pdf_files = []
for root, dirs, files in os.walk(fpath_1, topdown=False):
    for name in files:
        if (name.find('.') > -1) & (name.split('.')[-1] in compatible_types):
            pdf_files.append(os.path.join(root, name))
    # for name in dirs:
    #     print(os.path.join(root, name))

# test_pdf_file = pdfquery.PDFQuery(pdf_files[-1])
# test_pdf_file.load()
# VERY SLOW
keyword = "Charms"

pdfFileObj = open(pdf_files[-1], 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
num_pages = len(pdfReader.pages)
page_text = []
for page in range(int(num_pages/2)):
    page_text.append(pdfReader.getPage(page).extractText())
    # print(pageObj.extractText())
# much faster

sentences = (page_text[130])



# sentences = nltk.sent_tokenize(text)
# for sent in sentences:
#     print(sent, '\n')
#
# combine_idx_list = []
j=0
for i in range(len(sentences)):
    words = nltk.word_tokenize(sentences[i])
    # if words[-2] == 'etc':  # ended too early due to a dot at the end of 'etc.'; tokenizer failure
    #     combine_idx_list.append(i)
    for word in words:
        if (word in keyword):
            print("found another, total: {}".format(j))
            j+=1
#
# idx = 1
# new_sentences = sentences.copy()
# for idx in combine_idx_list:
#     new_sentences[idx] += str(' ' + str(sentences[idx + 1]))
#     del new_sentences[idx + 1]

