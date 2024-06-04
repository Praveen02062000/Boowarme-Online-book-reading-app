from flask import Flask,render_template,url_for,redirect,request,session,make_response
from werkzeug.utils import secure_filename
from flask import current_app as App
import time
import os
import sqlite3


# class for database and some function 

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
            DATAFORID = self.GET_All("select bookid from BOOKSTORE")["data"][-1][0]
            idCode = "BOO"
            sliceId = DATAFORID[3:]
            idnum = 0
            if sliceId[0] == "0" and len(sliceId) > 1:
                idnum = int(sliceId[1])
            else:
                idnum = int(sliceId)

            def IdSetter(start,num):
                idvalue = num + 1
                if idvalue <= 9:
                    return f'{start}0{idvalue}'
                return f'{start}{idvalue}'
            
            finalID = IdSetter(idCode,idnum)
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
    def GET_Libuser(self,username,password):
        try:
            cur = self.connect.cursor()
            query = """select * from LIB where username = ?"""
            cur.execute(query,(username,))
            con = cur.fetchall()
            self.connect.commit()
            if len(con) == 0:
                return {"status":"username-err","data":[]}
            else:
                if con[0][3] == password:
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


# ========================================================================================

Alert = AlertUpdate()
database  = Database()
ReturnDate = ReturnDate()


def ZeroSetter(num):
    if num > 9:
        return str(num)
    else:
        return f'0{num}'

