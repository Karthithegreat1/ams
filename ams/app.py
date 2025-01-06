from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from flask_mail import Mail, Message
import os
from datetime import date

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Email Configuration (Hardcoded)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'manokarthick.ks741@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'hyul ocro hrow bnah'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'manokarthick.ks741@gmail.com'  # Default sender address

mail = Mail(app)

# MySQL Database Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Your MySQL username
    password="karthick2002",  # Your MySQL password
    database="attendance_system"
)

cursor = db.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    cursor.execute("SELECT * FROM staff WHERE username=%s AND password=%s", (username, password))
    staff = cursor.fetchone()

    if staff:
        return redirect(url_for('attendance'))
    else:
        flash('Invalid login credentials')
        return redirect(url_for('login'))

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    student_id = request.args.get('student_id')  # Get the student ID from the URL parameters
    student = None

    if student_id:
        # Query the students table using the correct column name 'id' instead of 'student_id'
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cursor.fetchone()

    cursor.execute("SELECT * FROM students")  # Fetch all students for the dropdown
    students = cursor.fetchall()
    
    return render_template('attendance.html', student=student, students=students)

@app.route('/submit_attendance', methods=['POST'])
def submit_attendance():
    present_students = request.form.getlist('present')
    cursor.execute("SELECT * FROM students")
    all_students = cursor.fetchall()

    today = date.today()

    for student in all_students:
        student_id, name, email, _ = student
        status = 'present' if str(student_id) in present_students else 'absent'
        
        # Insert attendance record into the attendance table using 'id' (primary key) for student_id
        cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)", 
                       (student_id, today, status))
        db.commit()

        if status == 'absent':
            send_email(email, name)

    return redirect(url_for('success'))


    # Collect present and absent students based on dropdown selection
    for student in all_students:
        student_id, name, email, _ = student
        attendance_status = request.form.get(f'attendance_{student_id}')
        
        if attendance_status == 'present':
            present_students.append(student_id)
            status = 'present'
        else:
            absent_students.append(student_id)
            status = 'absent'

        # Insert attendance record into the attendance table
        cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)", 
                       (student_id, today, status))
        db.commit()

        # Send email if the student is absent
        if status == 'absent':
            send_email(email, name)

    return redirect(url_for('success'))


def send_email(student_email, student_name):
    msg = Message(
        f'Absence Notification for {student_name}',
        recipients=[student_email]
    )
    msg.body = f'Hello {student_name},\n\nYou were marked absent today.\nPlease ensure to attend the classes regularly.'
    mail.send(msg)

@app.route('/success')
def success():
    return render_template('success.html')

# New Route for Add Student Form
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cursor.execute("INSERT INTO students (name, email) VALUES (%s, %s)", (name, email))
        db.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('attendance'))

    return render_template('add_student.html')

# New Route for Success after adding student
@app.route('/student_added')
def student_added():
    return render_template('student_added.html')

if __name__ == '__main__':
    app.run(debug=True,port=8000)
