from flask import Flask, flash, redirect, render_template, request, session, abort, url_for,jsonify
from werkzeug.utils import secure_filename
from flaskext.mysql import MySQL
from functools import wraps
# from datetime import datetime, date, timedelta
import datetime
import calendar
# from datetime import datetime, timedelta
import os
from flask_mail import Mail, Message

# password generator *****
import string
import random
# ****************************

# cors************************
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = b'_5#y2hj,mngghF4Q8z\n\xec]/'
CORS(app)

app.config['path']="static/upload"
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'crime_detection'

dataTypesToDownload = [".jpg", ".jpeg", ".png", ".gif", ".ico", ".css", ".js", ".html"]
mysql = MySQL(app)
mysql.init_app(app)




def Mailer(sender,recipient,Subject,body):
    try:
        msg=Message(Subject,sender=sender,recipients=[recipient])
        msg.body=body
        # msg.html = render_template('Mail_Template.html',password=body)
        Mail.send(msg)

        return "sended successfully"
    except:
        return "A Error occurred while perform mailing !"

def randomString(stringLength):

    """Generate a random string with the combination of lowercase and uppercase letters """
    # letters = string.ascii_letters
    # return ''.join(random.choice(letters) for i in range(stringLength))

    # """ Generate a random string of letters and digits """    query=""
    # cursor.execute(query)
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))
    
def allow_for_loggined_users_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login',next=request.endpoint))
        return f(*args, **kwargs)
    return wrapper
# -----------------------------------------------------------------------------------------------------------------------------

  

@app.route('/admin')
@allow_for_loggined_users_only
def admin():
    return render_template('admin_home.html')

@app.route('/user',methods=['GET','POST'])
@allow_for_loggined_users_only
def user():
    if request.method=='GET':      
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) count from complaints_feedback where complainant_id=%s",session['lid'])     
        rows = cursor.fetchone()
        print(rows) 
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * from complaints_feedback where complainant_id=%s",session['lid'])     
        data = cursor.fetchall()
        print(data) 
        return render_template('user_home.html',row=rows,row1=data)
        
            
@app.route('/advocate_home')
@allow_for_loggined_users_only
def advocate_home():
    return render_template('advocate_home.html')

@app.route('/advocate_admin_home')
@allow_for_loggined_users_only
def advocate_admin_home():
    return render_template('advocate_admin_home.html')
    
@app.route('/station_admin_home')
@allow_for_loggined_users_only
def station_admin_home(): 
    if request.method == 'GET':         
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT st.name, (SELECT COUNT(DISTINCT ct.case_id) FROM cases ct WHERE ct.s_id = st.s_id) AS Total_Case_Counts,(SELECT COUNT(*) FROM station_user_map sm JOIN registration r ON sm.lid = r.lid JOIN login l ON r.lid = l.lid WHERE sm.s_id = st.s_id AND l.type = 'police') AS Total_Employees FROM station st WHERE st.s_id = %s",session['sid'])
        # cursor.execute("SELECT st.name, COUNT(DISTINCT ct.case_id) AS Total_Case_Counts, COUNT(DISTINCT et.lid) AS Total_Employees FROM station st JOIN cases ct ON st.s_id = ct.s_id JOIN login et ON st.s_id = ct.s_id WHERE et.lid = st.sh_id  GROUP BY et.lid;")
        rows = cursor.fetchall()
        print(rows) 
        return render_template('station_admin_home.html',rows=rows)
    # monthwise
    #SELECT YEAR(created_on) AS year, MONTH(created_on) AS month, COUNT(*) AS case_count FROM cases GROUP BY YEAR(created_on), MONTH(created_on) ORDER BY YEAR(created_on), MONTH(created_on);
    # yrwise
    #SELECT YEAR(created_on) AS year, COUNT(*) AS case_count FROM cases GROUP BY YEAR(created_on) ORDER BY YEAR(created_on);   
        # return render_template('station_admin_home.html')

@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  
    if request.method == 'POST':
        conn =mysql.connect()
        cursor = conn.cursor()
        query="select * from login where username=%s and password=%s and provisionized=1"
        cursor.execute(query,(request.form['username'],request.form['password']))
        result=cursor.fetchone()
        # print(result)
        conn.commit()                 
        if result:
            # print(result)
            session['loggedin'] =True
            session['username']= result[1] 
            session['lid']= result[0]  
            session['type']= result[4]
            if (result[4] == 'admin'):
                return redirect(url_for('admin'))
            elif (result[4] == 'station_admin'):
                conn =mysql.connect()
                cursor = conn.cursor()
                cursor.execute("select login.*,station_user_map.*,station.* from login,station_user_map,station where station_user_map.lid=login.lid and login.type='station_admin' and station.s_id=station_user_map.s_id and login.lid=%s",result[0])     
                rows = cursor.fetchone()
                session['sid']=rows[10]
                print(rows) 
                print(session['sid'])   
                return redirect(url_for('station_admin_home'))  
            elif (result[4] == 'advocate_admin'):
                return redirect(url_for('advocate_admin_home'))   
            elif (result[4] == 'advocate'):
                return redirect(url_for('advocate_home'))   
            elif (result[4] == 'user'):
                return redirect(url_for('user'))                                                                  
                
            else:
                flash('wrong password!')
                session['logged_in'] = True
        else:
            flash('Incorrect username or password supplied')
            return render_template("login.html")
        
    # return render_template('login.html',msg="wrong password!")    

@app.route('/logout',methods=['GET'])
def logout():
    print(session['loggedin'])
    if session['loggedin']:
        session['loggedin']=False
        session.pop(id,None)
        session.pop('username',None)
        return redirect(url_for('login'))
    else:
        print("loging first")  
        return "something went wrong"  

@app.route('/admin_add_station')
@allow_for_loggined_users_only
def admin_add_station():
    if request.method == 'GET':      
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT station.s_id,station.sh_id,station.name,station.address,station.member from station")     
        rows = cursor.fetchall()
        print(rows) 
        return render_template('admin_add_station.html',rows=rows)    

@app.route('/add_station',methods=['GET','POST'])
@allow_for_loggined_users_only
def station_registration():
              
    if request.method == 'GET':      
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT station.s_id,station.sh_id,station.name,station.address,station.member from station")     
        rows = cursor.fetchall()
        print(rows) 
        return render_template('admin_add_station.html',rows=rows)  
    if request.method == 'POST':
        data = request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        date=datetime.datetime.now()     
        query = "insert into station(sh_id,name,address,member,created_on) values (%s,%s,%s,%s,%s)"
        cursor.execute(query, (session['lid'],data['station_name'], data['station_address'], data['members'],date))          
        conn.commit()
        conn.close()
        return redirect(url_for('station_registration')) 
      

