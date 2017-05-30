from flask import Flask, flash, redirect, render_template, \
     request, url_for, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
import json
import os
from settings import APP_STATIC_JSON
from random import shuffle
import cgi

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:veda1997@localhost/GCT'
db = SQLAlchemy(app)

e1_start=801;e1_end=809;e2_start=1201;e2_end=1208;e3_start=1601;e3_end=1701;
e4_start=1701;e4_end=1702;
global status
global errortype

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    emailid = db.Column(db.String(180), unique=True)
    pin = db.Column(db.String(80))
    testctime = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, pin, emailid):
        self.name = name
        self.pin = pin
        self.emailid = emailid

class UserAudio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80))
    blob1 = db.Column(db.LargeBinary)
    time = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, user, blob1):
        self.user = user
        self.blob1 = blob1

class DataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(180))
    blob = db.Column(db.LargeBinary)

    def __init__(self, url, blob):
        self.url = url
        self.blob = blob 

class userDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email=db.Column(db.String(120), unique=True)
    phno = db.Column(db.String(120))
    rollno = db.Column(db.String(120))
    learningcenter = db.Column(db.String(120))

    def __init__(self, name, email, phno, rollno, learningcenter):
        self.name = name 
        self.email = email 
        self.phno = phno 
        self.rollno = rollno 
        self.learningcenter = learningcenter 

class TestDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(120))
    test= db.Column(db.Boolean())
    teststime=db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    delays=db.Column(db.Float())
    testend= db.Column(db.Boolean())
    lastPing = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    score = db.Column(db.Integer())
    learningcenter = db.Column(db.String(120))

    def __init__(self, **kwargs):
        super(TestDetails, self).__init__(**kwargs)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    emailid = db.Column(db.String(180))
    pin = db.Column(db.String(80))
    testctime = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    submittedans = db.Column(db.Text)
    responsetime = db.Column(db.Float)
    q_score = db.Column(db.Integer)
    q_status = db.Column(db.String(120))
    time = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow )
    currentQuestion=db.Column(db.String(120))
    serialno=db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Response, self).__init__(**kwargs)

