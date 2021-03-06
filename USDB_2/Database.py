from Table import Table
class Database(object):
    def __init__(self, dbname, *args, **kwargs) -> None:
        self.TableDict = {}
        self.dbname = dbname
    def CreateTable(self, tablename, *fieldsnames) -> None:
        if self.TableDict.get( tablename ) == None:
            self.TableDict.update({ tablename : Table( tablename, *fieldsnames ) })
        else:
            raise ValueError( Table )
    def Insert(self, tablename, fields ) -> None:
        self.TableDict.get( tablename ).Insert( fields )
    def Select(self, tablename, queryoptions = []):
        return self.TableDict.get( tablename ).Select(queryoptions)
    def Delete(self, tablename, queryoptions = []):
        self.TableDict.get( tablename ).Delete(queryoptions)