@app.route('/update_station',methods=['POST'])
def update_station():
    if request.method == "POST":
        data=request.json
        print(data)
        conn =mysql.connect()
        cursor = conn.cursor()
        q="UPDATE station SET `name`='{}',`address`='{}',`member`='{}' WHERE `s_id`='{}'"
        query= q.format(data['station'],data['saddress'],data['smember'],data['sid'])                        
        print(query)
        cursor.execute(query)
        conn.commit()
        conn.close()
        return 'ok'
        
@app.route('/update_station_employee',methods=['POST'])
def update_station_employee():
    if request.method == "POST":
        data=request.json
        print(data)
        conn =mysql.connect()
        cursor = conn.cursor()
        q="UPDATE registration SET `name`='{}',`gender`='{}',`dob`='{}',`email`='{}',`phone`='{}',`address`='{}',`adharnumber`='{}',`occupation`='{}' WHERE `id`='{}'"
        query= q.format(data['name'],data['gender'],data['dob'],data['email'],data['phone'],data['address'],data['adharnumber'],data['occupation'],data['id'])                        
        print(query)
        cursor.execute(query)
        conn.commit()
        conn.close()
        return 'ok'

       

@app.route('/view_station',methods=['GET','POST'])
@allow_for_loggined_users_only
def view_station():
    if request.method == 'GET':         
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT station.s_id,station.sh_id,station.name,station.address,station.member from station")
        rows = cursor.fetchall()
        print(rows) 
        return render_template('admin_manage_station.html',rows=rows)  
        

# @app.route('/edit/<int:id>')
# def edit_view(id):
#     conn = mysql.connect()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM station WHERE s_id=%s", id)
#     data = cursor.fetchone()
#     print("test",data)
#     cursor.close()
#     conn.close()
#     return jsonify(data)
   



          

@app.route('/delete_station',methods=['POST'])
def delete_station():
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from station where s_id=%s"
        cursor.execute(query, request.form.get('delete_by_id'))
        conn.commit()
        conn.close()
        return redirect(url_for('station_registration'))   

@app.route('/admin_add_station_employee',methods=['GET','POST'])
@allow_for_loggined_users_only
def admin_add_station_employee():
    if request.method == 'GET':       
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM station")
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('admin_add_employee.html',row=data)             
    if request.method == 'POST':
        data = request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        password=randomString(10) 
        date=datetime.datetime.now()
        print(date)
        img = request.files['files']
        filename = secure_filename(img.filename)
        print(os.path.join(app.config['path']  + filename))
        img.save(os.path.join(app.config['path']  + filename))
        query = "insert into login(username,password,provisionized,type,created_on) values (%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['name'], password, 0,'police',date))   
        employeeid=cursor.lastrowid
        query = "INSERT INTO registration(lid,name,gender,dob,email,phone,address,adharnumber,occupation,image,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (cursor.lastrowid,data['name'],data['radio'], data['dob'], data['email'], data['phone'], data['address'], data['adharnumber'],data['occupation'],filename,date))        
        query = "insert into station_user_map(lid,s_id,created_on) values (%s,%s,%s)"
        cursor.execute(query, (employeeid,data['sid'],date))          
        conn.commit()
        conn.close()
        return redirect(url_for('admin_add_station_employee'))   

@app.route('/admin_view_station',methods=['GET','POST'])
@allow_for_loggined_users_only
def admin_view_station():
    if request.method == 'GET':       
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute("select * from station")
        rows = cursor.fetchall()
        print(rows) 
        return render_template('admin_view_station.html',rows=rows)  
        

@app.route('/admin_view_employee', methods=['GET','POST'])
@allow_for_loggined_users_only
def admin_view_employee():
    if request.method == 'POST':
        data= request.form
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute("SELECT station.*,station_user_map.*,registration.*,login.* from station,station_user_map,registration,login where station.s_id=station_user_map.s_id and registration.lid=station_user_map.lid and registration.lid=login.lid and login.type='police' and station.s_id=%s",data['sid'])
        rows = cursor.fetchall()
        cursor.execute("SELECT station.*,station_user_map.*,registration.*,login.* from station,station_user_map,registration,login where station.s_id=station_user_map.s_id and registration.lid=station_user_map.lid and registration.lid=login.lid and login.type IN ('police', 'station_admin') and station.s_id=%s",data['sid'])
        rows1 = cursor.fetchall()
        print(rows) 
        return render_template('admin_view_employee.html',rows=rows,rows1=rows1)  
 
@app.route('/accept_station_admin', methods=['GET','POST'])  
def accept_station_admin():
    if request.method == 'POST':
        data=request.form['accept']
        data=data.split()
        print(data)
        conn=mysql.connect()
        cursor=conn.cursor()
        query="update login set type='"+str(data[1])+"', provisionized=1 where lid="+data[0]
        cursor.execute(query)
        print(query)  
        conn.commit()
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute("SELECT station.*,station_user_map.*,registration.*,login.* from station,station_user_map,registration,login where station.s_id=station_user_map.s_id and registration.lid=station_user_map.lid and registration.lid=login.lid and station.s_id=%s",data[2])
        rows = cursor.fetchall()
        print(rows) 
        conn.close()    
        return render_template('admin_view_employee.html',rows=rows)    

@app.route('/delete_station_employee',methods=['POST'])
def delete_station_employee():
    if request.method == 'POST':
        data=request.form['delete_by_id']
        data=data.split()
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from station_user_map where su_id=%s"
        cursor.execute(query, data[0])
        query = "delete from registration where id=%s"
        cursor.execute(query, data[1])
        query = "delete from login where lid=%s"
        cursor.execute(query, data[2])
        conn.commit()
        conn = mysql.connect()
        cursor.execute("SELECT station.*,station_user_map.*,registration.*,login.* from station,station_user_map,registration,login where station.s_id=station_user_map.s_id and registration.lid=station_user_map.lid and registration.lid=login.lid and station.s_id=%s",data[3])
        rows = cursor.fetchall()
        print(rows) 
        conn.close()    
        return render_template('admin_view_employee.html',rows=rows)
        
@app.route('/station_admin_delete_employee',methods=['POST'])
def station_admin_delete_employee():
    if request.method == 'POST':
        data=request.json
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from station_user_map where su_id=%s"
        cursor.execute(query, data['stid'])
        query = "delete from registration where id=%s"
        cursor.execute(query, data['regid'])
        query = "delete from login where lid=%s"
        cursor.execute(query, data['regid'])
        conn.commit()      
        return 'ok'     