class Randomize(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1=db.Column(db.String(120))
    serialno=db.Column(db.Integer)
    qno=db.Column(db.String(120))

    def __init__(self, user1, serialno, qno):
        self.user1 = user1 
        self.serialno = serialno 
        self.qno = qno 

class EssayTypeResponse(db.Model):
    """Sub model for storing user response for essay type questions"""
    id = db.Column(db.Integer, primary_key=True)
    useremailid = db.Column(db.String(120))
    qid = db.Column(db.String(120))
    ansText = db.Column(db.Text)
    qattemptedtime = db.Column(db.Float)

    def __init__(self, useremailid, qid, ansText, qattemptedtime):
        self.useremailid = useremailid 
        self.qid = qid 
        self.ansText = ansText 
        self.qattemptedtime = qattemptedtime 

def getQuestionPaper(qid_list):
    path = 'QP_template.json'
    json_temp=json.loads(open(os.path.join(APP_STATIC_JSON,path)).read())
    #print qid_list
    i=0;j=0;k=0;l=0;m=0;n=0;p=0;q=0;r=0;s=0;t=0
    for qid in qid_list:
        qid=int(qid)
        if qid in range(e1_start,e1_end):
              e1_readjson=json.loads(open(os.path.join(APP_STATIC_JSON,'E1-Reading.json')).read())
              for key in e1_readjson["passageArray"]:
                    for qn in key["questions"]:
                          pid=qn["id"]
                          if int(pid) == qid:
                                json_temp["section"][1]["subsection"][0]["passage"]=key["passage"]
                                json_temp["section"][1]["subsection"][0]["questions"].append(qn)
                                json_temp["section"][1]["subsection"][0]["questions"][m]["serialno"] = qid_list[qid]
                                m +=1
        if qid in range(e2_start,e2_end):
              e2_lsnjson=json.loads(open(os.path.join(APP_STATIC_JSON,'E2-Listening.json')).read())
              for key in e2_lsnjson["videoArray"]:
                    for qn in key["questions"]:
                          pid=qn["id"]
                          if int(pid) == qid:
                                json_temp["section"][0]["subsection"][0]["link"]=key["link"]
                                json_temp["section"][0]["subsection"][0]["questions"].append(qn)
                                json_temp["section"][0]["subsection"][0]["questions"][n]["serialno"] = qid_list[qid]
                                n +=1
        if qid in range(e3_start,e3_end):
              e3_spkjson=json.loads(open(os.path.join(APP_STATIC_JSON,'E3-Speaking.json')).read())
              for key in e3_spkjson["questions"]:
                    if int(key["id"]) == qid:
                          json_temp["section"][0]["subsection"][1]["questions"].append(key)
                          json_temp["section"][0]["subsection"][1]["questions"][p]["serialno"] = qid_list[qid]
                          p += 1
        if qid in range(e4_start,e4_end):
              e4_wrtjson=json.loads(open(os.path.join(APP_STATIC_JSON,'E4-Writing.json')).read())
              for key in e4_wrtjson["questions"]:
                    if int(key["id"]) == qid:
                          json_temp["section"][1]["subsection"][1]["questions"].append(key)
                          json_temp["section"][1]["subsection"][1]["questions"][q]["serialno"] = qid_list[qid]
                          q += 1
    return json_temp

def generateQuestionPaper():
    path = 'QP_template.json'
    json_temp=json.loads(open(os.path.join(APP_STATIC_JSON,path)).read())
    for key in json_temp:
        if  key == "section":
            section=json_temp[key]
            for s in section:
                for key in s:
                    if key == "subsection":
                        for subs in s[key]:
                            cnt=int(subs["count"])
                            name=subs["name"]
                            types=subs["types"]
                            #print name
                            if name == "E2-Listening":
                                #print name
                                json_subs=json.loads(open(os.path.join(APP_STATIC_JSON,name+".json")).read())
                                video_list=json_subs["videoArray"]
                                serialno=range(0,len(video_list))
                                shuffle(serialno)
                                subs["link"]=video_list[serialno[0]]["link"]
                                subs["questions"]=video_list[serialno[0]]["questions"]
                                i=0
                                for qn in subs["questions"]:
                                    subs["questions"][i]["serialno"]=i+1
                                    i +=1
                            if types =="question" or types =="record":
                                #print name
                                json_subs=json.loads(open(os.path.join(APP_STATIC_JSON,name+".json")).read())
                                qns_list=json_subs["questions"];
                                serialno=range(0,len(qns_list))
                                shuffle(serialno)
                                for no in range(0,cnt):
                                    subs["questions"].append(qns_list[serialno[no]])
                                    subs["questions"][no]["serialno"]=no+1
                            if types == "passage":
                                #print name
                                json_subs=json.loads(open(os.path.join(APP_STATIC_JSON,name+".json")).read())
                                psglist=json_subs["passageArray"]
                                serialno=range(0,len(psglist))
                                shuffle(serialno)
                                subs["questions"]=psglist[serialno[0]]["questions"]
                                j=0
                                for qn in subs["questions"]:
                                    subs["questions"][j]["serialno"]=j+1
                                    j +=1
                                subs["passage"]=psglist[serialno[0]]["passage"]
                            if types =="essay":
                                #print name
                                json_subs=json.loads(open(os.path.join(APP_STATIC_JSON,name+".json")).read())
                                qns_list=json_subs["questions"];
                                serialno=range(0,len(qns_list))
                                shuffle(serialno)
                                for no in range(0,cnt):
                                    subs["questions"].append(qns_list[serialno[no]])
                                    subs["questions"][no]["serialno"]=no+1
                            if name == "T2-Listening":
                                #print name
                                json_subs=json.loads(open(os.path.join(APP_STATIC_JSON,name+".json")).read())
                                video_list=json_subs["videoArray"]
                                serialno=range(0,len(video_list))
                                shuffle(serialno)
                                subs["link"]=video_list[serialno[0]]["link"]
                                subs["questions"]=video_list[serialno[0]]["questions"]
                                k=0
                                for qn in subs["questions"]:
                                  subs["questions"][k]["serialno"]=k+1
                                  k +=1
    #ss=json.dumps(json_temp)
    return json_temp

def getAnswer(qid):
    qid=int(qid)
    if qid in range(e1_start,e1_end):
        e1_readjson=json.loads(open(os.path.join(APP_STATIC_JSON, 'E1-Reading.json')).read())
        for psg in e1_readjson["passageArray"]:
            for key in psg["questions"]:
                if int(key["id"]) == qid:
                    for op in key["options"]:
                        if op[0] == "=":
                            return op[1:len(op)]
    if qid in range(e2_start,e2_end):
        e2_lsnjson=json.loads(open(os.path.join(APP_STATIC_JSON, 'E2-Listening.json')).read())
        for key in e2_lsnjson["videoArray"]:
            for qn in key["questions"]:
                if int(qn["id"]) == qid:
                    for op in qn["options"]:
                        if op[0] == "=":
                            return op[1:len(op)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/javascripts/<path:path>')
def send_javascripts(path):
    return send_from_directory('static/javascripts', path)

@app.route('/video/<path:path>')
def send_video(path):
    return send_from_directory('static/video', path)

@app.route('/stylesheets/<path:path>')
def send_stylesheets(path):
    return send_from_directory('static/stylesheets', path)

@app.route('/checklogin')
def checklogin():
    myname = "Veda"
    emailaddr = "vy@fju.us"
    ss = Response.query.filter_by(emailid=emailaddr).first()
    if ss is None:
        response = Response(emailid=emailaddr, name=myname)
        db.session.add(response)
        db.session.commit()
    sp=userDetails.query.filter_by(email=emailaddr).first()
    if sp is not None:
        return render_template('quiz.html')
    else:
        return render_template('register.html')

@app.route('/savepersonaldata', methods=['POST'])
def savepersonaldata():
    userdetails = userDetails(name=request.form['name'],email="vy@fju.us",phno=request.form['phone'],rollno=request.form['rollno'],learningcenter=request.form['learningcenter'])
    db.session.add(userdetails)
    db.session.commit()
    return redirect(url_for('startquiz'))

@app.route('/getquizstatus', methods=['POST'])
def getquizstatus():
    #qbank=QuestionBank()
    # check if candidate is resuming the test
    r1 = Randomize.query.filter_by(user1="vy@fju.us").all()
    #print r1
    #logging.error("random values")
    if r1:
        isRandomized = True
        qid_list={}
        for data in r1:
            qid_list[int(data.qno)] = data.serialno
        json_data=getQuestionPaper(qid_list)
    else:
        isRandomized = False
        json_data=generateQuestionPaper()
    print json_data;
    # TODO
    # New json_data returned from the question bank if is randomized is false
    # Else list of question ID should be fetched from randomize table
    # pass the question IDs list to the question bank to get json_data

    #json_data = json.loads(open(os.path.join(APP_STATIC_JSON,'quizdata.json')).read())
    for key in json_data:
        if  key == "section":
            section = json_data[key]
            for s in  section:
                for key in s:
                    if key == "subsection":
                        for subs in s[key]:
                            for key in subs:
                                if key == "questions":
                                    for q in subs[key]:
                                        if not isRandomized:
                                            r = Randomize(user1 = "vy@fju.us", serialno = q['serialno'], qno=q["id"])
                                            db.session.add(r)
                                            db.session.commit()
                                        else:
                                            #print q['id']
                                            #logging.error("question id is:")
                                            r = Randomize.query.filter_by(user1 = "vy@fju.us", qno = q["id"]).all()
                                        q1 = Response.query.filter_by(emailid="vy@fju.us", currentQuestion=q["id"]).order_by(Response.time.desc()).first()
                                        if q1:
                                            q["responseAnswer"]=q1.submittedans
                                            q["responseTime"]=q1.responsetime
                                            q["status"]=q1.q_status

    td = TestDetails.query.filter_by(email="vy@fju.us").first()
    if td:
        if td.testend:
            json_data['quizStatus'] = 'END'
        else:
            json_data['quizStatus'] = 'INPROGRESS'
    else:
        json_data['quizStatus'] = 'START'

    ss=json.dumps(json_data)
    return ss

@app.route('/testtime', methods=['POST'])
def testtime():
    duration = 60 * 60
    td = TestDetails.query.filter_by(email="vy@fju.us").first()
    if td is None:
        testdetails = TestDetails(email="vy@fju.us",test=True,delays=0.0)
        db.session.add(testdetails)
        db.session.commit()
        obj = {u"timeSpent":0, u"timeRemaining":duration, u"quizStatus": u"INPROGRESS"}
    else:
        if not td.testend:
            currTime = datetime.now()
            deltaTime = (currTime - td.lastPing).total_seconds()
            if(deltaTime > 65.0):
                td.delays = td.delays + deltaTime - 60.0
                db.session.add(td)
                db.session.commit()
            timeSpent = (currTime - td.teststime).total_seconds() - td.delays

            if timeSpent >= duration:
                td.testend = True
                quizStatus = u"END"
            else:
                quizStatus = u"INPROGRESS"
            obj = {u"timeSpent" : timeSpent, u"quizStatus": quizStatus, u"timeRemaining" : duration - timeSpent}
            td.lastPing = currTime
            db.session.add(td)
            db.session.commit()
        else:
            obj = {u"quizStatus":u"END"}
    ss=json.dumps(obj)
    return ss

@app.route('/submitanswer', methods=["POST"])
def submitanswer():
    td=TestDetails.query.filter_by(email="vy@fju.us").first()
    if td and not td.testend:
        validresponse="false"
        status=""
        errortype=""
        q_status=""
        score=0
        type=""
        vals = json.loads(cgi.escape(request.get_data()))
        vals = vals['jsonData']
        currentQuestion =vals['id']
        submittedans = vals['responseAnswer']
        responsetime = vals['responseTime']
        # opening  json file of quizdata
        #logging.error(currentQuestion,submittedans)
        currentQuestion=int(currentQuestion)
        if submittedans == "skip":
            validresponse="true"
            q_status="skip"
        
        elif currentQuestion in range(e3_start,e3_end):
            r=UserAudio.query.filter_by(user="vy@fju.us").first()
            if r :
                q_status="submitted"
                status="success"
                validresponse="true"
            else :
                q_status="submitted"
                status="success"
                validresponse="true"
        elif currentQuestion in range(e4_start,e4_end):
            q_status="submitted"
            status="success"
            validresponse="true"
        else :
            q_status="submitted"
            status="success"
            validresponse="true"
            cans=getAnswer(currentQuestion)
            if cans == submittedans:
                score = 1
        if validresponse=="true":
            status="success"
            if q_status!="skip":
                q_status="submitted"
        else:
            status="error"

        # creating json file for error response
        # placing in to the database
        n1=int(currentQuestion)
        data=Response(serialno=n1,emailid="vy@fju.us",name="Veda",currentQuestion=str(currentQuestion),submittedans=submittedans,responsetime=responsetime,q_status=q_status,q_score=score)
        db.session.add(data)
        db.session.commit()

        # added time taken based on the timer
        obj = {u"status":status , u"q_status":q_status, u"validresponse":validresponse, u"qid":currentQuestion}

    else:
        obj = {u"testEnd" : True}
    ss=json.dumps(obj)
    return ss

@app.route('/getResult', methods=["GET"])
def getResult():
    totalscore = 0
    q1= Response.query.filter_by(emailid="vy@fju.us").order_by(Response.serialno, Response.time.desc()).all()
    questionresponses_dict = {}
    question_records=[]
    totalscore=0
    s1="0"
    for q in q1:
        if q.responsetime is not None:
            if q.currentQuestion != s1 :
                s1=q.currentQuestion
                #totalscore=q.responsetime+q.q_score
                question = {"user":"Veda","submittedans":q.submittedans, "q_score":q.q_score,"currentQuestion":s1,"responsetime":q.responsetime}
                question_records.append(question)
    questionresponses_dict["question"]=question_records
    questionresponses_dict["totalscore"]=totalscore
    ss=json.dumps(questionresponses_dict)
    return ss

@app.route('/getScore', methods=["GET"])
def getScore():
    score=0
    q1= Response.query.filter_by(emailid="vy@fju.us").all()
    for q in q1:
        score=score+1
    template_values = {
        'p': q1,
        'score1':score,
        }
    return render_template("testresult.html")

@app.route('/autosaveEssay', methods=["POST"])
def autosaveEssay():
    vals = json.loads(cgi.escape(request.get_data()))
    vals = vals['jsonData']
    qid = vals['currentQuestion']
    print(vals)
    ans = vals['draft']
    qattemptedtime = vals['responsetime']
    print(vals)
    data1 = EssayTypeResponse.query.filter_by(useremailid = "vy@fju.us", qid = qid).first()
    print(qid)

    if data1:
        data1.qattemptedtime=qattemptedtime
        data1.ansText = ans
        db.session.add(data1)
        db.session.commit()

    else:
        data = EssayTypeResponse(useremailid="vy@fju.us", qid=qid, qattemptedtime=qattemptedtime, ansText = ans)
        db.session.add(data)
        db.session.commit()

    ss=json.dumps(vals)
    return ss

@app.route('/uploadredirect', methods=["POST"])
def uploadredirect():
    return redirect(url_for("/upload_audio"))

@app.route('/upload_audio', methods=["POST"])
def upload_audio():
    try:
        files = request.files.getlist('file')
        if files:
            useraudio = UserAudio(user="vy@fju.us", blob1=files[0].file.read())
            db.session.add(useraudio)
            db.session.commit()
    except Exception,e:
        return "Record Not Saved.\n\n"+str(e)

@app.route('/view_audio/<link>', methods=["GET"])
def view_audio(link):
    event = UserAudio.query.get_or_404(link)
    return app.response_class(event.blob1, mimetype='application/octet-stream')

# @app.route('/audio')
# def audio():

@app.route('/endtest', methods=["POST"])
def endtest():
    val = json.loads(cgi.escape(request.get_data()))
    val = val['jsonData']
    print(val)
    testend = val['testend']
    score = val['finalScore']
    spklink = val['spklink']
    print(testend)
    data1 = TestDetails.query.filter_by(email = "vy@fju.us").first()
    userdata=userDetails.query.filter_by(email = "vy@fju.us").first()
    learningcenter=userdata.learningcenter    
    if data1:
        data1.testend = testend
        data1.score = score
        data1.learningcenter = learningcenter
        db.session.add(data1)
        db.session.commit()

@app.route('/startquiz')
def startquiz():
    return render_template('quiz.html')