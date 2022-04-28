from typing import ValuesView
import unittest
import unittest.mock
from Pdbms import Pdbms
from Table import Table
from Worker import Worker

class Test_Pdbms_CreateDB( unittest.TestCase ):
    def test_CreateDB_none(self):
        Pdbms.CreateDB(None)
        self.assertEqual( Pdbms.DatabaseDict.get( None ).dbname, None )
    def test_CreateDB(self):
        Pdbms.CreateDB("One")
        self.assertEqual( Pdbms.DatabaseDict.get( "One" ).dbname, "One" )
    def test_CreateDB_copy(self):
        try:
            Pdbms.CreateDB("One")
        except:
            self.assertRaises( ValueError )
    def test_CreateDB_num(self):
        try:
            Pdbms.CreateDB(1)
        except:
            self.assertRaises( ValueError )

class Test_Pdbms_UseDB( unittest.TestCase ):
    def setUp(self) -> None:
        Pdbms.DatabaseDict = {}
        Pdbms.ActiveDB = None
    def test_Use_DB_wrong(self):
        try:
            Pdbms.UseDB( "One" )
        except:
            self.assertRaises( KeyError )
   
class Test_Pdbms_CreateTable( unittest.TestCase ):
    def setUp(self) -> None:
        Pdbms.DatabaseDict = {}
        Pdbms.ActiveDB = None
        Pdbms.CreateDB("One")
        Pdbms.UseDB("One")
    def test_CreateTable_none( self ):
        try:
            Pdbms.CreateTable(None)
        except:
            self.assertRaises( ValueError )
    def test_CreateTable( self ):
        Pdbms.CreateTable("one", ["name", "surname"])
        self.assertEqual( Pdbms.DatabaseDict.get( Pdbms.ActiveDB ).TableDict.get( "one" ).worker.filename, "one" ) 
    def test_CreateTable_copy(self):
        try:
            Pdbms.CreateTable("one", ["name", "surname"])
            Pdbms.CreateTable("one", ["asdasda", "sasdaad"])
        except:
            self.assertRaises( ValueError )
             
class Test_Pdbms_Insert( unittest.TestCase ):
    def setUp(self) -> None:
        Pdbms.DatabaseDict = {}
        Pdbms.ActiveDB = None
        Pdbms.CreateDB("One")
        Pdbms.UseDB("One")
        Pdbms.CreateTable( "one", [12, "mama"] )

    def test_Pdbms_Insert_none( self ):
        try:
            Pdbms.Insert()
        except:
            self.assertRaises( TypeError )
    def test_Pdbms_Insert_wrong_all( self ):
        try:
            Pdbms.Insert("two", {11: "Goo", "papa": "ya", "aaaa": 1})
        except:
            self.assertRaises( AttributeError )
    def test_Pdbms_Insert_ok( self ):
        Pdbms.Insert("one", {12: "Goo", "mama": "ya"})        
    def test_Pdbms_Insert_wrong_name( self ):
        try:
            Pdbms.Insert("two", {12: "Goo", "mama": "ya"})
        except:
            self.assertRaises( AttributeError )
    def test_Pdbms_Insert_wrong_fields( self ):
        try:
            Pdbms.Insert("one", {11: "Goo", "papa": "ya", "aaaa": 1})
        except:
            self.assertRaises( ValueError )

