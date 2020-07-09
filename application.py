import os
#import render_template

from flask import Flask, session,request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index1.html")

@app.route("/registration")
def registration():
    return render_template("index2.html")

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]   
        
    username1=db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
    password1=db.execute("SELECT password FROM users WHERE username=:username",{"username":username}).fetchone()
    db.commit()
    #return render_template("index4.html", value=password,password1=password1)
    #password2=password1[0]
    if username1 is None:
            return render_template("index3.html")
    else:        
        for password2 in password1:
                if password2 == password:
                    session['username']=request.form["username"]
                    return render_template('index4.html')
                else:
                    return render_template("index5.html")

            #return render_template('index5.html')


@app.route('/newuser',methods=["GET","POST"])
def newuser():
    if request.method=="POST":
        email=request.form["email"]
        fname=request.form["fname"]
        username=request.form["username"]
        password=request.form["password"]
    db.execute("INSERT INTO users (email,fname,username,password) VALUES(:email,:fname,:username,:password)",{"email":email,"fname":fname,"username":username,"password":password}) 
    db.commit()
    return render_template("index6.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template("index1.html")     

@app.route('/books',methods=["GET","POST"])
def books():
    if request.method=="POST":
        name=request.form["search"]
    list1=db.execute("SELECT title FROM books WHERE isbn=:name OR title=:name OR author=:name OR year=:name",{"name":name}).fetchall()
    db.commit()
    for list in list1:
        if list is None:
            return render_template("index8.html")
        else:
            break   
    thislist=[]
    for list in list1:
        thislist.append(list)               
    return render_template("index7.html", list1=thislist)

@app.route('/askedbook/<b_name>',methods=["GET","POST"])
def askedbook(b_name):
    name=session['username']
    list2=db.execute("SELECT * FROM books WHERE title=:b_name",{"b_name":b_name}).fetchall()
    list3=db.execute("SELECT review FROM reviews WHERE username=:username AND b_name=:b_name",{"username":name,"b_name":b_name}).fetchone()
    list4=db.execute("SELECT stars FROM reviews WHERE username=:username AND b_name=:b_name",{"username":name,"b_name":b_name}).fetchone()
    db.commit()
    return render_template("index9.html",value=list2,value2=list3,value3=list4)

@app.route('/submit_review/<b_name>',methods=["GET","POST"])
def submit_review(b_name):
    name=session['username']
    review=request.form["review"]
    stars=request.form["star"]
    db.execute("INSERT INTO reviews (username,review,b_name,stars) VALUES(:username,:review,:b_name,:stars)",{"username":name,"b_name":b_name,"review":review,"stars":stars}) 
    list2=db.execute("SELECT * FROM books WHERE title=:b_name",{"b_name":b_name}).fetchall()
    list3=db.execute("SELECT review FROM reviews WHERE username=:username AND b_name=:b_name",{"username":name,"b_name":b_name}).fetchone()
    list4=db.execute("SELECT stars FROM reviews WHERE username=:username AND b_name=:b_name",{"username":name,"b_name":b_name}).fetchone()
    db.commit()
    return render_template("index9.html",value=list2,value2=list3,value3=list4)

@app.route('/change_review/<b_name>',methods=["GET","POST"])
def change_review(b_name):
    name=session['username']
    list2=db.execute("SELECT * FROM books WHERE title=:b_name",{"b_name":b_name}).fetchall()
    db.execute("DELETE FROM reviews WHERE b_name=:b_name AND username=:username",{"b_name":b_name,"username":name})
    #reviews.query.filter_by(id=b_).delete()
    db.commit()
    return render_template("index11.html",value=list2)

@app.route('/edit_review/<b_name>',methods=["GET","POST"])
def edit_review(b_name):
    name=session['username']
    review=request.form["review"]
    stars=request.form["star"]
    db.execute("INSERT INTO reviews (username,review,b_name,stars) VALUES(:username,:review,:b_name,:stars)",{"username":name,"b_name":b_name,"review":review,"stars":stars}) 
    list2=db.execute("SELECT * FROM books WHERE title=:b_name",{"b_name":b_name}).fetchall()
    list3=db.execute("SELECT review FROM reviews WHERE username=:username AND b_name=:b_name",{"username":name,"b_name":b_name}).fetchone()
    list4=db.execute("SELECT stars FROM reviews WHERE username=:username AND b_name=:b_name",{"username":name,"b_name":b_name}).fetchone()
    db.commit()
    return render_template("index9.html",value=list2,value2=list3,value3=list4)
