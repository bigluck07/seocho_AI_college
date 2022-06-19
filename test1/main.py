from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123', db='web_test', charset="utf8")
cursor = db.cursor()

@app.route("/page", methods=["GET"])
def mainPage():
    return render_template('index.html')

@app.route("/student", methods=["GET"])
def get_students():
    sql = "select * from student_score"
    cursor.execute(sql)
    results = cursor.fetchall()
    students = []
    for res in results:
        students.append({
            'name':res[0],
            'Kor':res[1],
            'Math':res[2],
            'Eng':res[3]
        })
    return jsonify(students)

@app.route("/student", methods=["POST"])
# body로부터 학생이름과 성적을 받아 DB에 저장하고 마지막으로 OK를 반환합니다.
def svae_student():
    server_name = request.form["name"]
    server_Kor = request.form["Kor"]
    server_Math = request.form["Math"]
    server_Eng = request.form["Eng"]
    sql = """ insert into student_score (name, Kor, Math, Eng) values ('%s', %s, %s, %s) """ % (server_name, server_Kor, server_Math, server_Eng)
    cursor.execute(sql)
    db.commit()
    return "OK"


@app.route("/student", methods=["DELETE"])
def dlt_student():
    server_name = request.form["name"]
    sql = "delete from student_score where name='%s'" % server_name
    cursor.execute(sql)
    db.commit()
    return "OK"


@app.route("/student", methods=["PUT"])
def udt_student():
    server_name = request.form["name"]
    server_Kor = request.form["Kor"]
    server_Math = request.form["Math"]
    server_Eng = request.form["Eng"]

    sql = "update student_score set Kor=%s, Math=%s, Eng=%s where name='%s'" % (server_Kor,server_Math,server_Eng,server_name)
    cursor.execute(sql)
    db.commit()
    return "OK"


@app.route("/student", methods=["PATCH"])
def sort_students():
    server_check = request.form["ref_code"]
    sql2 = "select * from student_score order by %s" % server_check
    cursor.execute(sql2)
    results2 = cursor.fetchall()
    students2 = []
    for res in results2:
        students2.append({
            'name':res[0],
            'Kor':res[1],
            'Math':res[2],
            'Eng':res[3]
        })
    return jsonify(students2)



if __name__ == "__main__":
    app.run(debug=True)