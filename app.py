from flask import Flask,render_template,request,redirect,session
import random,smtplib
#import sqlite3
import pymysql
app = Flask(__name__)
app.secret_key="serect"
#conn=pymysql.connect(host="localhost",user="root",password="",database="flames")

conn=pymysql.connect(host="localhost",user="root",password="",database="flames")
@app.route("/")
def one():
    return(render_template("home1.html"))
    #return(r"<a href='\login'>login</a> <a href='\id\1'>one</a><a href='\register'>register</a>")

@app.route("/id/<ids>")
def index1(ids):
    return (render_template("index.html"))

@app.route("/id/<ids>",methods=["POST","GET"])
def index2(ids):
    s1,s2=request.form["user_name"],request.form["friend_name"]
    s1,s2=s1.lower(),s2.lower()
    s1=[i for i in s1 if i!='\r']
    s2=[i for i in s2 if i!='\r']
    #print(s1,s2)
    n1,n2=[]+s1,[]+s2
    for i in range(len(s1)):
        if s1[i] in n2:
            n1.remove(s1[i])
            n2.remove(s1[i])
    #print(n1,n2)
    fc=len(n1+n2)
    f,c='flames',0
    f1=list(f)
    if fc==1:
        r='SISTER'
    elif fc==2:
        r='ENEMIES'
    elif fc==3:
        r='FRIENDS'
    else:
        for i in range(fc*len(f)):
            for j in range(len(f1)):
                c+=1
                if c%fc==0:
                    f1.remove(f1[j])
            if len(f1)==1:
                break
        r=""
        for i in f1:
            if i=='f':
                r='FRIENDS'
                break
            elif i=='l':
                r='LOVE'
                break
            elif i=='a':
                r='ADORE'
                break
            elif i=='m':
                r='MARRIAGE'
                break
            elif i=='e':
                r='ENEMIES'
                break
            else:
                r='SISTER'
                break

        conn=pymysql.connect(host="localhost",user="root",password="",database="flames")


        c = conn.cursor()
        if c.execute("select id from details where id=%s" % (ids)):
            c.execute("insert into result values('%s','%s','%s','%s')"%(ids,request.form["user_name"],request.form["friend_name"],r))
            conn.commit()
            return(render_template("result.html",r=r,s1=request.form["user_name"],s2=request.form["friend_name"]))
        return ("id not present dont have account <a href='register'>register</a>")

@app.route("/login")
def login1():
    return(render_template("login.html"))

@app.route("/login",methods=["POST","GET"])
def login2():
    email=request.form["email"]
    password=request.form["password"]
    conn = pymysql.connect(host="localhost",user="root",password="",database="flames")


    c = conn.cursor()
    if c.execute("select id from details where email='%s' and password='%s'"%(email,password)):
        id=c.fetchall()
        c.execute("select user_name,friend_name,result from result where ids='%s';"%(str(id[0][0])))
        result=c.fetchall()
        return(render_template("home.html",result=result,id=id[0][0]))
    return(render_template("displaytext.html",text="invalid user details",url="",link=""))

@app.route("/register")
def register1():
    return(render_template("register.html"))

@app.route("/register",methods=["POST","GET"])
def regester1():
    email=request.form["email"]
    password=request.form["password"]
    name=request.form["name"]
    conn = pymysql.connect(host="localhost",user="root",password="",database="flames")


    c = conn.cursor()
    if c.execute("select id from details where email='%s';"%(email)):
        return(render_template("displaytext.html",text="email already taken",url="register",link="regester again"))
        #return("email already taken <a href='register'>register</a>")
    c.fetchall()
    c.execute("insert into details(name,email,password) values('%s','%s','%s');"%(name,email,password))
    conn.commit()
    conn.close()
    return(redirect("/login"))


@app.route("/forgot")
def forgot1():
    #enter email
    return(render_template("forgot.html"))

@app.route("/forgot",methods=["POST","GET"])
def forgot2():
    session["email"]=request.form["email"]
    otp=str(random.randint(10000,99999))
    print(otp)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("checkmeter888@gmail.com", "Checkmeter@888")
    message = "OTP to reset your password is %s"%(otp)
    s.sendmail("checkmeter888@gmail.com", request.form["email"], message)
    s.quit()
    #send otp to the mail
    #enter otp,newpassword
    session["otp"]=otp
    return(render_template("forgot1.html"))

@app.route("/confirm")
def confirm1():
    return("non")
@app.route("/confirm",methods=["POST","GET"])
def confirm2():
    if request.form["otp"]==session["otp"]:
        conn = pymysql.connect(host="localhost", user="root", password="", database="flames")
        c=conn.cursor()
        c.execute("update details set password='%s' where email='%s';"%(request.form["newpassword"],session["email"]))
        return(render_template("displaytext.html",text="Sucessfully changed your password ",url="login",link="Login"))
    return(render_template("displaytext.html",text=r"otp did not match ",url="forgot",link="Forgot password"))



if __name__ == "__main__":
    app.run(host="0.0.0.0")#doesnot work in pycharm but works in idle