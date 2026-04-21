from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# 🔹 DATABASE CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shraddha@0712",  
    database="student_management"
)

cursor = db.cursor()

# 🔹 HOME PAGE
@app.route('/')
def home():
    return render_template('home.html')

# 🔹 ADD STUDENT
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        course_id = request.form['course_id']

        cursor.execute(
            "INSERT INTO students (name, age, email) VALUES (%s, %s, %s)",
            (name, age, email)
        )
        db.commit()

        student_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)",
            (student_id, course_id)
        )
        db.commit()

        return redirect('/students')

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    return render_template('add_student.html', courses=courses)

# 🔹 VIEW STUDENTS
@app.route('/students')
def students():
    query = """
    SELECT s.student_id, s.name, s.age, s.email, c.course_name
    FROM students s
    JOIN enrollments e ON s.student_id = e.student_id
    JOIN courses c ON e.course_id = c.course_id
    """
    cursor.execute(query)
    data = cursor.fetchall()

    return render_template('students.html', students=data)

# 🔹 SEARCH
@app.route('/search')
def search():
    name = request.args.get('name')

    query = "SELECT * FROM students WHERE name LIKE %s"
    cursor.execute(query, ('%' + name + '%',))
    data = cursor.fetchall()

    return render_template('students.html', students=data)

# 🔹 RUN APP
if __name__ == '__main__':
    app.run(debug=True)