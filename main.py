from typing import List
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from fastapi import FastAPI
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)


# //////////////////////Create Tables Data Base//////////////////////////#
# //////////////////////Create Tables Data Base//////////////////////////#
# //////////////////////Create Tables Data Base//////////////////////////#

db = sqlite3.connect("TestSystem.db")
cr = db.cursor()

cr.execute("""CREATE TABLE if not exists "Users" (
	"id"	INTEGER NOT NULL UNIQUE,
	"fullName"	TEXT NOT NULL,
	"userName"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	"state"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);""")

cr.execute("""CREATE TABLE if not exists "Courses" (
	"id"	INTEGER NOT NULL UNIQUE,
	"courseName"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);""")

cr.execute("""CREATE TABLE if not exists "Questions" (
	"id"	INTEGER NOT NULL UNIQUE,
	"question"	TEXT NOT NULL,
	"answer1"	TEXT NOT NULL,
	"answer2"	TEXT NOT NULL,
	"answer3"	BLOB NOT NULL,
	"answer4"	REAL NOT NULL,
	"trueAnswer"	TEXT NOT NULL,
	"courseId"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);""")

cr.execute("""CREATE TABLE if not exists "UserAnswers" (
	"id"	INTEGER NOT NULL UNIQUE,
	"userAnswer"	TEXT NOT NULL,
	"userId"	INTEGER NOT NULL,
	"questionId"	INTEGER NOT NULL,
	"courseId"	INTEGER,
	"stateAnswer"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);""")


cr.execute("""CREATE TABLE if not exists "UserCourses" (
	"id"	INTEGER NOT NULL UNIQUE,
	"userId"	INTEGER NOT NULL,
	"courseId"	INTEGER NOT NULL,
	"countTrue"	INTEGER,
	"countFalse"	INTEGER,
	"average"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
);""")

db.commit()
db.close()


# //////////////////////CRUD Tables//////////////////////////#
# //////////////////////CRUD Tables//////////////////////////#
# //////////////////////CRUD Tables//////////////////////////#


#-------------------Questions-------------------#
@app.get("/getQuestions")
def getQuestions():
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute("select * from Questions")
    lst = cur.fetchall()
    con.close()
    lst_json = []
    for i in lst:
        items = {}
        items["id"] = i[0]
        items["question"] = i[1]
        items["answer1"] = i[2]
        items["answer2"] = i[3]
        items["answer3"] = i[4]
        items["answer4"] = i[5]
        items["trueAnswer"] = i[6]
        items["courseId"] = i[7]
        lst_json.append(items)
    return lst_json


@app.post("/deleteQuestion")
def deleteQuestion(id):
    id = int(id)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"delete from Questions where id={id}")
    con.commit()
    con.close()
    return {"status": "success"}


@app.get("/addQuestion")
def addQuestion(qn, ans1, ans2, ans3, ans4, ta, cid):
    cid = int(cid)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"""insert into Questions(question,answer1,answer2,answer3,answer4,trueAnswer,courseId)
                	values("{qn}","{ans1}","{ans2}","{ans3}","{ans4}","{ta}",{cid})""")
    con.commit()
    con.close()
    return {"status": "success"}


@app.get("/updateQuestion")
def updateQuestion(id, qn, ans1, ans2, ans3, ans4, ta, cid):
    id = int(id)
    cid = int(cid)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"""update Questions set question='{qn}',answer1='{ans1}',answer2='{ans2}',
                    answer3='{ans3}',answer4='{ans4}',trueAnswer='{ta}',courseId={cid} where id={id}""")
    con.commit()
    con.close()
    return {"status": "success"}


#-------------------Courses-------------------#
@app.get("/getCourses")
def getCourses():
    con = sqlite3.connect("TestSystem.db")
    sql = "select * from Courses"
    cur = con.execute(sql)
    lst = cur.fetchall()
    con.close()
    lst_json = []
    for i in lst:
        items = {}
        items["id"] = i[0]
        items["courseName"] = i[1]
        lst_json.append(items)
    return lst_json


@app.post("/deleteCourse")
def deleteCourse(id):
    id = int(id)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"delete from Courses where id={id}")
    con.commit()
    con.close()
    return {"success": "success"}


@app.get("/addCourse")
def addCourse(cn):
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"""insert into Courses(courseName)
                	values("{cn}")""")
    con.commit()
    con.close()
    return {"status": "success"}


@app.get("/updateCourse")
def updateCourse(id, cn):
    id = int(id)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(
        f"""update Courses set courseName='{cn}' where id={id}""")
    con.commit()
    con.close()
    return {"status": "success"}