@app.route('/admin_add_advocate_admin', methods=['GET','POST'])
@allow_for_loggined_users_only
def admin_add_advocate_admin():
    if request.method == 'GET':  
        return render_template('admin_add_advocate_admin.html')                               
    if request.method == 'POST':
        data = request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        password=randomString(10) 
        date=datetime.datetime.now()
        print(date)
        img = request.files['files']
        filename = secure_filename(img.filename)
        print(os.path.join(app.config['path']  + filename))
        img.save(os.path.join(app.config['path']  + filename))
        query = "insert into login(username,password,provisionized,type,created_on) values (%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['name'], password, 1,'advocate_admin',date))   
        advocateid=cursor.lastrowid
        query = "INSERT INTO registration(lid,name,gender,dob,email,phone,address,adharnumber,occupation,image,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (cursor.lastrowid,data['name'],data['radio'], data['dob'], data['email'], data['phone'], data['address'], data['adharnumber'],data['occupation'],filename,date))        
        query = "insert into advocate_info(lid,enrolment_year,practice_place,created_on) values (%s,%s,%s,%s)"
        cursor.execute(query, (advocateid,data['year'],data['practice_place'],date))          
        conn.commit()
        conn.close()
        return redirect(url_for('admin_add_advocate_admin')) 

@app.route('/view_manage_advocate',methods=['GET','POST'])
@allow_for_loggined_users_only
def view_manage_advocate():
    if request.method == 'GET':      
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute("select advocate_info.*,registration.*,login.* from login,registration,advocate_info where login.lid=registration.lid and registration.lid=advocate_info.lid and login.type='advocate_admin'")
        rows = cursor.fetchall()
        # print(rows) 
        return render_template('admin_view_advocate_admin.html',rows=rows)   

@app.route('/admin_update_advocate',methods=['POST'])
def admin_update_advocate():
    if request.method == "POST":
        data=request.json
        print(data)
        conn =mysql.connect()
        cursor = conn.cursor()
        q="UPDATE registration SET `name`='{}',`gender`='{}',`dob`='{}',`email`='{}',`phone`='{}',`address`='{}',`adharnumber`='{}',`occupation`='{}' WHERE `id`='{}'"
        query= q.format(data['name'],data['gender'],data['dob'],data['email'],data['phone'],data['address'],data['adharnumber'],data['occupation'],data['id'])                        
        cursor.execute(query)
        q="UPDATE advocate_info SET `enrolment_year`='{}',`practice_place`='{}' WHERE `aid`='{}'"
        query= q.format(data['enrolment'],data['place'],data['aid'])                        
        print(query)        
        cursor.execute(query)
        conn.commit()
        conn.close()
        return 'ok'         
    
@app.route('/delete_advocate_admin',methods=['POST'])
def delete_advocate_admin():
    if request.method == 'POST':
        data=request.form['delete_by_id']
        data=data.split()
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from advocate_info where aid=%s"
        cursor.execute(query, data[0])
        query = "delete from registration where id=%s"
        cursor.execute(query, data[1])
        query = "delete from login where lid=%s"
        cursor.execute(query, data[2])
        conn.commit()
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute("select advocate_info.*,registration.*,login.* from login,registration,advocate_info where login.lid=registration.lid and registration.lid=advocate_info.lid and login.type='advocate_admin'")
        rows = cursor.fetchall()
        print(rows)     
        return render_template('admin_view_advocate_admin.html',rows=rows)    

@app.route('/station_admin_add_employee',methods=['GET','POST'])
@allow_for_loggined_users_only
def station_admin_add_employee():
    if request.method == 'GET':               
        return render_template('station_admin_add_employee.html')           
    if request.method == 'POST':
        data = request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        password=randomString(10) 
        date=datetime.datetime.now()
        print(date)
        img = request.files['files']
        filename = secure_filename(img.filename)
        print(os.path.join(app.config['path']  + filename))
        img.save(os.path.join(app.config['path']  + filename))
        query = "insert into login(username,password,provisionized,type,created_on) values (%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['name'], password, 0,'police',date))   
        employeeid=cursor.lastrowid
        query = "INSERT INTO registration(lid,name,gender,dob,email,phone,address,adharnumber,occupation,image,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (cursor.lastrowid,data['name'],data['radio'], data['dob'], data['email'], data['phone'], data['address'], data['adharnumber'],data['occupation'],filename,date))        
        query = "insert into station_user_map(lid,s_id,created_on) values (%s,%s,%s)"
        cursor.execute(query, (employeeid,session['sid'],date))          
        conn.commit()
        conn.close()
        return redirect(url_for('station_admin_add_employee'))         

@app.route('/station_admin_manage_employee',methods=['GET','POST'])
@allow_for_loggined_users_only
def station_admin_manage_employee():
    if request.method == 'GET':        
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute("select registration.*,login.*,station_user_map.*,station.* from station_user_map,login,registration,station where station_user_map.lid=registration.lid and registration.lid=login.lid and station_user_map.s_id=station.s_id and login.type='police' and station.s_id=%s",session['sid'])
        rows = cursor.fetchall()
        print(rows) 
        return render_template('station_admin_view_employee.html',rows=rows) 
     

@app.route('/station_admin_manage_user',methods=['GET','POST'])
@allow_for_loggined_users_only
def station_admin_manage_user():
    if request.method == 'GET':       
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute("select registration.*,login.*,station_user_map.*,station.* from station_user_map,login,registration,station where station_user_map.lid=registration.lid and registration.lid=login.lid and station_user_map.s_id=station.s_id and login.type='user' and login.provisionized=0 and station.s_id=%s",session['sid'])
        rows = cursor.fetchall()
        print(rows) 
        return render_template('station_admin_view_user.html',rows=rows)       
           

@app.route('/station_admin_accept_user_list',methods=['GET','POST'])
@allow_for_loggined_users_only
def station_admin_accept_user_list():
    if request.method == 'GET':        
        conn = mysql.connect()
        cursor = conn.cursor()     
        cursor.execute("select registration.*,login.*,station_user_map.*,station.* from station_user_map,login,registration,station where station_user_map.lid=registration.lid and registration.lid=login.lid and station_user_map.s_id=station.s_id and login.type='user' and login.provisionized=1 and station.s_id=%s",session['sid'])
        rows = cursor.fetchall()
        print(rows) 
        return render_template('station_admin_accept_user.html',rows=rows)   
          

