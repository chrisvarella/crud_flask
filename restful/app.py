from flask import Flask, request
from flask_mysqldb import MySQL

import pymysql
#from app import app
#from db_config import mysql
from flask import jsonify
#from flask import flash

app = Flask(__name__)


#
#from flask import Flask, render_template, request
#from flask_mysqldb import MySQL
#
#app = Flask(__name__)


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'EnterpriseSystems'

mysql = MySQL(app)


@app.route('/selectstudents')
def selectstudents():
	try:
		cursor = mysql.connection.cursor()
		cursor.execute("SELECT * FROM student")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)



@app.route('/student/<idstudent>')
def student(idstudent):
	try:
		cursor = mysql.connection.cursor()
		cursor.execute("SELECT * FROM student WHERE student_id = %s", idstudent)
		row = cursor.fetchall()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)



@app.route('/insertstudent', methods=['POST'])
def insertstudent():
	try:
		json = request.json

		firstName = json['fname']
		lastName = json['lname']
		dateBirth = json['dob']
		amountDue = json['amount']

		sql = "INSERT INTO Student(first_name, last_name, dob, amount_due) VALUES (%s, %s, %s, %s)"
		data = (firstName, lastName, dateBirth, amountDue)

		cursor = mysql.connection.cursor()
		cursor.execute(sql, data)
		mysql.connection.commit()

		resp = jsonify('Student added successfully!')
		resp.status_code = 200
		return resp

	except Exception as e:
		print(e)




@app.route('/updatestudent', methods=['POST'])
def updatestudent():
	try:
		json = request.json

		idstudent = json['idstudent']
		firstName = json['fname']
		lastName = json['lname']
		dateBirth = json['dob']
		amountDue = json['amount']

		sql = "UPDATE Student SET first_name = %s, last_name = %s, dob = %s, amount_due = %s WHERE student_id = %s"
		data = (firstName, lastName, dateBirth, amountDue, idstudent)

		cursor = mysql.connection.cursor()
		cursor.execute(sql, data)
		mysql.connection.commit()

		resp = jsonify('Student updated successfully!')
		resp.status_code = 200
		return resp
    
	except Exception as e:
		print(e)


		
@app.route('/deletestudent/<idstudent>')
def deletestudent(idstudent):
	try:
		cursor = mysql.connection.cursor()
		cursor.execute("DELETE FROM student WHERE student_id =  %s" % (idstudent))
		mysql.connection.commit()

		resp = jsonify('Student deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)


		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
    

if __name__ == '__main__':
    app.run(debug=True)