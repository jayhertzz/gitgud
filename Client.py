import Backend as BE
# import Frontend as FE


"""
USER INPUTS
&
TEST FLAGS
"""
# user inputs for word(s) matching + context words
and_keywords = 'variable'  # small set used for testing. guaranteed hits
or_keywords = 'scientific analysis engineer'
not_keywords = 'algebra math theory'
backward_word_count = 10  # how many words to capture for quick-result displays in results UI
forward_word_count = 10  # same as above but forward facing

and_or_not_counts = [10,10,10]
"""
END TEST FLAGS
"""

"""
Input processing
"""

# user inputs keywords and search params
search_params = BE.Search(ands=and_keywords,ors=or_keywords,nots=not_keywords,
                      rad1=and_or_not_counts[0], rad2=and_or_not_counts[1], rad3=and_or_not_counts[2])
# user inputs file path (fpath)
input_filepath = r'D:\applications\PyCharm Projects\gitgud_01\test_documents_01'

"""
File name collecting
------------
Directory walk to find all compatible files in chosen directory
"""
file_list = BE.walk_directory(input_filepath)
"""
AndSearch processing
------------
Find all matches to the 'and' searches first
"""
# file_path = file_list[134]
document_dict = {}
for file_path in file_list:
    #create document object
    temp_document = BE.Document(fpath=file_path, search_params=search_params)
    # debug the items inside the 'check_file()' subroutine
    if temp_document.check_file():
        document_dict.update({temp_document.fname: temp_document})
        #store document text in document object
        temp_document.process_doc_for_text()
        temp_document.perform_search()
        temp_document.print_results()

        #conduct AndSearch:
        # temp_AndSrch = BE.AndSearch(kw=search_01.andQuery)
        # temp_AndSrch.perform_initial_search()





