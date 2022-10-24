# -*- coding: utf-8 -*-
"""
    common functions 
    @author : Karina DAMENE 
    Reviewer : Loic Morel & Patrick MONTEUX
"""


def request_file_path(file_paths):
    for idx, file_path in enumerate(file_paths):
        print(f"{idx}\t{file_path}")
    while True:
        try:
            file_path_idx = int(input(f"Pick a number between 0 and {len(file_paths)-1} : "))
            # raise exception if the user enter a negative number
            if file_path_idx < 0:
                raise ValueError
            file_path = file_paths.pop(file_path_idx)
            print(f"The file chosen is : {file_path}")
        # raise exception if the index is out of range (not in list)
        # or if the user did not enter a number (e.g.: a string or a character)
        except (IndexError, ValueError):
            print("invalid file index")
        # if no exception, then leave the while loop with the correct mpt file path
        else:
            break
    # prep1/rep2/rep3 ..../repx.bak ==> return repx not repx.bak !!! 
    return file_path.parts[-1].split('.')[0]

#bak_file_paths = sorted(Path().rglob("*.bak"))
#bak_file_path= request_file_path(bak_file_paths)
#print(bak_file_path) # PLCData_Lake_20221012.bak
# print(type(bak_file_path)) #pathlib 
# print(bak_file_path.parts[0].split('.')) # ['PLCData_Lake_20221012', 'bak']
# print(type(bak_file_path.parts[0].split('.')))  # list 
# print(bak_file_path.parts[0].split('.')[0]) # PLCData_Lake_20221012