from flask import Flask, render_template, request, jsonify
import pymysql


def showDB_func():

    rows = []

    config = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "260203",
        "db_name": "test",
    }
    try:
        connection = pymysql.connect(
            host=config.get("host"),
            port=config.get("port"),
            user=config.get("user"),
            password=config.get("password"),
            database=config.get("db_name"),
        )

    except:
        return "false"

    # Работа с ajax запросом
    if request.is_json:

        if request.method == "POST":
            jsonDictionary = request.get_json()
            type_key = jsonDictionary.get("type")

            if type_key == "PatientInfo":
                with connection.cursor() as cursor:

                    id = jsonDictionary.get("id")
                    query = (
                        "SELECT global.Patient_ID,Study_date,Modality,Patient_position,Patient_sex,Object,patient_info.Number FROM "
                        f"global, patient_info WHERE global.Patient_ID=patient_info.Patient_ID AND patient_info.Patient_ID={id}"
                    )

                    cursor.execute(query)
                    rows = list(cursor.fetchall())

                    table = []
                    for item in rows:
                        for i in range(len(item)):
                            table.append(item[i])

                    td = [
                        "Patient_ID",
                        "Study_date",
                        "Modality",
                        "Patient_position",
                        "Patient_sex",
                        "Object",
                        "Number",
                    ]
                    # print(f"table = {table}")

                    cursor.close()
                    return jsonify({"table": table, "td": td})

            elif type_key == "rec_dir":
                with connection.cursor() as cursor:
                    patient_id = jsonDictionary.get("id")
                    study_date = jsonDictionary.get("date")
                    object_ = jsonDictionary.get("object")

                    query = (
                        "SELECT Full_name, Recommendation, Treatment, Direction FROM "
                        f"rec_dir WHERE Patient_ID = {patient_id} AND Study_date = '{study_date}' AND Object = '{object_}'"
                    )

                    cursor.execute(query)
                    rows = list(cursor.fetchall())

                    table = []
                    for item in rows:
                        for i in range(len(item)):
                            table.append(item[i])

                    td = [
                        "Full_name",
                        "Recommendation",
                        "Treatment",
                        "Direction",
                    ]
                    cursor.close()

                    # print(f"rows = {table}")
                return jsonify({"table": table, "td": td})

            elif type_key == "delete_global":

                with connection.cursor() as cursor:
                    patient_id = jsonDictionary.get("id")
                    query = (
                        f"DELETE FROM test.rec_dir WHERE (Patient_ID = '{patient_id}');"
                    )
                    cursor.execute(query)
                    connection.commit()

                    query = f"DELETE FROM test.patient_info WHERE (Patient_ID = '{patient_id}');"
                    cursor.execute(query)
                    connection.commit()

                    query = (
                        f"DELETE FROM test.global WHERE (Patient_ID = '{patient_id}');"
                    )
                    cursor.execute(query)
                    connection.commit()

                    query = "SELECT * FROM global"
                    cursor.execute(query)
                    rows = list(cursor.fetchall())

                    table = []
                    for item in rows:
                        for i in range(len(item)):
                            table.append(item[i])

                    td = [
                        "Number",
                        "Patient ID",
                        "Count",
                    ]

                    cursor.close()

                return jsonify({"table": table, "td": td})

            elif type_key == "delete_patient":

                with connection.cursor() as cursor:
                    patient_id = jsonDictionary.get("id")
                    study_date = jsonDictionary.get("study_date")
                    object_ = jsonDictionary.get("object")

                    query = f"SELECT Patient_ID,Count(*) FROM global Where Patient_ID={patient_id}"
                    cursor.execute(query)
                    loc_check = list(cursor.fetchone())

                    if loc_check[0] == None:
                        return

                    elif loc_check[1] != 1:
                        count = loc_check[1]
                        count -= 1
                        update_info = f"UPDATE global set Count={count} WHERE Patient_ID={patient_id}"
                        cursor.execute(update_info)
                        connection.commit()

                    query = f"DELETE FROM test.rec_dir WHERE (Patient_ID = '{patient_id}') AND (Study_date='{study_date}') AND (Object='{object_}');"
                    cursor.execute(query)
                    connection.commit()

                    query = f"DELETE FROM test.patient_info WHERE (Patient_ID = '{patient_id}') AND (Study_date='{study_date}') AND (Object='{object_}');"
                    cursor.execute(query)
                    connection.commit()

                    if loc_check[1] == 1:
                        query = f"DELETE FROM test.global WHERE (Patient_ID = '{patient_id}');"
                        cursor.execute(query)
                        connection.commit()

                    query = "SELECT * FROM patient_info WHERE (Patient_ID = '{patient_id}');"
                    cursor.execute(query)
                    rows = list(cursor.fetchall())

                    table = []
                    for item in rows:
                        for i in range(len(item)):
                            table.append(item[i])

                    td = [
                        "Patient ID",
                        "Study date",
                        "Modality",
                        "Patient sex",
                        "Object",
                        "Number",
                    ]

                    cursor.close()

                return jsonify({"table": table, "td": td})

            elif type_key == "Back":

                with connection.cursor() as cursor:

                    query = "SELECT * FROM global"

                    cursor.execute(query)
                    rows = list(cursor.fetchall())

                    table = []
                    for item in rows:
                        for i in range(len(item)):
                            table.append(item[i])

                    td = [
                        "Number",
                        "Patient_ID",
                        "Count",
                    ]
                    # print(f"table = {table}")

                    cursor.close()
                    return jsonify({"table": table, "td": td})

    with connection.cursor() as cursor:
        query = "SELECT * FROM global"
        cursor.execute(query)
        rows = list(cursor.fetchall())
        cursor.close()

    return render_template("showBD.html", tabel=rows)