#-------------------Users-------------------#
@app.get("/getUsers")
def getUsers():
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute("select * from Users")
    lst = cur.fetchall()
    con.close()
    lst_json = []
    for i in lst:
        items = {}
        items["id"] = i[0]
        items["fullName"] = i[1]
        items["userName"] = i[2]
        items["password"] = i[3]
        items["state"] = i[4]
        lst_json.append(items)
    return lst_json


@app.post("/deleteUser")
def deleteUser(id):
    id = int(id)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"delete from Users where id={id}")
    con.commit()
    con.close()
    return {"status": "success"}


@app.get("/addUser")
def addUser(fn, un, pw, st):
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"""insert into Users(fullName,userName,password,state)
                	values("{fn}","{un}","{pw}","{st}")""")
    con.commit()
    con.close()
    return {"status": "success"}


@app.get("/updateUser")
def updateUser(id, fn, un, pw, st):
    id = int(id)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"""update Users set fullName='{fn}',userName='{un}',password='{pw}',
                    state='{st}' where id={id}""")
    con.commit()
    con.close()
    return {"status": "success"}


#-------------------UserAnswers-------------------#
@app.get("/getUserAnswers")
def getUserAnswers():
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute("select * from UserAnswers")
    lst = cur.fetchall()
    con.close()
    lst_json = []
    for i in lst:
        items = {}
        items["id"] = i[0]
        items["userAnswer"] = i[1]
        items["userId"] = i[2]
        items["questionId"] = i[3]
        items["courseId"] = i[4]
        items["stateAnswer"] = i[5]
        lst_json.append(items)
    return lst_json


@app.post("/deleteUserAnswer")
def deleteUserAnswer(id):
    id = int(id)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"delete from UserAnswers where id={id}")
    con.commit()
    con.close()
    return {"status": "success"}


@app.get("/addUserAnswer")
def addUserAnswer(ua, uid, qid, cid, sa):
    uid = int(uid)
    qid = int(qid)
    cid = int(cid)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"""insert into UserAnswers(userAnswer,userId,questionId,courseId,stateAnswer)
                	values("{ua}",{uid},{qid},{cid},"{sa}")""")
    con.commit()
    con.close()
    return {"status": "success"}


@app.get("/updateUserAnswer")
def updateUserAnswer(id, ua, uid, qid, cid, sa):
    id = int(id)
    uid = int(uid)
    qid = int(qid)
    cid = int(cid)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"""update UserAnswers set userAnswer='{ua}',userId={uid},questionId={qid},courseId={cid},
                    stateAnswer='{sa}' where id={id}""")
    con.commit()
    con.close()
    return {"status": "success"}


#-------------------UserCourses-------------------#
@app.get("/getUserCourses")
def getUserCourses():
    con = sqlite3.connect("TestSystem.db")
    sql = "select * from UserCourses"
    cur = con.execute(sql)
    lst = cur.fetchall()
    con.close()
    lst_json = []
    for i in lst:
        items = {}
        items["id"] = i[0]
        items["userId"] = i[1]
        items["courseId"] = i[2]
        items["countTrue"] = i[3]
        items["countFalse"] = i[4]
        items["average"] = i[5]
        lst_json.append(items)
    return lst_json


@app.post("/deleteUserCourses")
def deleteUserCourses(id):
    id = int(id)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"delete from UserCourses where id={id}")
    con.commit()
    con.close()
    return {"success": "success"}


@app.get("/addUserCourses")
def addUserCourses(uid, cid):
    uid = int(uid)
    cid = int(cid)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"""insert into UserCourses(userId,courseId)
                	values({uid},{cid})""")
    con.commit()
    con.close()
    return {"status": "success"}


@app.get("/updateUserCourses")
def updateUserCourses(id, uid, cid):
    id = int(id)
    uid = int(uid)
    cid = int(cid)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(
        f"""update UserCourses set userId={uid},courseId={cid} where id={id}""")
    con.commit()
    con.close()
    return {"status": "success"}


# //////////////////////Functions//////////////////////////#

# //////////////////////Functions//////////////////////////#

# //////////////////////Functions//////////////////////////#

#---------#  Check Account  #---------#
@app.get("/checkAccount")
def checkAccount(un, pw):
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(
        f"select * from Users where userName='{un}' and password='{pw}'")
    lst = cur.fetchone()
    con.close()

    if lst[0][4] == "user":
        return "user"
    elif lst[0][4] == "admin":
        return "admin"
    return "false"


#---------#  Get Student Questions  #---------#
@app.get("/getStudentQuestions")
def getQuestions(courseId):
    id = int(courseId)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"""select * from Questions where courseId={courseId}""")
    lst = cur.fetchall()
    con.close()
    lst_json = []
    for i in lst:
        items = {}
        items["id"] = i[0]
        items["question"] = i[1]
        items["answer1"] = i[2]
        items["answer2"] = i[3]
        items["answer3"] = i[4]
        items["answer4"] = i[5]
        items["trueAnswer"] = i[6]
        items["courseId"] = i[7]
        lst_json.append(items)
    return lst_json