class Test_Pdbms_Select( unittest.TestCase ): 
    def setUp(self) -> None:
        Pdbms.DatabaseDict = {}
        Pdbms.ActiveDB = None
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
    def test_Pdbms_Select_none( self ):
        try:
            Pdbms.Select()
        except:
            self.assertRaises( TypeError )
    def test_Pdbms_Select_ok( self ):
        s = Pdbms.Select("Members",[])
        names = ["Mikhail", "Sonya", "Alyona", "Dima", "Alexey"]
        surname = ["Soros"]
        roles = ["Son", "Father", "Mother", "Daughter"]
        for i in s:
            self.assertIn( i.get( "Name" ), names )
            self.assertIn( i.get( "Surname" ), surname )
            self.assertIn( i.get( "Role" ), roles )
    def test_Pdbms_Select_complex_1( self ):
        s = Pdbms.Select("Members",[ [ True, "Role", ["Son", "Daughter"] ] ])
        names = ["Alyona", "Dima", "Alexey"]
        surname = ["Soros"]
        roles = ["Son", "Daughter"]
        for i in s:
            self.assertIn( i.get( "Name" ), names )
            self.assertIn( i.get( "Surname" ), surname )
            self.assertIn( i.get( "Role" ), roles )
    def test_Pdbms_Select_complex_2( self ):
        s = Pdbms.Select("Members",[ [ True, "Role", ["Son", "Daughter"] ] ])
        owners = []
        for i in s:
            owners.append( i.get( "Name" ) )
        s = Pdbms.Select("Property",[ [ True, "Owner", owners ] ])
        names = ["PS5", "XBox Series X", "Doll", "Sword"]
        owners = ["Alexey", "Alyona", "Dima"]
        for i in s:
            self.assertIn( i.get( "Name" ), names )
            self.assertIn( i.get( "Owner" ), owners )

class Test_Pdbms_Delete( unittest.TestCase ):
    def setUp(self) -> None:
        Pdbms.DatabaseDict = {}
        Pdbms.ActiveDB = None
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
        Pdbms.Insert("Property", {"Name": "Flat", "Owner": "Mikhai l"})
        Pdbms.Insert("Property", {"Name": "Magazin", "Owner": "Sonya"})
        Pdbms.Insert("Property", {"Name": "Second Car", "Owner": "Sonya"})
        Pdbms.Insert("Property", {"Name": "Kitchen", "Owner": "Sonya"})
        Pdbms.Insert("Property", {"Name": "PS5", "Owner": "Dima"})
        Pdbms.Insert("Property", {"Name": "XBox Series X", "Owner": "Alexey"})
        Pdbms.Insert("Property", {"Name": "Doll", "Owner": "Alyona"})
        Pdbms.Insert("Property", {"Name": "Sword", "Owner": "Alyona"})
    def test_Pdbms_Delete_Children(self) -> None:
        Pdbms.Delete( "Members", [[ True, "Role", ["Son", "Daughter"] ]] )
        s = Pdbms.Select("Members",[])
        names = ["Mikhail", "Sonya"]
        surname = ["Soros"]
        roles = ["Father", "Mother"]
        self.assertNotEqual(s, [])
        for i in s:
            self.assertIn( i.get( "Name" ), names )
            self.assertIn( i.get( "Surname" ), surname )
            self.assertIn( i.get( "Role" ), roles )
    def test_Pdbms_Delete_all(self) -> None:
        Pdbms.Delete( "Members", [] )
        s = Pdbms.Select("Members",[])
        names = []
        surname = []
        roles = []
        for i in s:
            self.assertIn( i.get( "Name" ), names )
            self.assertIn( i.get( "Surname" ), surname )
            self.assertIn( i.get( "Role" ), roles )
    def test_Pdbms_Delete_complex(self) -> None:
        Pdbms.Delete( "Members" ,[[ False, "Role", ["Father", "Mother"] ], [ True, "Name", ["Mikhail"]]  ])
        s = Pdbms.Select("Members")
        names = ["Sonya"]
        surname = ["Soros"]
        roles = ["Mother"]
        self.assertNotEqual(s, [])
        for i in s:
            self.assertIn( i.get( "Name" ), names )
            self.assertIn( i.get( "Surname" ), surname )
            self.assertIn( i.get( "Role" ), roles )

class Test_Pdbms_Count( unittest.TestCase ):
    def setUp(self) -> None:
        Pdbms.DatabaseDict = {}
        Pdbms.ActiveDB = None
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
        Pdbms.Insert("Property", {"Name": "Flat", "Owner": "Mikhai l"})
        Pdbms.Insert("Property", {"Name": "Magazin", "Owner": "Sonya"})
        Pdbms.Insert("Property", {"Name": "Second Car", "Owner": "Sonya"})
        Pdbms.Insert("Property", {"Name": "Kitchen", "Owner": "Sonya"})
        Pdbms.Insert("Property", {"Name": "PS5", "Owner": "Dima"})
        Pdbms.Insert("Property", {"Name": "XBox Series X", "Owner": "Alexey"})
        Pdbms.Insert("Property", {"Name": "Doll", "Owner": "Alyona"})
        Pdbms.Insert("Property", {"Name": "Sword", "Owner": "Alyona"})
    def test_Pdbms_Count(self):
        self.assertEqual( Pdbms.Count("Property"), 10 )

