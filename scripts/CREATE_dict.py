import re
import pandas as pd
"""
    This script creates from SQL statements, from CREATE.txt, a python NESTED(!) dictionary.
    It can only read out CREATE TABLE statements for this project
    and might bug out on other valid CREATE TABLE statements.
    
    returned dict structure:
        {"Tablename" : {
            "FOREIGN KEY": [field_name, ref_table_name],
            "PRIMARY KEY": "field_name",
            field_name : [data_type, NOT NULL? ja/nein ]
            } }
    
    it might print to console "ERROR", if something went wrong for each occurance.
"""

def create_dict_from_statement_txt():
    # read file
    with open('CREATE.txt') as fp:
        contents = fp.read()

    # some cleaning and splitting each statement
    contents= contents.strip("; \n")
    tabelstatments = contents.split(";")
    
    tabelstatments_dict = {}
    # some more magic with cleaning, phrasing and writing dict
    for test in tabelstatments:
        test = test.replace("\n", " ").replace("\t", " ").strip()
        test = test[0:-1]
        test = test.split(",")
        test[0], dummy = test[0].split("(", maxsplit=1)
        test.insert(1,dummy)
        table_name = ""
        for j in test:         
            i = j.strip()
            if i.startswith("CREATE"):
                table_name = i[i.find('"')+1:-1]
                tabelstatments_dict[table_name] = {"FOREIGN KEY" : {}, "PRIMARY KEY": ""}
            elif i.startswith("FOREIGN"):
                index_list = [m.start() for m in re.finditer('"', i)]
                tabelstatments_dict[table_name]["FOREIGN KEY"].update({i[index_list[0]+1:index_list[1]] :
                                                                        i[index_list[2]+1:index_list[3]]})
            elif i.startswith("PRIMARY"):
                index_list = [m.start() for m in re.finditer('"', i)]
                tabelstatments_dict[table_name]["PRIMARY KEY"] = i[index_list[0]+1:index_list[1]]
            else:
                if i.endswith("NOT NULL"):
                    dummy = i.split(" ")
                    tabelstatments_dict[table_name][dummy[0].strip('"')] = [dummy[1], "Ja"]
                else:
                    if len(i.split(" ")) == 2:
                        dummy = i.split(" ")
                        tabelstatments_dict[table_name][dummy[0].strip('"')] = [dummy[1], "Nein"]
                    else:
                        print("ERROR ", i)
    return tabelstatments_dict