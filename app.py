import os
from HW12 import University
from flask import Flask, render_template

cwd = os.getcwd()
Stevens = University(cwd, web=True, pt=False)

app = Flask(__name__)


@app.route('/')
def intro():
    return render_template('index.html', title="Stevens Repository", table_title="Stevens Repository")


@app.route('/students')
def student_courses():
    return render_template('students.html', title="Stevens Repository", table_title="Student Summary",
                           data=Stevens.student_data)


@app.route('/instructors')
def instructor_courses():
    return render_template('instructors.html', title="Stevens Repository", table_title="Professor Summary",
                           data=Stevens.instructor_data)


if __name__ == '__main__':
    app.run(debug=False)
