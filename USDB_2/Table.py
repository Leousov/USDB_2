from csv import DictReader, DictWriter
import os

from Worker import Worker
class Table(object):
    def __init__(self, tablename = "Dull", *fieldsnames ) -> None:
        #self.filename = tablename
        #self.fieldsnames = fieldsnames
        #self.file = open( tablename + ".csv", "w", newline= "" )
        ##Twriter = DictReader( csvfile, fieldnames = fieldsnames)
        #self.file.close()
        fieldsnames = list(fieldsnames[0])
        fieldsnames.append("del")
        self.worker = Worker(tablename, *fieldsnames)
    def Insert(self, fields) -> None:
        fields["del"] = False
        self.worker.Insert(fields)
    def Select(self, queryoptions = []):
        final = []
        newstp = []
        q = True
        if queryoptions == []:
            try:
                i, final = self.worker.Read()
            except:
                i = 0
                final = 0
        else:
            i, Treader = self.worker.Read()
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
        return final
    def Delete(self, queryoptions = []):
        final = []
        newstp = []
        q = True
        if queryoptions == []:
            self.worker.Delete()
        else:
            i, Treader = self.worker.Read()
            for isinvert, fieldname, values in queryoptions: 
                if q:
                    for row in Treader:
                        if  ( isinvert ^ (row.get( fieldname ) in values) ):
                            newstp.append(row)

                    final = newstp.copy()
                    q = False
                else:
                    newstp = []
                    for i in range( len(final) ):
                        if  ( isinvert ^ (final[i].get( fieldname ) in values) ):
                            newstp.append(final[i])
                    
                    final = newstp.copy()
            self.worker.Delete()
            for i in newstp:
                self.worker.Insert(i)
        return final
    
    def Count(self):
        i, final = self.worker.Read()
        return i
    def Clean(self):
        fieldname = "del"
        newstp = []
        i, Treader = self.worker.Read()
        for row in Treader:
            if  ( row.get( fieldname ) == "False" ):
                newstp.append(row)
        self.worker.Delete()
        for i in newstp:
            self.worker.Insert(i)
    def Delete_1(self, queryoptions = []):
        final = []
        newstp = []
        q = True
        if queryoptions == []:
            i, Treader = self.worker.Read()
            self.worker.Delete()
            for row in Treader:
                row["del"] = True
                newstp.append(row)
                
            for i in newstp:
                self.worker.Insert(i)
        else:
            i, Treader = self.worker.Read()
            for isinvert, fieldname, values in queryoptions: 
                if q:
                    for row in Treader:
                        if  ( isinvert ^ (row.get( fieldname ) in values) ):
                            newstp.append(row)
                        else:
                            row["del"] = True
                            newstp.append(row)
                    final = newstp.copy()
                    q = False
                else:
                    newstp = []
                    for i in range( len(final) ):
                        if  ( isinvert ^ (final[i].get( fieldname ) in values) ):
                            newstp.append(final[i])
                        else:
                            row["del"] = True
                            newstp.append(row)
                    final = newstp.copy()
            self.worker.Delete()
            for i in newstp:
                self.worker.Insert(i)
    def Restore(self):
        fieldname = "del"
        newstp = []
        i, Treader = self.worker.Read()
        for row in Treader:
            row[fieldname] = False
            newstp.append(row)
        self.worker.Delete()
        for i in newstp:
            self.worker.Insert(i)