@app.route('/user_registration',methods=['GET','POST'])
def user_registration():
    if request.method == 'GET':   
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM station")
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('user_registration.html',row=data)  
       
    if request.method == 'POST':
        data = request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        password=randomString(10) 
        date=datetime.datetime.now()
        print(date)
        img = request.files['files']
        filename = secure_filename(img.filename)
        print(os.path.join(app.config['path']  + filename))
        img.save(os.path.join(app.config['path']  + filename))
        query = "insert into login(username,password,provisionized,type,created_on) values (%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['name'], password, 0,'user',date))   
        employeeid=cursor.lastrowid
        query = "INSERT INTO registration(lid,name,gender,dob,email,phone,address,adharnumber,occupation,image,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (cursor.lastrowid,data['name'],data['radio'], data['dob'], data['email'], data['phone'], data['address'], data['adharnumber'],data['occupation'],filename,date))        
        query = "insert into station_user_map(lid,s_id,created_on) values (%s,%s,%s)"
        cursor.execute(query, (employeeid,data['sid'],date))          
        conn.commit()
        conn.close()
        return redirect(url_for('user_registration'))   
 
@app.route('/station_admin_accept_user', methods=['GET','POST'])  
def station_admin_accept_user():
    if request.method == 'POST':
        data=request.form['accept']
        data=data.split()
        print(data)
        conn=mysql.connect()
        cursor=conn.cursor()
        query="update login set provisionized=1 where lid="+data[0]
        cursor.execute(query)
        print(query)  
        conn.commit()
        return redirect(url_for('station_admin_manage_user'))
     
@app.route('/user_edit', methods=['GET','POST'])  
@allow_for_loggined_users_only
def user_edit():
    if request.method == 'GET':        
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select registration.*,login.lid,login.provisionized,login.type from login,registration where registration.lid=login.lid and login.type='user' and login.provisionized=1 and registration.lid=%s",session['lid'])
        data = cursor.fetchone()
        print(data)
        cursor.close()
        conn.close()
        return render_template('user_edit_profile.html',row=data)   
           

@app.route('/update_user_profile', methods=['POST'])  
def update_user_profile():
    if request.method == 'POST':
        conn=mysql.connect()
        cursor=conn.cursor()
        q="update registration set name='{}',gender='{}',dob='{}',email='{}',phone='{}',address='{}',adharnumber='{}',occupation='{}' where id='{}'"
        query = q.format(request.form.get("name"),
                             request.form.get("gender"),
                             request.form.get("dob"),
                             request.form.get("email"), 
                             request.form.get("phone"),
                             request.form.get("address"),
                             request.form.get("adharnumber"), 
                             request.form.get("occupation"),
                             request.form.get("id"))
        cursor.execute(query)
        # cursor.execute(query(data['name'],data['gender'],data['dob'],data['email'],data['phone'],data['address'],data['adharnumber'],data['occupation'],data['id']))
        print(query)  
        conn.commit()
        return redirect(url_for('user_edit'))     

@app.route('/advocate_registration', methods=['GET','POST'])
def advocate_registration():
    if request.method == 'GET':       
        return render_template('advocate_registration.html')              
    if request.method=='POST':
        data=request.form  
        conn = mysql.connect()
        cursor = conn.cursor()
        password=randomString(10) 
        date=datetime.datetime.now()
        print(date)
        img = request.files['files']
        filename = secure_filename(img.filename)
        print(os.path.join(app.config['path']  + filename))
        img.save(os.path.join(app.config['path']  + filename))
        query = "insert into login(username,password,provisionized,type,created_on) values (%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['name'], password, 0,'advocate',date))   
        advocateid=cursor.lastrowid
        query = "INSERT INTO registration(lid,name,gender,dob,email,phone,address,adharnumber,occupation,image,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (cursor.lastrowid,data['name'],data['radio'], data['dob'], data['email'], data['phone'], data['address'], data['adharnumber'],data['occupation'],filename,date))        
        query = "insert into advocate_info(lid,enrolment_year,practice_place,created_on) values (%s,%s,%s,%s)"
        cursor.execute(query, (advocateid,data['year'],data['practice_place'],date))          
        conn.commit()
        conn.close()
        return redirect(url_for('advocate_registration'))

@app.route('/advocate_admin_view_advocate', methods=['GET','POST'])  
@allow_for_loggined_users_only
def advocate_admin_view_advocate():
    if request.method == 'GET':        
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select registration.*,login.lid,login.provisionized,login.type,advocate_info.* from login,registration,advocate_info where registration.lid=login.lid and login.type='advocate' and login.provisionized=0 and advocate_info.lid=registration.lid")
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('advocate_admin_view_advocate.html',row=data)     
     


@app.route('/advocate_admin_ciew_accept_advocate', methods=['GET','POST'])
@allow_for_loggined_users_only  
def advocate_admin_ciew_accept_advocate():
    if request.method == 'GET':        
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select registration.*,login.lid,login.provisionized,login.type,advocate_info.* from login,registration,advocate_info where registration.lid=login.lid and login.type='advocate' and login.provisionized=1 and advocate_info.lid=registration.lid")
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('advocate_admin_ciew_accept_advocate.html',row=data)     
       

@app.route('/advocate_admin_view_advocate_rating', methods=['GET','POST']) 
@allow_for_loggined_users_only 
def advocate_admin_view_advocate_rating():
    if request.method == 'GET':        
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select registration.*,login.lid,login.provisionized,login.type,advocate_info.* from login,registration,advocate_info where registration.lid=login.lid and login.type='advocate' and login.provisionized=1 and advocate_info.lid=registration.lid")
        data = cursor.fetchall()            
        dt=[]
        for item in data:
          
            cursor.execute("select avg((rating/5)) as average, ROUND ((rating/5),1) as rating from advocate_rating where adv_id=%s",item[1])
            rating = cursor.fetchall()
           
            dt.append(
                {
                    "name":item[2],
                    "phone":item[5],
                    "address":item[6],
                    "rating":rating[0][1]
                    
                    
                }
            )
        print(dt)
        cursor.close()
        conn.close()
        return render_template('advocate_admin_view_advocate_rating.html',row=dt)     
       
     
# @app.route('/edit/<string:id>')
# def edit_view(id):
#     if request.method == 'GET':
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         cursor.execute("select avg((rating/5)) as average, ROUND ((rating/5),1) as rating from advocate_rating where adv_id=%s", id)
#         data = cursor.fetchall()
#         print(data)
#         cursor.close()
#         conn.close()
#         return render_template('advocate_admin_rating.html', row=data)

# @app.route('/advocate_admin_view_rating', methods=['GET','POST'])  
# def advocate_admin_view_rating():
#     if request.method == 'POST':
#             data=request.form
#             print(data['advid'])  
#             conn = mysql.connect()
#             cursor = conn.cursor()
#             cursor.execute("select avg((rating/5)) as average, ROUND ((rating/5),1) as rating from advocate_rating where adv_id=%s",data['advid'])
#             data = cursor.fetchall()
#             print(data)
#             cursor.close()
#             conn.close()
#             return render_template('advocate_admin_rating.html',data=data)  
  