class Test_Pdbms_Clean( unittest.TestCase ):
    def setUp(self) -> None:
        Pdbms.DatabaseDict = {}
        Pdbms.ActiveDB = None
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
        Pdbms.Insert("Property", {"Name": "Flat", "Owner": "Mikhai l"})
        Pdbms.Insert("Property", {"Name": "Magazin", "Owner": "Sonya"})
        Pdbms.Insert("Property", {"Name": "Second Car", "Owner": "Sonya"})
        Pdbms.Insert("Property", {"Name": "Kitchen", "Owner": "Sonya"})
        Pdbms.Insert("Property", {"Name": "PS5", "Owner": "Dima"})
        Pdbms.Insert("Property", {"Name": "XBox Series X", "Owner": "Alexey"})
        Pdbms.Insert("Property", {"Name": "Doll", "Owner": "Alyona"})
        Pdbms.Insert("Property", {"Name": "Sword", "Owner": "Alyona"})
    def test_Pdbms_Clean_All(self):
        Pdbms.Delete_1( "Members", [] )
        Pdbms.Clean("Members")
        s = Pdbms.Select("Members",[])
        names = []
        surname = []
        roles = []
        for i in s:
            self.assertIn( i.get( "Name" ), names )
            self.assertIn( i.get( "Surname" ), surname )
            self.assertIn( i.get( "Role" ), roles )
    def test_Pdbms_Clean_Children(self):
        Pdbms.Delete_1( "Members", [[ True, "Role", ["Son", "Daughter"] ]] )
        Pdbms.Clean("Members")
        s = Pdbms.Select("Members",[])
        names = ["Mikhail", "Sonya"]
        surname = ["Soros"]
        roles = ["Father", "Mother"]
        self.assertNotEqual(s, [])
        for i in s:
            self.assertIn( i.get( "Name" ), names )
            self.assertIn( i.get( "Surname" ), surname )
            self.assertIn( i.get( "Role" ), roles )
    def test_Pdbms_Clean_complex(self):
        Pdbms.Delete_1( "Members" ,[[ False, "Role", ["Father", "Mother"] ], [ True, "Name", ["Mikhail"]]  ])
        Pdbms.Clean("Members")
        s = Pdbms.Select("Members")
        names = ["Sonya"]
        surname = ["Soros"]
        roles = ["Mother"]
        self.assertNotEqual(s, [])
        for i in s:
            self.assertIn( i.get( "Name" ), names )
            self.assertIn( i.get( "Surname" ), surname )
            self.assertIn( i.get( "Role" ), roles )

class Test_Pdbms_Delete_1( unittest.TestCase ):
    def setUp(self) -> None:
        Pdbms.DatabaseDict = {}
        Pdbms.ActiveDB = None
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
        Pdbms.Insert("Property", {"Name": "Flat", "Owner": "Mikhai l"})
        Pdbms.Insert("Property", {"Name": "Magazin", "Owner": "Sonya"})
        Pdbms.Insert("Property", {"Name": "Second Car", "Owner": "Sonya"})
        Pdbms.Insert("Property", {"Name": "Kitchen", "Owner": "Sonya"})
        Pdbms.Insert("Property", {"Name": "PS5", "Owner": "Dima"})
        Pdbms.Insert("Property", {"Name": "XBox Series X", "Owner": "Alexey"})
        Pdbms.Insert("Property", {"Name": "Doll", "Owner": "Alyona"})
        Pdbms.Insert("Property", {"Name": "Sword", "Owner": "Alyona"})

