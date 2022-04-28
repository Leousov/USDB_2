from Database import Database
class Pdbms(object):
    DatabaseDict = {}
    ActiveDB = None
    def __init__(self, *args, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
    def CreateDB(dbname) -> None:
        if Pdbms.DatabaseDict.get( dbname ) == None:
            Pdbms.DatabaseDict.update({dbname: Database( dbname ) })
        else:
            raise ValueError( Database )
    def UseDB(dbname) -> None:
        if dbname in Pdbms.DatabaseDict.keys():
            Pdbms.ActiveDB = dbname
        else:
            raise KeyError( Pdbms.DatabaseDict )
    def CreateTable(tablename, *fieldsnames) -> None:
        try:
            Pdbms.DatabaseDict.get( Pdbms.ActiveDB ).CreateTable( tablename, *fieldsnames )
        except:
            raise
    def Insert(tablename, fields) -> None:
        try:
            Pdbms.DatabaseDict.get( Pdbms.ActiveDB ).Insert( tablename, fields )
        except:
            raise
    def Select(tablename, queryoptions = []):
        try:
            return Pdbms.DatabaseDict.get( Pdbms.ActiveDB ).Select(tablename, queryoptions)
        except:
            raise
    def Delete(tablename, queryoptions = [] ):
        try:
            Pdbms.DatabaseDict.get( Pdbms.ActiveDB ).Delete(tablename, queryoptions)
        except:
            raise
    def Count(tablename ):
        try:
            return Pdbms.DatabaseDict.get( Pdbms.ActiveDB ).Count(tablename)
        except:
            raise
    def Clean(tablename):
        try:
            Pdbms.DatabaseDict.get( Pdbms.ActiveDB ).Clean(tablename)
        except:
            raise
    def Delete_1(tablename, queryoptions = []):
        try:
            Pdbms.DatabaseDict.get( Pdbms.ActiveDB ).Delete_1(tablename, queryoptions)
        except:
            raise
    def Restore(tablename):
        try:
            Pdbms.DatabaseDict.get( Pdbms.ActiveDB ).Restore(tablename)
        except:
            raise
if __name__ == "__main__":
    Pdbms.CreateDB("Family")
    Pdbms.UseDB("Family")
    Pdbms.CreateTable("Members", ["Name", "Surname", "Role"])
    Pdbms.CreateTable("Property", ["Name", "Owner"])
    Pdbms.Insert("Members", {"Name": "Mikhail", "Surname": "Soros", "Role": "Father"})
    Pdbms.Insert("Members", {"Name": "Sonya", "Surname": "Soros", "Role": "Mother"})
    Pdbms.Insert("Members", {"Name": "Alyona", "Surname": "Soros", "Role": "Daughter"})
    Pdbms.Insert("Members", {"Name": "Dima", "Surname": "Soros", "Role": "Son"})
    Pdbms.Insert("Members", {"Name": "Alexey", "Surname": "Soros", "Role": "Son"})
    Pdbms.Insert("Property", {"Name": "Box", "Owner": "Mikhail"})
    Pdbms.Insert("Property", {"Name": "Car", "Owner": "Mikhail"})
    Pdbms.Insert("Property", {"Name": "Flat", "Owner": "Mikhail"})
    Pdbms.Insert("Property", {"Name": "Magazin", "Owner": "Sonya"})
    Pdbms.Insert("Property", {"Name": "Second Car", "Owner": "Sonya"})
    Pdbms.Insert("Property", {"Name": "Kitchen", "Owner": "Sonya"})
    Pdbms.Insert("Property", {"Name": "PS5", "Owner": "Dima"})
    Pdbms.Insert("Property", {"Name": "XBox Series X", "Owner": "Alexey"})
    Pdbms.Insert("Property", {"Name": "Doll", "Owner": "Alyona"})
    Pdbms.Insert("Property", {"Name": "Sword", "Owner": "Alyona"})