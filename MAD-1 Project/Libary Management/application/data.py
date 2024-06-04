import sqlite3

class AlertUpdate:
    def __init__(self):
        self.status = None
    def LoginStatus(self,value):
        self.status = {"status":value}
        return self.status
    

class ReturnDate:
    def __init__(self):
        self.MonthDays = None
        self.Day = None
        self.month = None
        self.year = None
        self.adddays = 7
    
    def Zerosetter(self,num):
        if num > 9:
            return str(num)
        else:
            return f'0{num}'
    def monthsetterNum(self,month):
        if month[0] == "0":
            return int(month[1])
        else:
            return int(month)
        
    def setdate(self,current_date):
        try:
            date = current_date.split("-")
            monthCode = self.monthsetterNum(date[1])
            currentDay = self.monthsetterNum(date[0])
            currentyear = int(date[2])
            months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            monthsSetter = {"30_day":["Apr","Jun","Sep","Nov"],"31_days":["Jan","Mar","May","Jul","Aug","Oct","Dec"],"leep_yrs":["Feb"]}
            monthsSetterKeys = monthsSetter.keys()
            for i in monthsSetterKeys:
                for j in monthsSetter[i]:
                    if i == "30_day":
                        if months[monthCode-1] == j:
                            self.MonthDays = 30
                    elif i == "31_days":
                        if months[monthCode-1] == j:
                            self.MonthDays = 31
                    else:
                        if months[monthCode-1] == "Feb":
                            leapCheck = int(date[2])%4
                            if leapCheck == 0:
                                self.MonthDays = 29
                            else:
                                self.MonthDays = 28
            AddDays = currentDay + self.adddays
            if AddDays > self.MonthDays:
                self.Day = AddDays - self.MonthDays
                if monthCode < 12:
                    self.month = monthCode + 1
                    self.year = currentyear
                else:
                    self.month = 1
                    self.year = currentyear + 1
            else:
                self.Day = AddDays
                self.month = monthCode
                self.year = currentyear
            print(self.Day,self.month,self.year)
            if self.Day is not None and self.month is not None and self.year is not None:
                resObj = {"status":"good","returnDate":f'{self.Zerosetter(self.Day)}-{self.Zerosetter(self.month)}-{self.year}',"err":None}
                return resObj
            else:
                resObj = {"status":"bad","returnDate":None,"err":None}
                return resObj
        except Exception as err:
            resObj = {"status":"error","returnDate":None,"err":err}
            return resObj
        

