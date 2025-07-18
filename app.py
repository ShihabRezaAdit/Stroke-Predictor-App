# save this as app.py
from flask import Flask, escape, request, render_template, redirect, url_for, session
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
import re
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

model = pickle.load(open('model_pickle.pkl', 'rb'))
app = Flask(__name__)

# app.secret_key = 'xyzsdfg'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'stroke'
  
#mysql = MySQL(app)

#@app.route('/')
# @app.route('/login', methods =['GET', 'POST'])
# def login():
#     mesage = ''
#     if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
#         email = request.form['email']
#         password = request.form['password']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
#         user = cursor.fetchone()
#         if user:
#             session['loggedin'] = True
#             session['userid'] = user['userid']
#             session['name'] = user['name']
#             session['email'] = user['email']
#             mesage = 'Logged in successfully !'
#             return render_template('index.html', mesage = mesage)
#         else:
#             mesage = 'Please enter correct email / password !'
#     return render_template('login.html', mesage = mesage)



# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('userid', None)
#     session.pop('email', None)
#     return redirect(url_for('login'))



# @app.route('/register', methods =['GET', 'POST'])
# def register():
#     mesage = ''
#     if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
#         userName = request.form['name']
#         password = request.form['password']
#         email = request.form['email']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
#         account = cursor.fetchone()
#         if account:
#             mesage = 'Account already exists !'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             mesage = 'Invalid email address !'
#         elif not userName or not password or not email:
#             mesage = 'Please fill out the form !'
#         else:
#             cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
#             mysql.connection.commit()
#             mesage = 'You have successfully registered !'
#     elif request.method == 'POST':
#         mesage = 'Please fill out the form !'
#     return render_template('register.html', mesage = mesage)




@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

    
@app.route('/analysis', methods=['GET', 'POST'])
def analysis():

    if request.method =="POST":
        gender = request.form['gender']
        age = float(request.form['age'])
        hypertension = int(request.form['hypertension'])
        heart_disease = int(request.form['heart_disease'])
        ever_married_Yes = request.form['ever_married_Yes']
        work = request.form['work']
        residence = request.form['residence']
        avg_glucose_level = float(request.form['avg_glucose_level'])
        bmi = float(request.form['bmi'])
        smoking = request.form['smoking']

        # gender
        if (gender == "Male"):
            gender_Male=1
            gender_Other=0
        else:
            gender_Male=0
            gender_Other=1
        
        # married
        if(ever_married_Yes=="Yes"):
            ever_married_Yes = 1
        else:
            ever_married_Yes=0

        # work  type
        if(work=='Self-employed'):
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 1
            work_type_children=0
        elif(work == 'Private'):
            work_type_Never_worked = 0
            work_type_Private = 1
            work_type_Self_employed = 0
            work_type_children=0
        elif(work=="children"):
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children=1
        elif(work=="Never_worked"):
            work_type_Never_worked = 1
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children=0
        else:
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children=0

        # residence type
        if (residence=="Urban"):
            Residence_type_Urban=1
        else:
            Residence_type_Urban=0

        # smoking status
        if(smoking=='formerly smoked'):
            smoking_status_formerly_smoked = 1
            smoking_status_never_smoked = 0
            smoking_status_smokes = 0
        elif(smoking == 'smokes'):
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 0
            smoking_status_smokes = 1
        elif(smoking=="never smoked"):
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 1
            smoking_status_smokes = 0
        else:
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 0
            smoking_status_smokes = 0

        
        feature = np.array([[age, hypertension, heart_disease, avg_glucose_level, bmi, gender_Male, gender_Other, ever_married_Yes, work_type_Never_worked, work_type_Private, work_type_Self_employed, work_type_children, Residence_type_Urban,smoking_status_formerly_smoked, smoking_status_never_smoked, smoking_status_smokes]])

        prediction = model.predict(feature)
        
        #return render_template('result.html', prediction=prediction, gender=gender, age=age, hypertension=hypertension, heart_disease=heart_disease, ever_married_Yes=ever_married_Yes, work=work, residence=residence, avg_glucose_level=avg_glucose_level, bmi=bmi, smoking=smoking)
        return render_template("stroke.html")
    else:
        return render_template("stroke.html")
    
    
    
@app.route('/')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method =="POST":
        gender = request.form['gender']
        age = float(request.form['age'])
        hypertension = int(request.form['hypertension'])
        heart_disease = int(request.form['heart_disease'])
        ever_married_Yes = request.form['ever_married_Yes']
        work = request.form['work']
        residence = request.form['residence']
        avg_glucose_level = float(request.form['avg_glucose_level'])
        bmi = float(request.form['bmi'])
        smoking = request.form['smoking']

        # gender
        if (gender == "Male"):
            gender_Male=1
            gender_Other=0
        else:
            gender_Male=0
            gender_Other=1
        
        # married
        if(ever_married_Yes=="Yes"):
            ever_married_Yes = 1
        else:
            ever_married_Yes=0

        # work  type
        if(work=='Self-employed'):
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 1
            work_type_children=0
        elif(work == 'Private'):
            work_type_Never_worked = 0
            work_type_Private = 1
            work_type_Self_employed = 0
            work_type_children=0
        elif(work=="children"):
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children=1
        elif(work=="Never_worked"):
            work_type_Never_worked = 1
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children=0
        else:
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children=0

        # residence type
        if (residence=="Urban"):
            Residence_type_Urban=1
        else:
            Residence_type_Urban=0

        # smoking status
        if(smoking=='formerly smoked'):
            smoking_status_formerly_smoked = 1
            smoking_status_never_smoked = 0
            smoking_status_smokes = 0
        elif(smoking == 'smokes'):
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 0
            smoking_status_smokes = 1
        elif(smoking=="never smoked"):
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 1
            smoking_status_smokes = 0
        else:
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 0
            smoking_status_smokes = 0

        
        feature = np.array([[age, hypertension, heart_disease, avg_glucose_level, bmi, gender_Male, gender_Other, ever_married_Yes, work_type_Never_worked, work_type_Private, work_type_Self_employed, work_type_children, Residence_type_Urban,smoking_status_formerly_smoked, smoking_status_never_smoked, smoking_status_smokes]])

        prediction = model.predict(feature)
        
        return render_template('result.html', prediction=prediction, gender=gender, age=age, hypertension=hypertension, heart_disease=heart_disease, ever_married_Yes=ever_married_Yes, work=work, residence=residence, avg_glucose_level=avg_glucose_level, bmi=bmi, smoking=smoking)
        #return render_template("stroke.html")
    else:
        return render_template("index.html")





if __name__ == "__main__":
    app.run(debug=False)