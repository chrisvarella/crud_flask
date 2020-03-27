from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'EnterpriseSystems'

mysql = MySQL(app)

@app.route('/')
def liststudents():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM student''')
    data = cur.fetchall()

    return render_template('select.html', data=data)



@app.route('/select')
def selectstudents():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM student''')
    data = cur.fetchall()

    return render_template('select.html', data=data)



@app.route('/insert')
def insert():
    return render_template('insert.html')



@app.route('/insertstudent', methods=['GET', 'POST'])
def insertstudent():
    if request.method == "POST":
        details = request.form
        
        firstName = details['fname']
        lastName = details['lname']
        dateBirth = details['dob']
        amountDue = details['amount']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Student(first_name, last_name, dob, amount_due) VALUES (%s, %s, %s, %s)", (firstName, lastName, dateBirth, amountDue))        
        mysql.connection.commit()
        cur.close()

        return render_template('success.html')



@app.route('/delete/<idstudent>', methods=['GET', 'POST'])
def delete(idstudent):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE student_id = %s", (idstudent))
    data = cur.fetchall()

    return render_template('delete.html', data=data)


@app.route('/deletestudent', methods=['GET', 'POST'])
def deletestudent():
    if request.method == "POST":
        details = request.form
        
        idstudent = details['idstudent']
        
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM student WHERE student_id =  %s", (idstudent))       
        mysql.connection.commit()
        cur.close()

        return render_template('success.html')



@app.route('/update/<idstudent>', methods=['GET', 'POST'])
def update(idstudent):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE student_id = %s", (idstudent))
    data = cur.fetchall()

    return render_template('update.html', data=data)


@app.route('/updatestudent', methods=['GET', 'POST'])
def updatestudent():
    if request.method == "POST":
        details = request.form
        
        idstudent = details['idstudent']
        firstName = details['fname']
        lastName = details['lname']
        dateBirth = details['dob']
        amountDue = details['amount']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Student SET first_name = %s, last_name = %s, dob = %s, amount_due = %s WHERE student_id = %s", (firstName, lastName, dateBirth, amountDue, idstudent))        
        mysql.connection.commit()
        cur.close()

        return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)