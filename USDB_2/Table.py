from csv import DictReader, DictWriter
import os
class Table(object):
    def __init__(self, tablename = "Dull", *fieldsnames ) -> None:
        self.filename = tablename
        self.fieldsnames = fieldsnames
        self.file = open( tablename + ".csv", "w", newline= "" )
        #Twriter = DictReader( csvfile, fieldnames = fieldsnames)
        self.file.close()
    def Insert(self, fields) -> None:
        if os.path.exists( self.filename + ".csv"):
            self.file = open( self.filename + ".csv", "a", newline= "" )
        else:
            self.file = open( self.filename + ".csv", "w", newline= "" )
        try:
            Twriter = DictWriter(self.file, *self.fieldsnames )
            Twriter.writerow(fields )
        except:
            raise
        finally:
            self.file.close()

    def Select(self, queryoptions = []):
        final = []
        newstp = []
        q = True
        if queryoptions == []:
            self.file = open( self.filename + ".csv", "r", newline= "" )
            Treader = DictReader( self.file, *self.fieldsnames )
            for row in Treader:
                final.append(row)
        else:
            self.file = open( self.filename + ".csv", "r", newline= "" )
            Treader = DictReader( self.file, *self.fieldsnames )
            for isinvert, fieldname, values in queryoptions: 
                if q:
                    for row in Treader:
                        if isinvert and row.get( fieldname ) in values:
                            newstp.append(row)
                        elif not isinvert and not (row.get( fieldname ) in values) :
                            newstp.append(row)
                    final = newstp.copy()
                    q = False
                else:
                    for i in range( len(final) ):
                        if isinvert and final[i].get( fieldname ) in values:
                            newstp.append(row)
                        elif not isinvert and not (final[i].get( fieldname ) in values) :
                            newstp.append(row)
        self.file.close()
        return final
    def Delete(self, queryoptions = []):
        final = []
        newstp = []
        q = True
        if queryoptions == []:
            self.file = open( self.filename + ".csv", "w", newline= "" )
        else:
            self.file = open( self.filename + ".csv", "r", newline= "" )
            Treader = DictReader( self.file, *self.fieldsnames )
            for isinvert, fieldname, values in queryoptions: 
                if q:
                    for row in Treader:
                        if not (isinvert and row.get( fieldname ) in values):
                            newstp.append(row)
                        elif not isinvert and not (row.get( fieldname ) in values) :
                            newstp.append(row)
                    final = newstp.copy()
                    q = False
                else:
                    for i in range( len(final) ):
                        if not (isinvert and final[i].get( fieldname ) in values):
                            newstp.append(row)
                        elif not isinvert and not (final[i].get( fieldname ) in values) :
                            newstp.append(row)
                self.file.close()
                self.file = open( self.filename + ".csv", "w", newline= "" )
                Twriter = DictWriter(self.file, self.fieldsnames )
                for i in newstp:
                    Twriter.writerow(i)
        self.file.close()
        return final