# @app.get("/getQuestionsCourse")
# def getQuestionsCourse(courseId):
#     courseId = int(courseId)
#     con = sqlite3.connect("TestSystem.db")
#     cur = con.execute(f"select * from Questions where courseId={courseId}")
#     lst = cur.fetchall()
#     con.close()
#     lst_json = []
#     for i in lst:
#         items = {}
#         items["id"] = i[0]
#         items["question"] = i[1]
#         items["answer1"] = i[2]
#         items["answer2"] = i[3]
#         items["answer3"] = i[4]
#         items["answer4"] = i[5]
#         items["trueAnswer"] = i[6]
#         items["courseId"] = i[7]
#         lst_json.append(items)
#     return lst_json

#---------#  Get User Courses By UserId  #---------#
@app.get("/getUserCoursesById")
def getUserCoursesById(userId):
    userId = int(userId)
    con = sqlite3.connect("TestSystem.db")
    sql = f"select * from UserCourses where userId={userId}"
    cur = con.execute(sql)
    lstUC = cur.fetchall()
    IDs = ""
    for i in lstUC:
        IDs += f"{i[2]},"
    IDs = IDs.strip(",")
    sql = f"select * from Courses where id in({IDs})"
    cur = con.execute(sql)
    lstC = cur.fetchall()
    con.close()
    lst_json = []
    for i in lstC:
        items = {}
        items["id"] = i[0]
        items["courseName"] = i[1]
        lst_json.append(items)
    return lst_json


#---------#  Get Name User  #---------#
@app.get("/getNameUser")
def getNameUser(id):
    id = int(id)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"select fullName from Users where id={id}")
    lst = cur.fetchone()
    con.close()
    print(lst[0])
    fullName = f"{lst[0]}"
    return fullName


#---------#  Get Name Course  #---------#
@app.get("/getNameCourse")
def getNameCourse(id):
    id = int(id)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"select courseName from Courses where id={id}")
    lst = cur.fetchone()
    con.close()
    courseName = f"{lst[0]}"
    return courseName


#---------#  Update User Course Results  #---------#
@app.get("/updateUserCourseResult")
def updateUserCourseResult(uid, cid):
    uid = int(uid)
    cid = int(cid)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(
        f"select * from UserAnswers where userId={uid} and courseId={cid} ")
    lst = cur.fetchall()
    ct = 0
    cf = 0
    for i in lst:
        if i[5] == "true":
            ct += 1
        if i[5] == "false":
            cf += 1

    avg = round(((ct/len(lst))*100), 2)

    cur = con.execute(
        f"""update UserCourses set countTrue={ct},countFalse={cf},average={avg} where userId={uid} and courseId={cid} """)
    con.commit()
    con.close()
    return {"status": "success"}


#---------#  Get User Course   #---------#
@app.get("/getUserCourse")
def getUserCourse(uid, cid):
    uid = int(uid)
    cid = int(cid)
    con = sqlite3.connect("TestSystem.db")
    sql = f"select * from UserCourses where userId={uid} and courseId={cid}"
    cur = con.execute(sql)
    lst = cur.fetchall()
    con.close()
    lst_json = []
    for i in lst:
        items = {}
        items["id"] = i[0]
        items["userId"] = i[1]
        items["courseId"] = i[2]
        items["countTrue"] = i[3]
        items["countFalse"] = i[4]
        items["average"] = i[5]
        lst_json.append(items)
    return lst_json


#-------------------checkCompleteCourse-------------------#
@app.get("/checkCompleteCourse")
def checkCompleteCourse(uid, cid):
    uid = int(uid)
    cid = int(cid)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(
        f"select * from UserAnswers where userId={uid} and courseId={cid}")
    lst = cur.fetchall()
    con.close()
    if len(lst) == 0:
        return False
    else:
        return True


#---------#  Get Data Result  #---------#
@app.get("/getDataResult")
def getDataResult(userId,courseId):
    userId = int(userId)
    courseId = int(courseId)
    con = sqlite3.connect("TestSystem.db")
    cur = con.execute(f"""select q.id,q.question,q.trueAnswer,ua.userAnswer,ua.stateAnswer from Questions q inner join UserAnswers ua
                      where (q.id=ua.questionId) and (ua.userId={userId} and ua.courseId={courseId}) """)
    lst = cur.fetchall()
    con.close()
    lst_json = []
    for i in lst:
        items = {}
        items["id"] = i[0]
        items["question"] = i[1]
        items["trueAnswer"] = i[2]
        items["userAnswer"] = i[3]
        items["stateAnswer"] = i[4]
        lst_json.append(items)
    return lst_json