@app.route('/advocate_admin_accept_advocate', methods=['GET','POST'])  
def advocate_admin_accept_advocate():
    if request.method == 'POST':
        data=request.form
        conn=mysql.connect()
        cursor=conn.cursor()
        query="update login set provisionized=1 where lid="+data['accept']
        cursor.execute(query)
        print(query)  
        conn.commit()
        conn.close()  
        
        return redirect(url_for('advocate_admin_view_advocate'))                        

@app.route('/advocate_admin_delete_advocate',methods=['POST'])
def advocate_admin_delete_advocate():
    if request.method == 'POST':
        data=request.form['delete_by_id']
        data=data.split()
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from advocate_info where aid=%s"
        cursor.execute(query, data[2])
        query = "delete from registration where id=%s"
        cursor.execute(query, data[0])
        query = "delete from login where lid=%s"
        cursor.execute(query, data[1])
        conn.commit()
        return redirect(url_for('advocate_admin_view_advocate'))   



@app.route('/user_add_complaint/<string:id>')  
@allow_for_loggined_users_only 
def user_add_complaint(id):
    if request.method == 'GET':            
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select registration.*,login.lid from login,registration where login.lid=registration.lid and registration.lid=%s",id)
        data = cursor.fetchone()
        print(data)
        cursor.close()
        conn.close()
        return render_template('user_add_advocate_complaint.html',row=data)  
          

@app.route('/user_add_complaint_againt_advocate',methods=['POST'] ) 
@allow_for_loggined_users_only 
def user_add_complaint_againt_advocate():        
    if request.method == 'POST': 
        data=request.form        
        conn=mysql.connect()
        cursor=conn.cursor()
        date=datetime.datetime.now()
        query = "INSERT INTO complaint_against_advocate(complainant_id,adv_id,complaint,created_on) VALUES(%s,%s,%s,%s)"        
        cursor.execute(query, (session['lid'],data['aid'],data['complaint'],date)) 
        print(query)  
        conn.commit()
        conn.close()
        return redirect(url_for('user_view_advocate')) 

@app.route('/user_add_spot_complaint',methods=['GET','POST'] )
@allow_for_loggined_users_only 
def user_add_spot_complaint():  
    if request.method == 'GET':            
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM station")
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('user_add_spot_complaint.html',row=data)
        # return render_template('user_add_spot_complaint.html')           
    if request.method == 'POST': 
        data=request.form        
        conn=mysql.connect()
        cursor=conn.cursor()
        files = request.files['files']
        filename = secure_filename(files.filename)
        print(os.path.join(app.config['path']  + filename))
        files.save(os.path.join(app.config['path']  + filename))
        date=datetime.datetime.now()
        query = "INSERT INTO quick_complaint(lid,complaint,image,created_on) VALUES(%s,%s,%s,%s)"        
        cursor.execute(query, (session['lid'],data['complaint'],filename,date)) 
        print(query)  
        conn.commit()
        conn.close()
        return redirect(url_for('user_add_spot_complaint')) 