class Database:
    def __init__(self):
        self.connect = sqlite3.connect("Libdata.db",check_same_thread=False)

    def GET_All(self,query):
        try :
            cur = self.connect.cursor()
            cur.execute(query)
            data = cur.fetchall()
            self.connect.commit()
            return {"status":"good","data":data}
        except sqlite3.Error as err:
            print("err in get_all book function")
            print("ERROR is : ",err)
        finally:
            cur.close()
    def GET_ALL_CONDITION(self,query,datas):
        try :
            cur = self.connect.cursor()
            cur.execute(query,datas)
            data = cur.fetchall()
            self.connect.commit()
            return {"status":"good","data":data}
        except sqlite3.Error as err:
            print("err in get_all book function")
            print("ERROR is : ",err)
        finally:
            cur.close()
    
    def UpdateCmd(self,query,data):
        try:
            cur = self.connect.cursor()
            cur.execute(query,data)
            self.connect.commit()
            cur.close()
            return {"status":"done"}
            
        except sqlite3.Error as err:
            print("error",err)
            return {"status":"err"}
        finally:
            print("completed")


    def GETSECTION(self):
        try:
            SECTIONDATA = self.GET_All("select * from SECTIONTYPE")
            SECTIONIMAGEDATA = self.GET_All("select * from SECTION_IMAGE")
            finalValue = {"status":"good","data":[]}
            for i in SECTIONDATA["data"]:
                for j in SECTIONIMAGEDATA["data"]:
                    if i[0] == j[0]:
                        finalValue["data"].append({"id":i[0],"title":i[1],"img":j[1]})
                        # finalValue["data"][i[1]] = j[1]
                        # finalValue["data"]["id"] = i[0]
            return finalValue
        except Exception as err:
            print("Error in getsection function !")
            print(err)
        
    def InsertSection(self,id,section_name,date,des,imgpath):
        try:
            cur = self.connect.cursor()
            query = """INSERT INTO SECTIONTYPE (sec_id, sec_name, data_created,description) VALUES(?,?,?,?)"""
            sec_imgQuery = """INSERT INTO SECTION_IMAGE (id, value_src) VALUES(?,?)"""
            data = (id,section_name,date,des)
            data1 = (id,imgpath)
            cur.execute(query,data)
            cur.execute(sec_imgQuery,data1)
            self.connect.commit()
            return {"status":"done"}
        except sqlite3.Error as err:
            print("Error in upload the section details")
            print("ERROR : {err}".format(err=err))
            return {"status":"bad"}
        finally:
            cur.close()


    def InsertSectionBook(self,gener,bookid):
        try:
            cur = self.connect.cursor()
            Sectiondata = self.GET_All("""select * from SECTIONTYPE""")
            idStore = ""
            for i in Sectiondata["data"]:
                if i[1] == gener:
                    idStore = i[0]
                    break
            query = """INSERT INTO SECTION_BOOK(sec_id, book_id)
            VALUES(?,?)
            """
            cur.execute(query,(idStore,bookid))
            self.connect.commit()
            return {"status":"sectionupdated"}
        except sqlite3.Error as err:
            print("Error in uploading in Section_book")
            print("ERROR is : ",err)
        finally:
            cur.close()


    def InsertBooks(self,data):
        try:
            cursor = self.connect.cursor()
            query = """INSERT INTO BOOKSTORE (bookid,bookname,bookpath,author,bookposterpath,section,publishdate)
            VALUES(?,?,?,?,?,?,?)
            """
            DATAFORID = self.GET_All("select * from BOOKSTORE")
            valueID  = len(DATAFORID["data"])+1
            finalID = ""
            
            if (valueID < 10):
                finalID = f'BOO0{valueID}'
            else:
                finalID = f'BOO{valueID}'
            dataUpload = (finalID,data[0],data[1],data[2],data[3],data[4],data[5])
            SectionUpload = self.InsertSectionBook(data[4],finalID)
            cursor.execute(query,dataUpload)
            
            self.connect.commit()
            return {"status":"upload"}
        except sqlite3.Error as err:
            print("error in insertbook")
            print("ERROR is : ",err)
            return {"status":"notuploaded"}
        finally:
            cursor.close()

    def GET_allBookSection (self):
        try:
            bookData = self.GET_All("SELECT * FROM BOOKSTORE")
            sectionData = self.GET_All("SELECT * FROM SECTIONTYPE")
            sectionbookData = self.GET_All("SELECT * FROM SECTION_BOOK")
            print(bookData["data"])
            print(sectionData["data"])
            print(sectionbookData["data"])
            finalDataShare = {}
            for keys in sectionData["data"]:
                finalDataShare[keys[1]] = []
            for value_id in sectionbookData["data"]:
                bookcon = None
                sectionName = None
                for bookdata in bookData["data"]:
                    if (value_id[1] == bookdata[0]):
                        bookcon = bookdata
                        break
                for seccon in sectionData["data"]:
                    if (value_id[0] == seccon[0]):
                        sectionName = seccon[1]
                        break
                finalDataShare[sectionName].append(bookcon)
                bookcon = None
                sectionName = None
            return {"status":"good","data":finalDataShare}
        except Exception as err:
            print(err)
            return err

        
    def GET_libdata(self):
        try :
            cur = self.connect.cursor()
            query = "SELECT * FROM LIB"
            cur.execute(query)
            dataLIb = cur.fetchall()
            print("connected to lib database ......")
            self.connect.commit()
            if dataLIb == []:
                return {"status":"no-users","data":[]}
            return {"status":"good","data":dataLIb}
        except sqlite3.Error as err:
            print("Error in fetch data of lib")
            print("ERROR is : ",err)
        finally:
            cur.close()

    def SET_newlib(self,username, email, password):
        # data's of user's
        fullData = self.GET_libdata()
        #check duplicate user flag ---type:boolean
        checkFlag = False
        #id for db
        count_id = 0
        if fullData["status"] == "no-users":
            count_id = 1
        elif fullData["status"] == "good":
            for i in fullData["data"]:
                if i[1] == username:
                    checkFlag = True
                    break
            if checkFlag == False:
                count_id = len(fullData["data"])+1

        if checkFlag == True:
            return {"status":"username_exists"}
        try:
            cur = self.connect.cursor()
            query = '''INSERT INTO LIB (id, username, email, password) VALUES(?,?,?,?)'''
            data_user = (count_id, username, email, password)
            cur.execute(query,data_user)
            self.connect.commit()
            return {"status":"account created...."}
        except sqlite3.Error as err:
            print("error in add users in Lib")
            print("Error is : ",err)
            return {"status":"err"}
        finally:
            cur.close()

        

    def UpdateStudentBook(self,bookid,stdid,issueData,returnData,book_status):
        try:
            cur = self.connect.cursor()
            query = """INSERT INTO STATUSBOOK_TABEL (book_id,user_id, issue_data, return_data,book_status) VALUES(?,?,?,?,?)"""
            data = (bookid,stdid,issueData,returnData,book_status)
            cur.execute(query,data)
            self.connect.commit()
            return {"status":"good"}
        except sqlite3.Error as err:
            print("ERROR in updatebook")
            print("ERROR is : ",err)
            return {"status":"bad"}
        finally:
            cur.close()        
    def BOOKCOUNT(self,stdid):
        try:
            cur = self.connect.cursor()
            currentdata = self.GET_All(f'SELECT * FROM STUDENT WHERE STUDENT.id = {stdid}')["data"]
            statusFlag = False
            bookcount = currentdata[0][4]
            if bookcount < 5:
                bookcount += 1
            else:
                statusFlag = True
            if statusFlag == False:    
                query = f'UPDATE STUDENT SET bookcount = {bookcount} WHERE id = {stdid}'
                cur.execute(query)
                self.connect.commit()
                return {"bookcount":"done"}
            return {"bookcount":"not done"}
        except sqlite3.Error as err:
            print("ERROR in BOOKCOUNT")
            print("ERROR is : ",err)
        finally:
            cur.close()

    def get_Studentdata(self):
        try:
            cur = self.connect.cursor()
            query = "select * from STUDENT"
            cur.execute(query)
            final_data = cur.fetchall()
            self.connect.commit()
            cur.close()
            if final_data is None:
                return []
            else:
                print("student data")
                print("final_data",final_data)
                return final_data
        except sqlite3.Error as err:
            print(err)

    def GET_User(self,username,password):
        try:
            cur = self.connect.cursor()
            query = "select * from STUDENT as st where st.username = ?"
            cur.execute(query,(username,))
            con = cur.fetchall()
            self.connect.commit()
            if len(con) == 0:
                return {"status":"username-err","data":[]}
            else:
                if con[0][2] == password:
                    return {"status":"password-success","data":con}
                return {"status":"password-err","data":[]}
            
        except sqlite3.Error as err:
            print("ERROR is : ",err)

        finally:
            cur.close() 


    def addStudent(self,username,password,email):
        try:
            data = self.get_Studentdata()
            count = 0
            checkuser = False
            if data is None:
                count = 1
            else:
                for i in data:
                    if i[1] == username:
                        checkuser = True
                        break
                count = len(data) + 1
            if checkuser == False:
                cur = self.connect.cursor()
                query = '''INSERT INTO STUDENT VALUES(?,?,?,?,?)'''
                cur.execute(query,(count,username,password,email,0))
                self.connect.commit()
                cur.close()
                return {"status":"success"}
            else:
                return {"status":"create-new"}
        except sqlite3.Error as err:
            print(err)
            return
    

    def BarrowedData(self,userid,status):
        try:
            userBookContainer = self.GET_All(f'select * from STATUSBOOK_TABEL as st where st.book_status = {status} and st.user_id = {userid}')["data"]
            bookContainer = self.GET_All(f'select * from BOOKSTORE')["data"]
            finalData = {"status":"default","data":{},"err":None}
            print(userBookContainer)
            if len(userBookContainer) != 0 and len(bookContainer) != 0:
                for i in userBookContainer:
                    for j in bookContainer:
                        if i[0] == j[0]:
                            finalData["data"][i[0]] = [i,j]
                finalData["status"] = "good"
                return finalData
            else:
                finalData["status"] = "bad"
                return finalData
        except Exception as err:
            print("ERROr in barroweddata ")
            print("ERROR is ",err)
            finalData["stauts"] = "err"
            finalData["err"] = err
            return finalData
