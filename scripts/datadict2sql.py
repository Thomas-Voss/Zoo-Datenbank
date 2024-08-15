#!python
""" Generating DDL statements for SQLite from a data dictionary (csv file) """

import csv
import sqlite3


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file:          database file
    :return:                 Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn:             Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)


def do_table(name, columns, fk, conn, outfile):
    """ Creates DDL statments for table <name>, executes them using the
        existing connection <conn> and writes the statements to <outfile>
    :param name:             table name
    :param columns:          a list of lists containing the name, datatype,
                             datatype lenght (if neccessary) and the nullable
                             and unique characteristics
    :param fk:               boolean, whether recreate table with foreign key
                             Note: SQLite does not support ALTER TABLE ADD
                             CONSTRAINT, so use a workaround by creating the
                             table with a different name, drop the existing
                             one anr rename the new one
    :param conn:             Connection object
    :param outfile:          Filehandle to the logfile containing the executed
                             SQL statements
    :return:
    """
    oldname = name
    if fk:
        name += '__fk'

    ddl = "CREATE TABLE IF NOT EXISTS '%(name)s' ( " % {'name': name}
    primary_key = ''
    foreign_key = ''

    for column in columns:
        if column[2]:
            # create datatye thith length information
            datatype = "%(col_type)s(%(col_len)s)" % {
                'col_type': column[1], 'col_len': column[2]}
        else:
            # just the datatype
            datatype = column[1]
        if fk and column[6]:
            fk_table, fk_column = column[6].split('.')
            foreign_key += ", FOREIGN KEY(%(col)s) REFERENCES %(ftab)s(%(fcol)s)" % {
                'col': column[0],
                'ftab': fk_table,
                'fcol': fk_column
            }
        ddl += "%(columnname)s %(typeofdata)s %(nullable)s %(uniqueinfo)s, " % {
            'columnname': column[0],
            'typeofdata': datatype,
            'nullable': 'NOT NULL' if column[3] else '',
            'uniqueinfo': 'UNIQUE' if column[4] else ''
            }
        if column[5]:
            primary_key += " PRIMARY KEY(\"%(keyname)s\") " % {'keyname': column[0]}

    ddl += primary_key
    if fk:
        ddl += foreign_key
    ddl += ')'

    print(ddl)
    outfile.write(ddl + ";\n")
    create_table(conn, ddl)

    if fk:
        dropddl = "DROP TABLE %(otab)s" % {'otab': oldname}
        outfile.write(dropddl + ";\n")
        create_table(conn, dropddl)
        renameddl = "ALTER TABLE %(ntab)s RENAME TO %(oname)s" % {
            'ntab': name,
            'oname': oldname
        }
        outfile.write(renameddl + ";\n")
        create_table(conn, renameddl)


def get_column_info(row, fk):
    """ collect all infos needed to define a column """
    cols = [row['column'], row['type'], row['length'],
            row['notnull'], row['unique'], row['primarykey']]
    if fk:
        cols.append(row['foreignkey'])
    return cols


def main(fk=False):
    DATA_DICTIONARY = "/home/kess/private/Training/alfatraining.Schulung/DataEngineer/Zoo/Data_dict_all.csv"
    SQLITE_DB = r"/home/kess/private/Training/alfatraining.Schulung/DataEngineer/Zoo/Zoo.sqlite.db"
    # CSV_COLLUMS = [ "table","column", "type", "length", "primarykey", "foreignkey"
    #           , "unique", "notnull", "Beschreibung", "Beipiel"]

    csvdict = csv.DictReader(open(DATA_DICTIONARY, newline=''))
    sorteddata = sorted(csvdict, key=lambda row: (row['table'], row['primarykey']))

    conn = sqlite3.connect(SQLITE_DB)
    if conn is not None:
        currenttable = ''
        columns = []

        for row in sorteddata:
            if currenttable == '':
                currenttable = row['table']
            if row['table'] == currenttable:
                columns.append(get_column_info(row, fk))
                next
            else:
                # end of current table create DDL
                print("Creating table %(tab)s" % {'tab': currenttable})
                do_table(currenttable, columns, fk, conn, outfile)
                # initialize next table
                columns = []
                columns.append(get_column_info(row, fk))
                currenttable = row['table']

        if bool(currenttable):
            print("Creating table %(tab)s" % {'tab': currenttable})
            do_table(currenttable, columns, fk, conn, outfile)
    else:
        print("Error! cannot create the database connection.")

    conn.commit()
    conn.close()


if __name__ == '__main__':
    SQLFILE = "/home/kess/private/Training/alfatraining.Schulung/DataEngineer/Zoo/Zoo.sqlite.sql"
    outfile = open(SQLFILE, 'w')
    main()
    main(fk=True)
    outfile.close()