@app.route('/station_admin_add_pettycases',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def station_admin_add_pettycases():  
    if request.method == 'GET':          
        return render_template('station_admin_add_pettycases.html')            
    if request.method == 'POST': 
        data=request.form        
        conn=mysql.connect()
        cursor=conn.cursor()            
        date=datetime.datetime.now()
        query = "INSERT INTO cases(case_type,subject,content,location,s_id,created_on) VALUES(%s,%s,%s,%s,%s,%s)"        
        cursor.execute(query, (data['casetype'],data['subject'],data['content'],data['location'],session['sid'],date)) 
        print(query)  
        conn.commit()
        conn.close()
        return redirect(url_for('station_admin_add_pettycases'))
        
@app.route('/station_admin_view_spot_complaints',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def station_admin_view_spot_complaints():  
    if request.method == 'GET':           
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select quick_complaint.* ,registration.* from quick_complaint,registration  where quick_complaint.lid=registration.lid ORDER BY quick_complaint.lid DESC")
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('station_admin_view_spot_complaints.html',row=data)


@app.route('/station_admin_view_complaints',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def station_admin_view_complaints():  
    if request.method == 'GET':           
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT  r.name,r.email,r.phone,nm.case_subject,nm.complaint,nm.status FROM normal_complaints as nm,registration as r,station_user_map as sm where nm.complainant_id=r.lid and nm.complainant_id=sm.lid and sm.s_id=(SELECT s_id FROM station_user_map where lid=%s)",session['lid'])
        normal = cursor.fetchall()
        cursor.execute("SELECT  r.name,r.email,r.phone,pc.complaint,pc.status FROM personalised_complaints as pc,registration as r,station_user_map as sm where pc.complainant_id=r.lid and pc.complainant_id=sm.lid and sm.s_id=(SELECT s_id FROM station_user_map where lid=%s)",session['lid'])
        personal = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('station_admin_view_complaints.html',normal=normal,personal=personal)
        

# @app.route('/station_admin_manage_cases',methods=['GET','POST'] ) 
# @allow_for_loggined_users_only 
# def station_admin_manage_cases():  
#     if request.method == 'GET':          
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM cases where s_id=%s",session['sid'])
#         data = cursor.fetchall()
#         print(data)
#         cursor.close()
#         conn.close()
#         return render_template('station_admin_manage_cases.html',row=data)      
                       
    
@app.route('/delete_station_admin_case',methods=['GET','POST'])  
@allow_for_loggined_users_only 
def delete_station_admin_case():
    if request.method=='POST':
        data=request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from cases where case_id=%s"
        cursor.execute(query, data['delete_by_id'])
        conn.commit()
        return redirect(url_for('station_admin_manage_cases'))

@app.route('/user_add_normal_complaint',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def user_add_normal_complaint():  
    if request.method == 'GET':            
        return render_template('user_add_normal_complaint.html')           
    if request.method == 'POST': 
        data=request.form        
        conn=mysql.connect()
        cursor=conn.cursor()            
        date=datetime.datetime.now()
        query = "INSERT INTO normal_complaints(complainant_id,case_subject,complaint,status,created_on) VALUES(%s,%s,%s,%s,%s)"        
        cursor.execute(query, (session['lid'],data['subject'],data['complaint'],'pending',date)) 
        print(query)  
        conn.commit()
        conn.close()
        return redirect(url_for('user_add_normal_complaint'))

        # not completed portion

@app.route('/station_admin_view_normal_complaint',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def station_admin_view_normal_complaint():  
    if request.method == 'GET':           
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select registration.*,login.*,station_user_map.*,station.*,normal_complaints.* from station_user_map,login,registration,station,normal_complaints where station_user_map.lid=registration.lid and registration.lid=login.lid and station_user_map.s_id=station.s_id and login.type='user' and login.provisionized=1 and registration.lid=normal_complaints.complainant_id and normal_complaints.status='pending' and station.s_id=%s",session['sid'])
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('station_admin_view_normal_complaint.html',row=data)
                 
    if request.method == 'POST': 
        data=request.form
        conn=mysql.connect()
        cursor=conn.cursor()
        query="update normal_complaints set status='accepted' where Normal_complaints_id="+data['status']
        cursor.execute(query)
        print(query)  
        conn.commit()
        conn.close()    
        return redirect(url_for('station_admin_view_normal_complaint'))  

@app.route('/station_admin_delete_normal_complaint',methods=['POST'])  
@allow_for_loggined_users_only 
def station_admin_delete_normal_complaint():
    if request.method=='POST':
        data=request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from normal_complaints where Normal_complaints_id=%s"
        cursor.execute(query, data['delete_by_id'])
        conn.commit()
        return redirect(url_for('station_admin_view_normal_complaint'))  


@app.route('/station_admin_view_personalize_complaint',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def station_admin_view_personalize_complaint():  
    if request.method == 'GET':          
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select registration.*,login.*,station_user_map.*,station.*,personalised_complaints.* from station_user_map,login,registration,station,personalised_complaints where station_user_map.lid=registration.lid and registration.lid=login.lid and station_user_map.s_id=station.s_id and login.type='user' and login.provisionized=1 and registration.lid=personalised_complaints.complainant_id and personalised_complaints.status='pending' and station.s_id=%s",session['sid'])
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('station_admin_view_personalize_complaint.html',row=data) 
              
    if request.method == 'POST': 
        data=request.form
        conn=mysql.connect()
        cursor=conn.cursor()
        query="update personalised_complaints set status='accepted' where Personalised_complaints_id="+data['status']
        cursor.execute(query)
        print(query)  
        conn.commit()
        conn.close()    
        return redirect(url_for('station_admin_view_personalize_complaint'))  

@app.route('/station_admin_delete_personalize_complaint',methods=['POST'])  
def station_admin_delete_personalize_complaint():
    if request.method=='POST':
        data=request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from personalised_complaints where Personalised_complaints_id=%s"
        cursor.execute(query, data['delete_by_id'])
        conn.commit()
        return redirect(url_for('station_admin_view_personalize_complaint'))  


# select registration.*,login.*,station_user_map.*,station.*,normal_complaints.* from station_user_map,login,registration,station,normal_complaints where station_user_map.lid=registration.lid and registration.lid=login.lid and station_user_map.s_id=station.s_id and login.type='user' and login.provisionized=1 and registration.lid=normal_complaints.complainant_id and station.s_id=4     
@app.route('/user_personalized_complaint',methods=['GET','POST']) 
@allow_for_loggined_users_only 
def user_personalized_complaint():  
    if request.method == 'GET':      
        return render_template('user_personalized_complaint.html')           
    if request.method == 'POST': 
        data=request.form        
        conn=mysql.connect()
        cursor=conn.cursor()            
        date=datetime.datetime.now()
        query = "INSERT INTO personalised_complaints(complainant_id,name,phone,email,parenetname,complaint,status,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"        
        cursor.execute(query, (session['lid'],data['name'],data['phone'],data['email'],data['parenetname'],data['complaint'],'pending',date)) 
        print(query)  
        conn.commit()
        conn.close()
        return redirect(url_for('user_personalized_complaint'))         

@app.route('/user_view_case_request',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def user_view_case_request():  
    if request.method == 'GET':           
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cases")
        data = cursor.fetchall()
        cursor.execute("select login.lid,login.type,registration.*,advocate_info.* from advocate_info,registration,login where login.lid=registration.lid and registration.lid=advocate_info.lid and login.type='advocate'")
        data1 = cursor.fetchall()
        cursor.execute("SELECT r.name,request_type,case_type,subject,content,location,st.name,ar.status FROM advocate_request as ar,registration as r,cases as c ,station as st where ar.adv_id=r.lid and c.s_id=st.s_id and ar.case_id=c.case_id and ar.req_id=%s",session['lid'])
        cases = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('user_view_case_request.html',row=data,row1=data1,cases=cases)  
          
    if request.method == 'POST':  
        data=request.form        
        conn=mysql.connect()
        cursor=conn.cursor()            
        date=datetime.datetime.now()
        query = "INSERT INTO advocate_request(req_id,adv_id,request_type,case_id,created_on,status) VALUES(%s,%s,%s,%s,%s,%s)"        
        cursor.execute(query, (session['lid'],data['advid'],data['request'],data['caseid'],date,'pending')) 
        print(query)  
        conn.commit()
        conn.close()
        return redirect(url_for('user_view_case_request'))

@app.route('/advocate_edit', methods=['GET','POST'])  
@allow_for_loggined_users_only 
def advocate_edit():
    if request.method == 'GET':        
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select registration.*,login.lid,login.provisionized,login.type,advocate_info.* from login,registration,advocate_info where registration.lid=login.lid and login.type='advocate' and login.provisionized=1 and advocate_info.lid=registration.lid and registration.lid=%s",session['lid'])
        data = cursor.fetchone()
        print(data)
        cursor.close()
        conn.close()
        return render_template('advocate_profile.html',row=data)    
              

@app.route('/update_advocate_edit', methods=['POST'])  
def update_advocate_edit():
    if request.method == 'POST':
        conn=mysql.connect()
        cursor=conn.cursor()
        q="update registration set name='{}',gender='{}',dob='{}',email='{}',phone='{}',address='{}',adharnumber='{}',occupation='{}' where id='{}'"
        query = q.format(request.form.get("name"),
                             request.form.get("gender"),
                             request.form.get("dob"),
                             request.form.get("email"), 
                             request.form.get("phone"),
                             request.form.get("address"),
                             request.form.get("adharnumber"), 
                             request.form.get("occupation"),
                             request.form.get("id"))
        cursor.execute(query)
        q="update advocate_info set enrolment_year='{}',practice_place='{}' where aid='{}'"
        query = q.format(request.form.get("entolment"),
                             request.form.get("practice"),                            
                             request.form.get("aid"))
        cursor.execute(query)
        print(query)  
        conn.commit()
        return redirect(url_for('advocate_edit'))   


@app.route('/advocate_view_case_request',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def advocate_view_case_request():  
    if request.method == 'GET':           
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.provisionized,login.type,registration.*,advocate_request.*,cases.* from advocate_request,registration,login,cases where login.lid=registration.lid and registration.lid=advocate_request.req_id and cases.case_id=advocate_request.case_id and advocate_request.status='pending' and advocate_request.adv_id=%s",session['lid'])
        
        data = cursor.fetchall()
        cursor.execute("select login.lid,login.provisionized,login.type,registration.*,advocate_request.*,cases.* from advocate_request,registration,login,cases where login.lid=registration.lid and registration.lid=advocate_request.req_id and cases.case_id=advocate_request.case_id and advocate_request.status='accepted' and advocate_request.adv_id=%s",session['lid'])
        cases = cursor.fetchall()
        conn.close()
        return render_template('advocate_view_case_request.html',row=data,cases=cases) 
          
    if request.method=='POST':
        conn=mysql.connect()
        cursor=conn.cursor()
        data=request.form['arid']
        data=data.split()
        query="update advocate_request set status='"+str(data[1])+"' where ar_id="+data[0]                        
        cursor.execute(query)
        print(query)
        query="update advocate_request set status='"+str(data[1])+"' where ar_id="+data[0]                        
        cursor.execute(query)
        cursor.execute(query)
        print(query)
        conn.commit()
        return redirect(url_for('advocate_view_case_request'))     

# page cross check
@app.route('/advocate_admin_view_advocate_complaint',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def advocate_admin_view_advocate_complaint():  
    if request.method == 'GET':          
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,registration.*,complaint_against_advocate.*,advocate_info.* from complaint_against_advocate,registration,login,advocate_info where registration.lid=login.lid and registration.lid=complaint_against_advocate.adv_id and registration.lid=advocate_info.lid")
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('advocate_admin_view_advocate_complaint.html',row=data) 
         

@app.route('/user_add_system_complaint',methods=['GET','POST'] )
@allow_for_loggined_users_only  
def user_add_system_complaint():  
    if request.method == 'GET':               
        return render_template('user_add_system_complaint.html')                
    if request.method == 'POST':
        data=request.form        
        conn=mysql.connect()
        cursor=conn.cursor()            
        date=datetime.datetime.now()
        query = "INSERT INTO complaints_feedback(complainant_id,complaint,reply,created_on,replied_on) VALUES(%s,%s,%s,%s,%s)"        
        cursor.execute(query, (session['lid'],data['complaint'],'',date,date)) 
        print(query)  
        conn.commit()
        conn.close()
        return redirect(url_for('user_add_system_complaint'))

@app.route('/admin_view_and_reply_complaint',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def admin_view_and_reply_complaint():  
    if request.method == 'GET':          
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from complaints_feedback")
        row = cursor.fetchall()
        # print(row)
        conn.commit()
        conn.close()      
        return render_template('admin_view_and_reply_complaint.html',row=row) 
               
    if request.method == 'POST':    
        print(request.json)
        data = request.json
        conn =mysql.connect()
        cursor = conn.cursor()
        q=" UPDATE complaints_feedback SET reply ='{}',replied_on='{}' WHERE complaints_feedback_id='{}'"
        query= q.format(data['reply'],datetime.datetime.now(),data['complaint_id'])                        
        print(query)
        cursor.execute(query)
        conn.commit()
        conn.close()
        return redirect(url_for('admin_view_and_reply_complaint')) 

@app.route('/user_add_complaint_against_individual',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def user_add_complaint_against_individual():  
    if request.method == 'GET':              
        return render_template('user_add_complaint_against_individual.html')            
    if request.method == 'POST':
        data=request.form        
        conn=mysql.connect()
        cursor=conn.cursor()            
        date=datetime.datetime.now()
        query = "INSERT INTO case_against_individuals(case_type,name,phone,email,parent_name,details,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s)"        
        cursor.execute(query, (data['casetype'],data['name'],data['phone'],data['email'],data['parenetname'],data['details'],date)) 
        print(query)  
        conn.commit()
        conn.close()
        return redirect(url_for('user_add_complaint_against_individual'))       

@app.route('/admin_view_individual_cases',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def admin_view_individual_cases():  
    if request.method == 'GET':           
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from case_against_individuals")
        row = cursor.fetchall()
        conn.commit()
        conn.close()   
        return render_template('admin_view_individual_cases.html',row=row) 
          

@app.route('/admin_add_more_individual_cases',methods=['GET','POST'] )
@allow_for_loggined_users_only 
def admin_add_more_individual_cases():  
    if request.method == 'GET':         
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from case_against_individuals")
        row = cursor.fetchone()
        cursor.execute("SELECT * FROM station")
        rows = cursor.fetchall()
        conn.commit()
        conn.close()   
        return render_template('admin_add_more_individual_cases.html',row=row,rows=rows) 
     
    if request.method == 'POST': 
        data=request.form        
        conn=mysql.connect()
        cursor=conn.cursor()            
        date=datetime.datetime.now()
        query = "INSERT INTO case_involve(c_id,name,phone,email,address,parent_name,details,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"        
        cursor.execute(query, (data['cid'],data['name'],data['phone'],data['email'],data['address'],data['parenetname'],data['details'],date)) 
        query = "INSERT INTO cases(case_type,case_involver,number,subject,content,location,s_id,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"        
        cursor.execute(query, (data['casetype'],data['name'],data['phone'],data['subject'],data['content'],data['location'],data['sid'],date)) 
        print(query)  
        conn.commit()
        conn.close()
        return redirect(url_for('admin_add_more_individual_cases'))

@app.route('/delete_admin_view_individual_case',methods=['POST'])  
def delete_admin_view_individual_case():
    if request.method=='POST':
        data=request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from case_against_individuals where c_id=%s"
        cursor.execute(query, data['delete_by_id'])
        conn.commit()
        return redirect(url_for('admin_view_individual_cases'))          

@app.route('/admin_view_user',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def admin_view_user():  
    if request.method == 'GET':          
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.provisionized,login.type,registration.* from registration,login where login.lid=registration.lid and login.type='user' and login.provisionized=1")
        row = cursor.fetchall()
        conn.commit()
        conn.close()   
        return render_template('admin_view_user.html',row=row) 
    # if request.method == 'POST':
    #     conn = mysql.connect()
    #     cursor = conn.cursor()
    #     query = "DELETE FROM login, advocate_rating WHERE lid=%s AND user_id=%s"
    #     cursor.execute(query, request.form.get('delete_by_id'))
    #     conn.commit()
    #     conn.close()
    #     return redirect(url_for('admin_view_user'))                     
        

@app.route('/admin_manage_personal_complaint',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def admin_manage_personal_complaint():  
    if request.method == 'GET':          
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,registration.*,personalised_complaints.* from registration,login,personalised_complaints where registration.lid=login.lid and registration.lid=personalised_complaints.complainant_id and personalised_complaints.status='pending' ")
        row = cursor.fetchall()
        conn.commit()
        conn.close()   
        return render_template('admin_manage_personal_complaint.html',row=row)                   
       


@app.route('/admin_accept_personalice_complaint', methods=['GET','POST'])  
def admin_accept_personalice_complaint():
    if request.method == 'POST':
        data=request.form
        print(data)
        conn=mysql.connect()
        cursor=conn.cursor()
        query="update personalised_complaints set status='accepted' where Personalised_complaints_id="+data['accept']
        cursor.execute(query)
        print(query)  
        conn.commit()
        return redirect(url_for('admin_manage_personal_complaint'))

@app.route('/admin_reject_personalice_complaint', methods=['GET','POST'])  
def admin_reject_personalice_complaint():
    if request.method == 'POST':
        data=request.form
        print(data)
        conn=mysql.connect()
        cursor=conn.cursor()
        query="update personalised_complaints set status='reject' where Personalised_complaints_id="+data['reject']
        cursor.execute(query)
        print(query)  
        conn.commit()
        return redirect(url_for('admin_manage_personal_complaint'))

@app.route('/admin_manage_normal_complaint',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def admin_manage_normal_complaint():  
    if request.method == 'GET':          
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,registration.*,normal_complaints.* from registration,login,normal_complaints where registration.lid=login.lid and registration.lid=normal_complaints.complainant_id and normal_complaints.status='pending' ")
        row = cursor.fetchall()
        conn.commit()
        conn.close()   
        return render_template('admin_manage_normal_complaint.html',row=row)                   
          

@app.route('/admin_accept_normal_complaint', methods=['GET','POST'])  
def admin_accept_normal_complaint():
    if request.method == 'POST':
        data=request.form
        print(data)
        conn=mysql.connect()
        cursor=conn.cursor()
        query="update normal_complaints set status='accepted' where Normal_complaints_id="+data['accept']
        cursor.execute(query)
        print(query)  
        conn.commit()
        return redirect(url_for('admin_manage_normal_complaint'))

@app.route('/admin_reject_normal_complaint', methods=['GET','POST'])  
def admin_reject_normal_complaint():
    if request.method == 'POST':
        data=request.form
        print(data)
        conn=mysql.connect()
        cursor=conn.cursor()
        query="update normal_complaints set status='reject' where Normal_complaints_id="+data['reject']
        cursor.execute(query)
        print(query)  
        conn.commit()
        return redirect(url_for('admin_manage_normal_complaint'))   

@app.route('/admin_view_spot_complaints',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def admin_view_spot_complaints():  
    if request.method == 'GET':          
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select quick_complaint.* ,registration.* from quick_complaint,registration where quick_complaint.lid=registration.lid")
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('admin_view_quick_complaint.html',row=data)  
        

@app.route('/user_view_complaints',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def user_view_complaints():  
    if request.method == 'GET':         
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quick_complaint where lid=%s",session['lid'])
        spot = cursor.fetchall()
        cursor.execute("SELECT * FROM normal_complaints where complainant_id=%s",session['lid'])
        normal = cursor.fetchall()
        cursor.execute("SELECT * FROM personalised_complaints where complainant_id=%s",session['lid'])
        personal = cursor.fetchall()
        cursor.execute("SELECT  r.name,c.complaint,c.created_on FROM complaint_against_advocate as c,registration as r where c.adv_id=r.lid and complainant_id=%s",session['lid'])
        advocate = cursor.fetchall()
        cursor.execute("SELECT * FROM complaints_feedback where complainant_id=%s",session['lid'])
        system = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('user_view_complaints.html',spot=spot,normal=normal,personal=personal,advocate=advocate,system=system) 

@app.route('/user_view_advocate', methods=['GET','POST'])  
@allow_for_loggined_users_only 
def user_view_advocate():
    if request.method == 'GET':        
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,login.provisionized,registration.*,advocate_info.* from advocate_info,registration,login where login.lid=registration.lid and registration.lid=advocate_info.lid and login.type='advocate' and login.provisionized=1")
        data = cursor.fetchall()
        print(data)
        cursor.execute("select login.lid,registration.* from registration,login where login.lid=registration.lid and registration.lid=%s",session['lid'])
        datas = cursor.fetchone()
        print(datas)
        # print(session['lid'])
        cursor.close()
        conn.close()
        return render_template('user_view_advocate.html',row=data,row1=datas)
         
    if request.method == 'POST':
        data=request.json
        print(data)        
        conn=mysql.connect()
        cursor=conn.cursor()
        date=datetime.datetime.now()       
        query = "INSERT INTO advocate_rating(user_id,adv_id,rating,created_on) VALUES(%s,%s,%s,%s)"        
        cursor.execute(query, (data['lid'],data['advid'],data['rating'],date)) 
        print(query)  
        conn.commit()
        conn.close()  
        return 'ok'
        # return redirect(url_for('user_view_advocate'))  


@app.route('/user_view_rate',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def user_view_rate():  
    if request.method == 'GET':         
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select avg((rating/5)) as average, ROUND ((rating/5),1) as rating from advocate_rating where adv_id=%s",session['lid'])
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('advocate_view_rating.html',row=data)  
       


@app.route('/advocate_view_rating',methods=['GET','POST'] ) 
@allow_for_loggined_users_only 
def advocate_view_rating():  
    if request.method == 'GET':          
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select avg((rating/5)) as average, ROUND ((rating/5),1) as rating from advocate_rating where adv_id=%s",session['lid'])
        data = cursor.fetchall()
        print(data)
        cursor.close()
        conn.close()
        return render_template('advocate_view_rating.html',row=data)  
                                   
# @app.route('/forgotpassword',methods=['POST', 'GET'])
# def forgoatemail():
#     if request.method == 'GET': 
#         return render_template("forgetpassword.html")
    # if request.method == 'POST': 
    #     data=request.form
    #     conn = mysql.connect()
    #     cursor = conn.cursor()
    #     print(request.form)       
    #     query = "select * from login where username='" + \
    #         str(request.form['email'])+"'"
    #     cursor.execute(query)
    #     data = cursor.fetchall()
    #     conn.close()
    #     print(data)
    #     if len(data) > 0:
    #         out = []
    #         out.append(data[0][1])
    #         msg = Message('Password Recovery',
    #                       sender='stichit4321@gmail.com', recipients=out)
    #         msg.body = "we are attaching your password with this mail, please check --->" + \
    #             str(data[0][2])
    #         mail.send(msg)
    #     return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)     