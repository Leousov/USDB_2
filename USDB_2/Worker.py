from csv import DictReader, DictWriter
from csv import *
import csv
import os
class Worker():
    format = "csv"
    def __init__(self):
        self.file = None
        self.reader = None
        self.writer = None
    def __init__(self, tablename = 'aaa', *fieldsnames):
        self.filename = tablename
        self.fieldsnames = fieldsnames
        self.file = open( tablename + ".csv", "w", newline= "" )
        self.file.close()
    def Insert(self, fields):
        if os.path.exists( self.filename + ".csv"):
            self.file = open( self.filename + ".csv", "a", newline= "" )
        else:
            self.file = open( self.filename + ".csv", "w", newline= "" )
        try:
            self.writer = DictWriter(self.file, fieldnames = self.fieldsnames )
            self.writer.writerow(fields)
        except:
            raise
        finally:
            self.file.close()
    def Read(self):
        try:
            final = []
            self.file = open( self.filename + ".csv", "r", newline= "" )
            self.reader = DictReader( self.file, fieldnames = self.fieldsnames )
            i = 0
            for row in self.reader:
                i += 1
                final.append(row)
            self.file.close()
            return i, final
        finally:
            self.file.close()
    def Delete(self):
        try:
            if os.path.exists( self.filename + ".csv"):
                self.file = open( self.filename + ".csv", "w", newline= "" )
        except: raise
        finally:
            self.file.close()