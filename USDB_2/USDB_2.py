from Pdbms import Pdbms

print("Welcome!\nThat's Leo Usov's DBMS")
while True:
    print("""Required numbers of commands:
    1 - Create Database
    2 - Use Database
    3 - Create Table
    4 - Insert row into table
    5 - Select some row from table
    6 - Show databases list
    7 - Show tables list of active database
    0 - Exit\n""")
    stro = input("Enter the number of command:\n")
    try:
        i = int(stro)
    except:
        i = -1
    if   i == 1:
        Pdbms.CreateDB( input( "Enter a name of a new DB:\n" ) )
    elif i == 2:
        Pdbms.UseDB( input( "Enter the name of DB:\n" ) )
    elif i == 3:
        name = input( "Enter a name of a new table:\n" )
        fields = []
        j = 0
        while j == 0:
            try:
                j = int(input( "Enter the number of fields of table:\n" ))
            except:
                j = 0
        for k in range(j):
            fields.append( input( "Enter the name of the field #{}\n".format(k) ) )
        Pdbms.CreateTable(name , fields )
    elif i == 4:
        name = input( "Enter the name of Table:\n" )