class Test_Pdbms_Restore( unittest.TestCase ):
    def setUp(self) -> None:
        Pdbms.DatabaseDict = {}
        Pdbms.ActiveDB = None
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
        Pdbms.Insert("Property", {"Name": "Flat", "Owner": "Mikhai l"})
        Pdbms.Insert("Property", {"Name": "Magazin", "Owner": "Sonya"})
        Pdbms.Insert("Property", {"Name": "Second Car", "Owner": "Sonya"})
        Pdbms.Insert("Property", {"Name": "Kitchen", "Owner": "Sonya"})
        Pdbms.Insert("Property", {"Name": "PS5", "Owner": "Dima"})
        Pdbms.Insert("Property", {"Name": "XBox Series X", "Owner": "Alexey"})
        Pdbms.Insert("Property", {"Name": "Doll", "Owner": "Alyona"})
        Pdbms.Insert("Property", {"Name": "Sword", "Owner": "Alyona"})
    def test_Pdbms_Delete_1_Children(self) -> None:
        Pdbms.Delete_1( "Members", [[ True, "Role", ["Son", "Daughter"] ]] )
        s = Pdbms.Select("Members",[])
        names = ["Mikhail", "Sonya"]
        surname = ["Soros"]
        roles = ["Father", "Mother"]
        self.assertNotEqual(s, [])
        for i in s:
            if i.get( "del" ) == "True":
                self.assertNotIn(i.get( "Name" ), names)
                self.assertIn(i.get( "Surname" ), surname)
                self.assertNotIn(i.get( "Role" ), roles)
            else:
                self.assertIn( i.get( "Name" ), names )
                self.assertIn( i.get( "Surname" ), surname )
                self.assertIn( i.get( "Role" ), roles )
    def test_Pdbms_Delete_1_all(self) -> None:
        Pdbms.Delete_1( "Members", [] )
        s = Pdbms.Select("Members",[])
        names = []
        surname = ["Soros"]
        roles = []
        self.assertNotEqual(s, [])
        for i in s:
            if i.get( "del" ) == "True":
                self.assertNotIn(i.get( "Name" ), names)
                self.assertIn(i.get( "Surname" ), surname)
                self.assertNotIn(i.get( "Role" ), roles)
            else:
                self.assertIn( i.get( "Name" ), names )
                self.assertIn( i.get( "Surname" ), surname )
                self.assertIn( i.get( "Role" ), roles )
    def test_Pdbms_Delete_1_complex(self) -> None:
        Pdbms.Delete_1( "Members" ,[[ False, "Role", ["Father", "Mother"] ], [ True, "Name", ["Mikhail"]]  ])
        s = Pdbms.Select("Members")
        names = ["Sonya"]
        surname = ["Soros"]
        roles = ["Mother"]
        self.assertNotEqual(s, [])
        for i in s:
            if i.get( "del" ) == "True":
                self.assertNotIn(i.get( "Name" ), names)
                self.assertIn(i.get( "Surname" ), surname)
                self.assertNotIn(i.get( "Role" ), roles)
            else:
                self.assertIn( i.get( "Name" ), names )
                self.assertIn( i.get( "Surname" ), surname )
                self.assertIn( i.get( "Role" ), roles )

class Test_Worker_Insert( unittest.TestCase ):
    def test_Worker_Insert_Ok(self):
        t = Table("ok",["f", "s"])
        t.worker.Insert = unittest.mock.MagicMock()
        t.Insert({"f":"12","s":"23"})
        t.worker.Insert.assert_called()
    def test_Worker_Insert_Args(self):
        t = Table("ok",["f", "s"])
        t.worker.Insert = unittest.mock.MagicMock()
        t.Insert({"f":"12","s":"23"})
        t.worker.Insert.assert_called_once_with({"f":"12","s":"23","del":False})
    def test_Worker_Insert_None(self):
        t = Table("ok",[])
        t.worker.Insert = unittest.mock.MagicMock()
        t.Insert({})
        t.worker.Insert.assert_called_once_with({"del":False})

class Test_Worker_Read( unittest.TestCase ):
    def test_Worker_Read_Ok(self):
        t = Table("ok",["f", "s"])
        t.worker.Read = unittest.mock.MagicMock()
        t.Select()
        t.worker.Read.assert_called()

class Test_Worker_Read( unittest.TestCase ):
    def test_Worker_Read_Ok(self):
        t = Table("ok",["f", "s"])
        t.worker.Delete = unittest.mock.MagicMock()
        t.Delete()
        t.worker.Delete.assert_called()

if __name__ == '__main__':
    unittest.main()
