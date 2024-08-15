import re
import pandas as pd
import CREATE_dict as CD
"""
    This file is for dataquality.
    To ensure ERD (drawio), CREATE TABLE statements and Data Dictionary are consistent.

"""

def check_text_from_drawio_export():
    """extract text of .drawio with build-in text plugin and save into text.txt
    parses the text into a pd.Dataframe with 2 columns for [table_name : field_name] 

    Returns:
        pd.Dataframe : _description_
    """
    with open('text.txt') as f:
        contents = f.read()

    delete_strings = [" N ", " 1 ", " n "]
    for i in delete_strings:
        while i in contents:
            contents= contents.replace(i, " ")
    # remove the " N" at the end
    if contents[-2] == " ":
        contents = contents[0:-2]    

    list1 = [m.start() for m in re.finditer(" PK", contents)]
    list2 = [contents.rfind(" ", 0, m) for m in list1]
    list2[0] = 0
    parts = [contents[i:j] for i,j in zip(list2, list2[1:]+[None])]
    tabels = {}
    for i in parts:
        dummy = i.split(" PK ")
        tabels[dummy[0].strip()] = dummy[1].split(" ")
    df = pd.DataFrame(columns= ["Tabelle", "Feldname"])
    for i in tabels:
        for j in tabels[i]:
            df.loc[len(df)] = [i,j]
    return df

# was used to check for spellings to ensure exact matching names in drawio, CREATE TABLE statments and Data Dictionary
# df = check_text_from_drawio_export()

df2 = pd.read_excel("DataDictionary_Zoo_V4.xlsx")

# see doc-string in CREATE_dict
statments_dict = CD.create_dict_from_statement_txt()
# create DataFrame from CREATE TABLE statment file for Data Dictionary
df4 = pd.DataFrame(columns= ['Tabelle', 'Feldname', 'Datentyp', 'Pflichtfeld', 'Primärschlüssel',
                              'Fremdschlüssel', 'FS Tabelle', 'Beschreibung'])
for i in statments_dict.keys():
    for j in statments_dict[i].keys():
        if j in ["PRIMARY KEY", "FOREIGN KEY"]:
            pass
        elif j == statments_dict[i]["PRIMARY KEY"]:
            df4.loc[len(df4)] = [i, j, statments_dict[i][j][0], statments_dict[i][j][1],
                                  "Ja", "Nein", None, None]
        elif j in statments_dict[i]["FOREIGN KEY"].keys():
            df4.loc[len(df4)] = [i, j, statments_dict[i][j][0], statments_dict[i][j][1],
                                  "Nein", "Ja", statments_dict[i]["FOREIGN KEY"][j], None]
        else:
            df4.loc[len(df4)] = [i, j, statments_dict[i][j][0], statments_dict[i][j][1],
                                  "Nein", "Nein", None, None]

# print(df4.head(10))
# df4.to_excel("python_test_creat_to_data_dictionary.xlsx")
# print(len([m for m in df2['Feldname'].tolist() if m.startswith("FK_")]))

# This line might not be used anymore used to remove FK_ notation in ERD (drawio) or other df
df2["Feldname"] = df2.Feldname.apply(lambda x: x[3:] if x.startswith("FK_") else x)

# combine the CREATE TABLE values with just the description of the work-in-progress version for better data quality in the Data Dictionary
df3 = pd.merge(df4[['Tabelle', 'Feldname', 'Datentyp', 'Pflichtfeld', 'Primärschlüssel', 'Fremdschlüssel',
                     'FS Tabelle',]], df2[['Tabelle', 'Feldname', 'Beschreibung']], how="outer",
                       on= ["Tabelle", "Feldname"],sort=False, right_index=False)

# wirte excel file of the Data Dictionary
df3.to_excel("test3.xlsx", index=False)
