from flask import Flask,render_template,request,redirect
from flask_mysqldb import MySQL
import yaml

# Instantiate an object to run flask app
app=Flask(__name__)

#Configure Db 
with open('db.yaml', 'r') as file:
    config = yaml.safe_load(file)
app.config['MYSQL_HOST']=config['mysql_host']
app.config['MYSQL_USER']=config['mysql_user']
app.config['MYSQL_PASSWORD']=config['mysql_password']
app.config['MYSQL_DB']=config['mysql_db']

#creating an object
mysql=MySQL(app)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        #Fetch data from form 
        # if GET then it will be for user 
        # if POST then it will get sotred in database
        userDetails=request.form
        name=userDetails['name']
        email=userDetails['email']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,email) VALUES(%s,%s)",(name,email))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')

    return render_template('index.html')

@app.route('/users')
def users():
    cur=mysql.connection.cursor()
    resultValue=cur.execute("SELECT * FROM users")
    if resultValue>0:
        userDetails=cur.fetchall()
        return render_template('users.html',userDetails=userDetails)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)