def TimeResult(timedata):
    day = timedata[0]
    months = ["Jan","Feb","Mar","Apr","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    dateday = ZeroSetter(int(timedata[2]))
    year = timedata[4]
    times = timedata[3]
    monthNumCode = ""
    for i in range(len(months)):
        if timedata[1] == months[i]:
            num = i+1
            monthNumCode = ZeroSetter(num)
            break
    return {"time":times,"date":f'{dateday}-{monthNumCode}-{year}',"day":day}
    
def ReturnBook(currentdate):
    try:
        if currentdate is not None:
            userId = session.get("userDetails")["userId"]
            bookData = database.GET_All("select * from STATUSBOOK_TABEL where user_id = {} and book_status = 1".format(userId))
            updateCon = database.UpdateCmd("""UPDATE STATUSBOOK_TABEL SET book_status = 0 WHERE user_id = ? AND return_data = ?""",data=(userId,currentdate))
            updateCount = database.UpdateCmd("""UPDATE STUDENT SET bookcount = ? where id = ?""",data=(len(bookData["data"]),userId))
    except Exception  as err:
        print("err",err)       

def ReviewIdReturn():
    reviewdata = database.GET_All("""select * from REVIEW""")["data"]
    final = ""
    if len(reviewdata) > 9:
        final = str(len(reviewdata)+1)
    else:
        final = f'0{str(len(reviewdata)+1)}'
    return f'REV{final}'


def SetCol(data):
    final = ""
    for key in data.keys():
        final += " "+key+" = ?"
    return final

def SetCountBookStatus():
    try:
        userId = database.GET_All("""select id from STUDENT""")["data"]
        for key in userId:
            data = database.GET_ALL_CONDITION("""select book_id from STATUSBOOK_TABEL where user_id = ? and book_status = 1""",(key[0],))["data"]
            count = len(data)
            setCount = database.UpdateCmd("""update STUDENT set bookcount = ? where id = ?""",(count,key[0]))           
    except Exception as err:
        print(err)

# App = Flask(__name__)
App.secret_key = "cool001"
App.config["SECRET_KEY"] = "supersecretkey"
App.config["BOOK_FOLDER"] = "./static/Books"
App.config["POSTER_FOLDER"] = "./static/assets/bookposter"
App.config["SECTION_IMG"] = "./static/assets/section-poster"

# start main page
@App.route('/')
def home():
    session['userlogin'] = False
    SetCountBookStatus()
    return render_template("loadMain.html")

@App.route('/startcheck',methods=["POST","GET"])
def startcheck():
    reqCon = request.form
    if reqCon["user-select"] == "Students/users":
        return redirect(url_for('Login'))
    return redirect(url_for('LibLogin'))

# userlogin 
@App.route('/login')
def Login():
    return render_template('userLogin.html',status = "good")

# user signup
@App.route('/signup')
def SignUp():
    return render_template('userSignup.html')


@App.route("/user/logout/")
def UserLogout():
    session['userlogin'] = False
    userobj = {"userId":"","username":""}
    session["userDetails"] = userobj 
    return render_template("userLogin.html",status = "good")


@App.route('/studentadd', methods = ["POST","GET"])
def AddPersonStudent():
    datavalueuser = request.form
    username = datavalueuser["user"]
    password = datavalueuser["pass"]
    email = datavalueuser["email"]
    database.addStudent(username=username,password=password,email=email)
    return redirect(url_for('Login'))

# userdashboard route 

@App.route('/userdash')
def UserHome():
    flag = session.get("userlogin")
    if flag == True:
        ReturnBook(TimeResult(time.ctime(time.time()).split(" "))["date"])
        book_data = database.GET_allBookSection()
        username = session.get("userDetails")["username"]
        bookCount = database.GET_ALL_CONDITION("""select * from STATUSBOOK_TABEL where user_id = ? and book_status = 1""",(str(session.get("userDetails")["userId"]),))["data"]
        return render_template('userHome.html',mainbookdata = book_data["data"],user = [username,len(bookCount)])
    return redirect(url_for("Login"))


@App.route("/user/Barrowed/")
def Barrowed():
    flag = session.get("userlogin")
    if flag == True:
        userId = session.get("userDetails")["userId"]
        data = database.BarrowedData(userid=userId,status=1)
        if data["status"] == "good" or data["status"] == "bad":
            return render_template("UserBarrow.html",barrowData = data["data"])
        else:
            return "err"
    else:
        return redirect(url_for("Login"))
    

@App.route("/user/barrow/bookread/", methods=["POST","GET"])
def readBook():
    try:
        userloginflag = session.get("userlogin")
        if userloginflag == True:
            BookId = request.args.get("id")
            bookData = database.GET_All(f'SELECT * FROM BOOKSTORE')
            finalData = []
            for i in bookData["data"]:
                if i[0] == BookId:
                    finalData.append(i)
                    break
            return render_template("BookRead.html",BookData = finalData)
        else:
            return redirect(url_for("Login"))
    except Exception as err:
        print(err)
        return "err"

@App.route("/user/Barrowed/return",methods=["POST","GET"])
def UserReturn():
    flag = session.get("userlogin")
    if flag == True:
        book_id = request.args.get("bookid")
        userid = session.get("userDetails")["userId"]
        bookReturn = database.UpdateCmd("""update STATUSBOOK_TABEL set book_status = 0 where book_id = ? and user_id = ? and book_status = 1""",(book_id,str(userid)))
        SetCountBookStatus()
        return redirect(url_for("Barrowed"))
    return redirect(url_for("Login"))

@App.route("/user/addcart/",methods=["POST","GET"])
def ADDBOOKCART():
    try:
        userloginflag = session.get("userlogin")
        if userloginflag == True: 
            bookdata = database.GET_All("SELECT * FROM STATUSBOOK_TABEL")
            userID = session.get("userDetails")["userId"]
            bookid = request.args.get("id")
            bookCount = database.GET_ALL_CONDITION("""select * from STATUSBOOK_TABEL where user_id = ? and book_status = 1""",(userID,))["data"]
            flag = False
            for i in bookdata["data"]:
                if i[0] == bookid and i[1] == str(userID) and i[4] == 1:
                    print("done")
                    flag = True
                    break
            if flag == False:
                issuedate = TimeResult(time.ctime(time.time()).split(" "))["date"]
                returndate = ReturnDate.setdate(issuedate)["returnDate"]
                bookstatus = 1
                if len(bookCount) < 5:
                    database.UpdateStudentBook(bookid=bookid,stdid=userID,issueData=issuedate,returnData=returndate,book_status=bookstatus)
                    return redirect(url_for("Barrowed"))
                else:
                    return redirect(url_for("Barrowed"))
            else:
                return redirect(url_for("Barrowed"))
        else:
            return redirect(url_for("Login"))
    except Exception as err:
        print(err)
        return "err"

@App.route("/user/View All/")
def ViewAll():
    userloginflag = session.get("userlogin")
    if userloginflag == True:
        book_data = database.GET_allBookSection()
        return render_template("bookViewAll.html",book=book_data["data"])
    else:
        return redirect(url_for("Login"))

@App.route('/login/check',methods=["POST","GET"])
def LoginValidation():
    con = request.form
    get_user = con["user"]
    get_pass = con["pass"]
    databaseResponse = database.GET_User(username=get_user,password=get_pass)
    if databaseResponse["status"] == "username-err":
        resp = make_response(render_template("userLogin.html",status = Alert.LoginStatus("user-err")))
        return resp
    elif databaseResponse["status"] == "password-err":
        resp = make_response(render_template("userLogin.html",status = Alert.LoginStatus("password-err")))
        return resp
    session['userlogin'] = True
    userobj = {"userId":databaseResponse["data"][0][0],"username":databaseResponse["data"][0][1],"email":databaseResponse["data"][0][3]}
    session["userDetails"] = userobj
    return  redirect(url_for("UserHome"))




@App.route("/bookdata/",methods=["POST","GET"])
def FindBook():
    userloginflag = session.get("userlogin")
    if userloginflag == True:
        paramId = request.args["id"]
        query = """select * from BOOKSTORE"""
        productData = database.GET_All(query=query)
        reviewData = database.GET_All(f'select * from REVIEW')
        # userDetails = session.get("userDetails")
        finalData = {"productdata":[],"review":[]}
        for i in productData["data"]:
            if i[0] == paramId:
                finalData["productdata"].append(i)
                break
        for i in reviewData["data"]:
            if i[1] == paramId:
                finalData["review"].append(i)
        if len(finalData["productdata"]) > 0:
            return render_template("BookProduct.html",Data = finalData["productdata"][0],review=finalData["review"])
        return "err"
    else:
        return redirect(url_for("Login"))
    
@App.route("/bookdata/review/",methods=["POST","GET"])
def UpdateReview():
    userloginflag = session.get("userlogin")
    if userloginflag == True:
        if request.method == "POST":
            detailCon = request.args
            reviewData = request.form
            userData = session.get("userDetails")
            dataQuery = (ReviewIdReturn(),detailCon.get("id"),userData["userId"],reviewData.get("rating-star"),reviewData.get("review"),TimeResult(time.ctime(time.time()).split(" "))["date"],userData["email"])
            updatestatus = database.UpdateCmd("""insert into REVIEW(review_id, book_id, user_id, rating, review, createDate, email) values(?, ?, ?, ?, ?, ?, ?)""",data=dataQuery)
            return redirect(url_for("FindBook",id=detailCon.get("id"),code="false"))
        return "err"
    else:
        return redirect(url_for("Login"))
    
@App.route('/user/returnbook/')
def returnBookpage():
    userloginflag = session.get("userlogin")
    if userloginflag == True:
        userId = session.get("userDetails")["userId"]
        returnbookdata = database.BarrowedData(userid=userId,status=0)
        return render_template("Userreturnbook.html",returndata = returnbookdata["data"])
    else:
        return redirect(url_for("Login"))
    


@App.route("/user/view All/search",methods=["POST","GET"])
def searchBook():
    
    userloginflag = session.get("userlogin")
    if userloginflag == True:
        usersearchValue = request.args["value"].lower()
        finalresult = []
        endfinal = {}
        bookData = database.GET_All("""select * from BOOKSTORE""")
        for value in bookData["data"]:
            if usersearchValue in value[1].lower():
                finalresult.append(value)
            elif usersearchValue in value[5].lower():
                finalresult.append(value)
            elif usersearchValue in value[3].lower():
                finalresult.append(value)
        for i in finalresult:
            endfinal[i[5]] = []
        for keys in endfinal.keys():
            for i in finalresult:
                if keys == i[5]:
                    endfinal[keys].append(i)
        return render_template("bookViewAll.html",book=endfinal)
    else:
        return redirect(url_for("Login"))
    


@App.route("/user/payment/",methods=["POST","GET"])
def userPaymentpage():
    userFlag = session.get("userlogin")
    if userFlag == True:
        payment = database.GET_All("""select * from PAYMENT""")["data"]
        bookId = request.args["id"]
        userId = session.get("userDetails")["userId"]
        currentdate = TimeResult(time.ctime(time.time()).split(" "))["date"]
        finalId = len(payment) + 1   
        status = "success"
        pay = database.UpdateCmd("""insert into PAYMENT(payid, bookid, userid, paydate, paystatus) values (?, ?, ?, ?, ?)""",(finalId,bookId,userId,currentdate,status))
        if pay["status"] == "done":
            return redirect(url_for("FindBook",id=bookId))
    return redirect(url_for("Login"))
    
@App.route("/user/book-download/")
def ViewDownload():
    try:
        userFlag = session.get("userlogin")
        if userFlag == True:
            userId = session.get("userDetails")["userId"]
            payment = database.GET_ALL_CONDITION("""select * from PAYMENT where userid = ?""",(userId,))
            finalresult = {}
            for i in payment["data"]:
                finalresult[i[1]] = []
            for key in finalresult.keys():
                data = database.GET_ALL_CONDITION("""select * from BOOKSTORE where bookid = ?""",(key,))
                if data["status"] == "good":
                    finalresult[key].append(data["data"][0])
            return render_template("Payment.html",datas = finalresult)
        else:
            return redirect(url_for("Login"))
    except Exception as err:
        return str(err)
    



# ======================================== lib account =========================================== #

# lib user login
@App.route("/LibLogin")
def LibLogin():
    return render_template("LibLogin.html",status = "good")
@App.route("/lib/logout")
def LibLogout():
    session['liblogin'] = False
    userobj = {"userId":"","username":"","email":""}
    session["LibDetails"] = userobj
    return redirect(url_for("LibLogin"))

# @App.route('/libSignup')
# def LibSignup():
#     return render_template('LibSignup.html')

# @App.route('/Addlibuser',methods=["POST","GET"])
# def ADD_Newuser():
#     clientdata = request.form
#     username = clientdata["usernamelib"]
#     email = clientdata["emaillib"]
#     password = clientdata["passwordlib"]
#     status = database.SET_newlib(username=username,email=email,password=password)
#     if status["status"] == "username_exists":
#         return redirect(url_for("LibSignup",mes=status["status"]))
#     elif status["status"] == "err":
#         return redirect(url_for("LibSignup",mes=status["status"]))
#     return redirect(url_for("LibLogin"))

@App.route('/lib/dashlib')
def dashlib():
    liblogin = session.get("liblogin")
    if liblogin == True:
        SetCountBookStatus()
        timer = TimeResult(time.ctime(time.time()).split(" "))
        membersData = database.get_Studentdata()
        book_data = database.GETSECTION()["data"]
        return render_template("Libdashboard.html",timerData = timer,mem=membersData,book = book_data)
    return redirect(url_for("LibLogin"))


@App.route('/lib/Addbook/')
def Addbook():
    liblogin = session.get("liblogin")
    if liblogin == True:
        return render_template("Addbook.html")
    return redirect(url_for("LibLogin"))

@App.route('/lib/addbook/newbook',methods=["POST","GET"])
def AddbookSet():
    liblogin = session.get("liblogin")
    if liblogin == True:
        if request.method == "POST":
            bookDetails = request.form
            poster = request.files["poster"]
            bookPdf = request.files["file-pdf"]
            bookname = bookDetails.get("book-name")
            authorName = bookDetails.get("book-author")
            bookGener = bookDetails.get("book-gener")
            pulishedDate = bookDetails.get("book-date")
            if poster.filename == None or bookPdf.filename == None or bookname == '' or bookGener == '' or authorName == '' or pulishedDate == '':
                return redirect(url_for("Addbook"))
            bookPath = f'./Books/{bookPdf.filename}'
            posterPath = f'./assets/bookposter/{poster.filename}'
            dataSENT = [bookname,bookPath,authorName,posterPath,bookGener,pulishedDate]
            response = database.InsertBooks(dataSENT)
            if response["status"] == "upload":
                poster.save(f'{App.config["POSTER_FOLDER"]}/{secure_filename(poster.filename)}')
                bookPdf.save(f'{App.config["BOOK_FOLDER"]}/{secure_filename(bookPdf.filename)}')
                return render_template("SuccessUpload.html",bookdatas = [1,posterPath,bookname])
            else:
                return render_template("SuccessUpload.html",bookdatas = [0,posterPath,bookname])
    return redirect(url_for("LibLogin"))

@App.route('/lib/members/')
def Viewmembers():
    liblogin = session.get("liblogin")
    if liblogin == True:
        membersData = database.get_Studentdata()
        return render_template("Memberspage.html", data = membersData)
    return redirect(url_for("LibLogin"))


@App.route('/lib/add-sec/',methods=["POST","GET"])
def AddSection():
    try:
        liblogin = session.get("liblogin")
        if liblogin == True:
            if request.method == "POST":
                imgSRC = request.files["imgsec"]
                SectionName = request.form.get("namesec")
                desSection = request.form.get("decsec")
                if SectionName == "" and secure_filename(imgSRC.filename) == "":
                    return redirect(url_for("dashlib"))
                SECDATA = database.GET_All("""select * from SECTIONTYPE""")["data"]
                count = len(SECDATA)+1
                SECID = f'SEC{ZeroSetter(count)}'
                ImgPath = f'./assets/section-poster/{secure_filename(imgSRC.filename)}'
                currentDate = TimeResult(time.ctime(time.time()).split(" "))
                result = database.InsertSection(id=SECID,section_name=SectionName,date=currentDate["date"],des=desSection,imgpath=ImgPath)
                imgSRC.save(f'{App.config["SECTION_IMG"]}/{secure_filename(imgSRC.filename)}')
                return redirect(url_for("dashlib"))
        return redirect(url_for("LibLogin"))
    
    except Exception as err:
        print(err)
        return f' Error is  {err}'

@App.route('/libloginvalidation/',methods=["POST","GET"])
def LibUserValidation():
    con = request.form
    get_user = con["user"]
    get_pass = con["pass"]
    databaseResponse = database.GET_Libuser(username=get_user,password=get_pass)
    if databaseResponse["status"] == "username-err":
        resp = make_response(render_template("LibLogin.html",status = Alert.LoginStatus("user-err")))
        return resp
    elif databaseResponse["status"] == "password-err":
        resp = make_response(render_template("LibLogin.html",status = Alert.LoginStatus("password-err")))
        return resp
    session['liblogin'] = True
    userobj = {"userId":databaseResponse["data"][0][0],"username":databaseResponse["data"][0][1],"email":databaseResponse["data"][0][2]}
    session["LibDetails"] = userobj
    return  redirect(url_for("dashlib"))

@App.route("/lib/userview/",methods=["POST","GET"])
def userViewer():
    liblogin = session.get("liblogin")
    if liblogin == True:
        SetCountBookStatus()
        username = request.args.get("id")
        userid = request.args.get("code")
        if username and userid:
            userdata = database.GET_ALL_CONDITION("""select id, username, email,bookcount from STUDENT where id = ? and username = ?""",datas=(userid,username))
            bookdata = database.GET_ALL_CONDITION("""select * from STATUSBOOK_TABEL where user_id = ?""",datas=(userid))
            userReview = database.GET_ALL_CONDITION("""select * from REVIEW where user_id = ?""",(userid,))["data"]
            bookId = [tuple(i[0] for i in bookdata["data"])]
            bookDetail = None
            if len(bookId[0]) > 1:
                bookDetail = database.GET_All("select * from BOOKSTORE where bookid in {}".format(bookId[0]))["data"]
            elif len(bookId[0]) == 1:
                bookDetail = database.GET_ALL_CONDITION(f'select * from BOOKSTORE where bookid = ?',datas=(bookId[0]))["data"]
            else:
                bookDetail = []
            fulldata = {"user":userdata["data"],"book":bookdata["data"],"bookdetail":bookDetail,"review":userReview}
            return render_template("userView.html",detail = fulldata)
        else:
            return "sorry"
    return redirect(url_for("LibLogin"))

@App.route("/lib/View All/")
def LibViewAll():
    liblogin = session.get("liblogin")
    if liblogin == True:
        book_data = database.GET_allBookSection()
        return render_template("LibBooks.html",book=book_data["data"])
    return redirect(url_for("LibLogin"))


# lib remove user #
@App.route("/lib/userbook/remove/",methods=["POST","GET"])
def userbookremove():
    liblogin = session.get("liblogin")
    if liblogin == True:
        querydata = request.args
        query = """update STATUSBOOK_TABEL set book_status = 0 where book_id = ? and user_id = ? and issue_data = ? and return_data = ? and book_status = 1"""
        dataUpdate = database.UpdateCmd(query=query,data=(querydata.get("bookid"),querydata.get("id"),querydata.get("issD"),querydata.get("retD")))
        if dataUpdate["status"] == "done":
            username = database.GET_ALL_CONDITION("""select username from STUDENT where id = ?""",(querydata.get("id"),))["data"]
            lenBookCount = database.GET_ALL_CONDITION("""select book_id from STATUSBOOK_TABEL where user_id = ? and book_status = 1""",(querydata.get("id"),))["data"]
            userUpdate = database.UpdateCmd("""update STUDENT set bookcount = ? where id = ?""",(len(lenBookCount),querydata.get("id")))
            return redirect(url_for("userViewer",id=username[0][0],code=querydata.get("id")))
        return "err"
    return redirect(url_for("LibLogin"))

@App.route("/lib/sectionupdate/",methods=["POST","GET"])
def SectionUpdate():
    liblogin = session.get("liblogin")
    if liblogin == True:
        if request.method == "POST":
            uservalue = request.form
            userImg = request.files.get("poster")
            flagUpdate = False
            finaldata = {}
            old_Title = database.GET_ALL_CONDITION("""select st.sec_name from SECTIONTYPE as st where st.sec_id = ?""",(uservalue["id"],))["data"]
            for keyvalue in uservalue.keys():
                if uservalue[keyvalue] != "":
                    if keyvalue == "title":
                        finaldata["sec_name"] = uservalue[keyvalue]
                        flagUpdate = True
                    elif keyvalue == "des":
                        finaldata["description"] = uservalue[keyvalue]
                        flagUpdate = True
            if flagUpdate == True:
                query =  """update SECTIONTYPE set {} where sec_id = ?""".format(SetCol(finaldata))
                finaldata["sec_id"] = uservalue["id"]
                tupleData = [tuple(key for value,key in finaldata.items())]
                stautsUpdates = database.UpdateCmd(query=query,data=tupleData[0])
                if stautsUpdates["status"] == "done":
                    updateTitleBook = database.UpdateCmd("""update BOOKSTORE set section = ? where section = ?""",(finaldata["sec_name"],old_Title[0][0]))
            if secure_filename(userImg.filename) != "":
                imgpath = f'./assets/section-poster/{secure_filename(userImg.filename)}'
                imageUpdateQuery = f'update SECTION_IMAGE set value_src = ? where id = ?'
                deletepath = f'{App.config["SECTION_IMG"]}/{uservalue["old_src"]}'
                if os.path.isfile(deletepath):
                    status = database.UpdateCmd(imageUpdateQuery,(imgpath,uservalue["id"]))
                    if status["status"] == "done":
                        os.remove(deletepath)
                        userImg.save(f'{App.config["SECTION_IMG"]}/{secure_filename(userImg.filename)}')
                        return redirect(url_for("dashlib"))
                else:
                    status = database.UpdateCmd(imageUpdateQuery,(imgpath,uservalue["id"]))
                    if status["status"] == "done":
                        userImg.save(f'{App.config["SECTION_IMG"]}/{secure_filename(userImg.filename)}')
                        return redirect(url_for("dashlib"))
                    
            return redirect(url_for("dashlib"))
        
        return "err"
    return redirect(url_for("LibLogin"))

@App.route("/lib/deletesection/", methods=["POST","GET"])
def DeleteSection():
    try:
        liblogin = session.get("liblogin")
        if liblogin == True:
            SectionId = request.args.get("id")
            SectionName = database.GET_ALL_CONDITION("""select sec_name from SECTIONTYPE where sec_id = ?""",(SectionId,))["data"][0][0]
            bookIds = database.GET_ALL_CONDITION("""select bookid from BOOKSTORE where section = ?""",(SectionName,))["data"]
            userIds = []
            userBookCount = {}
            SectionPathPoster = database.GET_ALL_CONDITION("""select value_src from SECTION_IMAGE where id = ?""",(SectionId,))["data"][0][0].split("/")[-1]
            # removing book related to section name 
            for bookids in bookIds:
                getpathsPdf = database.GET_ALL_CONDITION("""select bookpath,bookposterpath  from BOOKSTORE where bookid = ?""",(bookids[0],))
                database.UpdateCmd("""delete from BOOKSTORE where bookid = ?""",(bookids[0],))
                for paths in getpathsPdf["data"]:
                    # App.config["BOOK_FOLDER"] = "./static/Books"
                    # App.config["POSTER_FOLDER"] = "./static/assets/bookposter"
                    if os.path.isfile(f'./static/{paths[0]}') and os.path.isfile(f'./static/{paths[1]}'):
                        os.remove(f'./static/{paths[0]}')  
                        os.remove(f'./static/{paths[1]}')
                database.UpdateCmd("""delete from Review where book_id = ?""",(bookids[0],))
                database.UpdateCmd("""delete from STATUSBOOK_TABEL where book_id = ?""",(bookids[0],))
                database.UpdateCmd("""delete from SECTION_BOOK where book_id = ?""",(bookids[0],))
                getuserId = database.GET_ALL_CONDITION("""select user_id from STATUSBOOK_TABEL where book_id = ?""",(bookids[0],))
                for userid in getuserId["data"]:
                    if userid[0] not in userIds:
                        userIds.append(userid[0])
            database.UpdateCmd("""delete from SECTION_IMAGE where id = ?""",(SectionId,)) 
            if os.path.isfile(f'{App.config["SECTION_IMG"]}/{SectionPathPoster}'):
                os.remove(f'{App.config["SECTION_IMG"]}/{SectionPathPoster}')
            database.UpdateCmd("""delete from SECTIONTYPE where sec_id = ?""",(SectionId,))
            for i in userIds:
                bookcount = database.GET_ALL_CONDITION("""select book_id from STATUSBOOK_TABEL where user_id = ? and book_status = 1""",(i,))
                updateCount = database.UpdateCmd("""UPDATE STUDENT SET bookcount = ? where id = ?""",(len(bookcount["data"]),i))
            return redirect(url_for("dashlib"))
        return redirect(url_for("LibLogin"))
    except Exception as err:
        print(err)
        return "err"
    

@App.route("/lib/members/remove/", methods=["POST","GET"])
def userremove():
    liblogin = session.get("liblogin")
    if liblogin == True:
        userId = request.args["id"]
        database.UpdateCmd("""delete from STUDENT where id = ?""",(userId,))
        database.UpdateCmd("""delete from REVIEW where user_id = ?""",(userId,))
        database.UpdateCmd("""delete from STATUSBOOK_TABEL where user_id = ?""",(userId,))
        return redirect(url_for("Viewmembers"))
    return redirect(url_for("LibLogin"))

@App.route("/lib/view All/search")
def searchLiB():
    liblogin = session.get("liblogin")
    if liblogin == True:
        usersearchValue = request.args["value"].lower()
        finalresult = []
        endfinal = {}
        bookData = database.GET_All("""select * from BOOKSTORE""")
        for value in bookData["data"]:
            if usersearchValue in value[1].lower():
                finalresult.append(value)
            elif usersearchValue in value[5].lower():
                finalresult.append(value)
            elif usersearchValue in value[3].lower():
                finalresult.append(value)
            for i in finalresult:
                endfinal[i[5]] = []
        for keys in endfinal.keys():
            for i in finalresult:
                if keys == i[5]:
                    endfinal[keys].append(i)
        return render_template("LibBooks.html",book=endfinal)
    return redirect(url_for("LibLogin"))


@App.route("/lib/book/delete",methods=["POST","GET"])
def DeleteBook():
    information = request.args
    book_id = information.get("id")
    section = information.get("section")
    booktitle = information.get("title")
    bookdetails = database.GET_ALL_CONDITION("""select * from BOOKSTORE where bookid = ?""",(book_id,))["data"]
    posterPath = f'{App.config["POSTER_FOLDER"]}/{bookdetails[0][4].split("/")[-1]}'
    bookPdfPath = f'{App.config["BOOK_FOLDER"]}/{bookdetails[0][2].split("/")[-1]}'
    bookRemove = database.UpdateCmd("""delete from BOOKSTORE where bookid = ? """,(book_id,))
    if bookRemove["status"] == "done":
        if os.path.isfile(posterPath) and os.path.isfile(bookPdfPath):
            os.remove(posterPath)
            os.remove(bookPdfPath)
    paymentBook = database.UpdateCmd("""delete from PAYMENT where bookid = ?""",(book_id,))
    reviewBook = database.UpdateCmd("""delete from REVIEW where book_id = ?""",(book_id,))
    sectionBook = database.UpdateCmd("""delete from SECTION_BOOK where book_id = ?""",(book_id,))
    statusbook = database.UpdateCmd("""delete from STATUSBOOK_TABEL where book_id = ?""",(book_id,))
    SetCountBookStatus()
    return redirect(url_for("LibViewAll"))



    

