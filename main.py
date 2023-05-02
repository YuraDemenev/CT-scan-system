from flask import Flask, render_template, request, jsonify, json, redirect
from werkzeug.utils import secure_filename
import os
import numpy as np
import pydicom as dicom
from PIL import Image
import glob
from datetime import datetime
import pymysql

# для segmentation
import matplotlib.pyplot as plt
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from scipy import ndimage as ndi
from scipy.ndimage import binary_dilation

# Для создания форм
from forms import UploadFileForm

# Для разных страниц
import showDB

app = Flask(__name__)
app.config["SECRET_KEY"] = "123sda4gf323jsf_13gja94fs56easd"
app.config["UPLOAD_FOLDER"] = "static"


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    status = "disabled"
    arrayDcm = []
    form = UploadFileForm()
    # Находим файл
    if form.validate_on_submit():
        file = form.file.data
        # Сохраняем файл
        file.save(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                secure_filename(file.filename),
            )
        )
        return redirect("/showDicom")
        # Удаление изображение из папок
    list_files = [
        "./static/images/axial/*",
        "./static/images/sagital/*",
        "./static/images/coronal/*",
    ]
    for i in range(3):
        files = glob.glob(list_files[i])
        for f in files:
            os.remove(f)

    # Проверка на наличие dcm файла
    for file in os.listdir("./static/"):
        if file.endswith(".dcm"):
            arrayDcm.append(os.path.join("./static/", file))
    if len(arrayDcm) != 0:
        status = "Enable"

    return render_template("index.html", form=form, status=status)


app.add_url_rule("/showDB", view_func=showDB.showDB_func, methods=["POST", "GET"])
# @app.route("/showDB", methods=["POST", "GET"])
# def showDB():
#     app.logger.info("showDB")
#     return render_template("showBD.html")


# IMAGES_FOLDER_PATH = os.path.join("static", "images")
# app.config["UPLOAD_FOLDER"] = IMAGES_FOLDER_PATH


@app.route("/showDicom", methods=["POST", "GET"])
def ShowDicom():
    shape = 0
    number_axial = 256
    number_sagital = 256
    number_coronal = 256

    global count_segments
    arrayDcm = []

    global mask_labeled

    app.logger.info("start Show dicom")

    # Работа с ajax запросом
    if request.is_json:
        # if request.method == "GET":
        #     return jsonify(
        #         {"img": "static/images/axial/axial" + str(number_axial) + ".jpg"}
        #     )
        if request.method == "POST":
            jsonDictionary = request.get_json()
            type_key = jsonDictionary.get("type", 0)
            if type_key == "dicom_show":
                if "axialNumber" in jsonDictionary:
                    value_axial = jsonDictionary["axialNumber"] - 1
                    print(value_axial)
                    return jsonify(
                        {"img": "static/images/axial/axial" + str(value_axial) + ".jpg"}
                    )
                elif "sagitalNumber" in jsonDictionary:
                    value_sagital = jsonDictionary["sagitalNumber"] - 1
                    print(value_sagital)
                    return jsonify(
                        {
                            "img": "static/images/sagital/sagital"
                            + str(value_sagital)
                            + ".jpg"
                        }
                    )
                elif "coronalNumber" in jsonDictionary:
                    value_coronal = jsonDictionary["coronalNumber"] - 1
                    print(value_coronal)
                    return jsonify(
                        {
                            "img": "static/images/coronal/coronal"
                            + str(value_coronal)
                            + ".jpg"
                        }
                    )

            elif type_key == "dicom_segmentation":
                count_segments = int(jsonDictionary.get("countSegments", 0))
                app.logger.info("dicom_segmentation")
                img = np.load("static/npy/npy1.npy")

                plt.pcolormesh(img[256, :, :])

                # изначально -320 но шкала в нашем npy +1500

                mask = img < 100
                print("mask <180")

                mask = np.vectorize(clear_border, signature="(n,m)->(n,m)")(mask)
                # plt.pcolormesh(mask[256])

                # для разделения на области если в друг он принял что-то не нужное за кость
                mask_labeled = np.vectorize(label, signature="(n,m)->(n,m)")(mask)

                mask_labeled = np.vectorize(keep_top, signature="(n,m)->(n,m)")(
                    mask_labeled
                )
                labels = label(mask_labeled[256], background=0)
                print("labels")

                # plt.pcolormesh(labels)
                plt.imsave("static/images/segmentation/test.png", labels)

                return jsonify({"img": "static/images/segmentation/test.png"})

            elif type_key == "mask":
                # Удаление файлов
                list_files = [
                    "./static/images/axial/*",
                    "./static/images/sagital/*",
                    "./static/images/coronal/*",
                ]
                for i in range(3):
                    files = glob.glob(list_files[i])
                    for f in files:
                        os.remove(f)

                # MASK
                img = np.load("./static/npy/npy1.npy")
                mask = mask_labeled > 0
                # binary_fill_holes принимает 0 и 1 и заполняет дырки
                mask = np.vectorize(ndi.binary_fill_holes, signature="(n,m)->(n,m)")(
                    mask
                )

                # Увеличиваем(расширяем) изображение добавляя пикселей
                mask_new = binary_dilation(mask, iterations=5)
                img *= mask_new

                # img_shape = list(img.shape)
                # # добавляем кол-во файлов .dcm
                # volume3d = np.zeros(img_shape)

                # for i in range(512):
                #     array2d = img[i]
                #     volume3d[:, :, i] = array2d

                app.logger.info("middle")
                for i in range(0, img.shape[0]):

                    plt.imsave(
                        f"static/images/axial/axial{i}.jpg",
                        img[i, :, :],
                        cmap="gray",
                    )

                    plt.imsave(
                        f"static/images/sagital/sagital{i}.jpg",
                        img[:, :, i],
                        cmap="gray",
                    )

                    plt.imsave(
                        f"static/images/coronal/coronal{i}.jpg",
                        img[:, 511 - i, :],
                        cmap="gray",
                    )

                app.logger.info("End")

                return jsonify(
                    {
                        "axial": "static/images/axial/axial256.jpg",
                        "sagital": "static/images/sagital/sagital256.jpg",
                        "coronal": "static/images/coronal/coronal256.jpg",
                    }
                )
            elif type_key == "SQL":
                full_name = jsonDictionary.get("full_name")
                text_value = jsonDictionary.get("text_value")
                treatment = jsonDictionary.get("treatment")
                direction = jsonDictionary.get("direction")
                recomendation = jsonDictionary.get("recomendation")

                if text_value == "":
                    return jsonify(
                        {
                            "check": "false",
                            "error": "the scan object field has no record",
                        }
                    )

                if full_name == "\n                " or full_name == "":
                    return jsonify(
                        {"check": "false", "error": "the full name field has no record"}
                    )

                if recomendation == "\n                " or full_name == "":
                    return jsonify(
                        {
                            "check": "false",
                            "error": "the recomendation field has no record",
                        }
                    )

                if treatment == "\n                " or treatment == "":
                    return jsonify(
                        {"check": "false", "error": "the treatment field has no record"}
                    )

                if direction == "\n                " or direction == "":
                    return jsonify(
                        {"check": "false", "error": "the direction field has no record"}
                    )

                app.logger.info("SQL")

                for file in os.listdir("./static/"):
                    if file.endswith(".dcm"):
                        arrayDcm.append(os.path.join("./static/", file))
                dc = dicom.dcmread(arrayDcm[0])

                check, error = SQL_add(
                    dc, text_value, treatment, full_name, recomendation, direction
                )
                return jsonify({"check": check, "error": error})

    # Обработка dicom
    for file in os.listdir("./static/"):
        if file.endswith(".dcm"):
            arrayDcm.append(os.path.join("./static/", file))
    dc = dicom.dcmread(arrayDcm[0])
    arr_hu = get_pixels_hu(dc)
    np.save("./static/npy/npy1", arr_hu)

    img_shape = list(dc.pixel_array[0].shape)
    # добавляем кол-во файлов .dcm
    img_shape.append(int(512))
    # shape = img_shape[2]
    volume3d = np.zeros(img_shape)

    for i in range(512):
        array2d = dc.pixel_array[i]
        volume3d[:, :, i] = array2d

    for i in range(0, img_shape[2]):

        create_image(volume3d[:, :, i], "axial", "axial" + str(i))
        create_image(
            volume3d[:, i, :],
            "sagital",
            "sagital" + str(i),
        )
        create_image(
            volume3d[511 - i, :, :],
            "coronal",
            "coronal" + str(i),
        )

    axial_image_path = "static/images/axial/axial256.jpg"
    sagital_image_path = "static/images/sagital/sagital256.jpg"
    coronal_image_path = "static/images/coronal/coronal256.jpg"

    tabel = create_a_table_array(dc)

    return render_template(
        "dicomShow.html",
        axial=axial_image_path,
        segmentation="static/images/Optional/background.jpg",
        sagital=sagital_image_path,
        coronal=coronal_image_path,
        tabel=tabel,
    )


def create_image(image: np.ndarray, name_folder: str, name: str):
    # Convert pixel_array (img) to -> gray image (img_2d_scaled)
    # Step 1. Convert to float to avoid overflow or underflow losses.
    img_2d = image.astype(float)

    # Step 2. Rescaling grey scale between 0-255
    img_2d_scaled = (np.maximum(img_2d, 0) / img_2d.max()) * 255.0

    # Step 3. Convert to uint
    img_2d_scaled = np.uint8(img_2d_scaled)
    img_2d_scaled = Image.fromarray(img_2d_scaled)
    img_2d_scaled.save("./static/images/" + name_folder + "/" + name + ".jpg")


def keep_top(slc):
    # создаем новый срез
    new_slc = np.zeros_like(slc)

    # Получаем массив значений(площади объектов)
    rps = regionprops(slc)
    areas = [r.area for r in rps]

    # список номеров полощадей,отсортированный по велечине площадей от большего к меньшему
    idxs = np.argsort(areas)[::-1]
    for i in idxs[:count_segments]:
        new_slc[tuple(rps[i].coords.T)] = i + 1

    return new_slc


def get_pixels_hu(scans: dicom.Dataset):
    image = np.stack(scans.pixel_array)

    # Convert to int16 (from sometimes int16),
    # should be possible as values should always be low enough (<32k)
    image = image.astype(np.int16)

    # Set outside-of-scan pixels to 1
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0

    # Convert to Hounsfield units (HU)
    intercept = scans.RescaleIntercept if "RescaleIntercept" in scans else -1024
    slope = scans.RescaleSlope if "RescaleSlope" in scans else 1

    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)

    image += np.int16(intercept)

    return np.array(image, dtype=np.int16)


def create_a_table_array(dc: dicom):
    arr_string = str(np.array(dc.convert_pixel_data))
    arr_string = arr_string.split()

    # Получение даты
    index = arr_string.index("Study")
    study_data = arr_string[index + 3]
    study_data = study_data.replace("'", "")

    arr_string.pop(index)

    date = datetime(
        year=int(study_data[0:4]), month=int(study_data[4:6]), day=int(study_data[6:8])
    )

    study_data = str(date)
    # print(arr_string)

    # Получение времени
    # index = arr_string.index("Study")
    # study_time = arr_string[index + 3]
    # study_time = study_time.replace("'", "")

    # print(str(timedelta(study_time))[:-3])

    scores = (
        [1, "Study date", study_data[0:10]],
        [2, "Modality", dc.Modality],
        [3, "Patient ID", dc.PatientID],
        # ["Patient name", dc.PatientName],
        [4, "Patient position", dc.PatientPosition],
        [5, "Patient sex", dc.PatientSex],
    )
    return scores


def SQL_add(
    dc: dicom,
    text_value,
    treatment: str,
    full_name: str,
    recomendation: str,
    direction: str,
):

    arr_string = str(np.array(dc.convert_pixel_data))
    arr_string = arr_string.split()

    # Получение даты
    index = arr_string.index("Study")
    study_data = arr_string[index + 3]
    study_data = study_data.replace("'", "")

    arr_string.pop(index)

    date = datetime(
        year=int(study_data[0:4]), month=int(study_data[4:6]), day=int(study_data[6:8])
    )

    study_data = str(date)

    dic = {
        "Study_date": study_data[0:10],
        "Modality": dc.Modality,
        "Patient_ID": dc.PatientID,
        "Patient_position": dc.PatientPosition,
        "Patient_sex": dc.PatientSex,
        "Object": text_value,
    }

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
        return "false", "server connection"

    with connection.cursor() as cursor:

        query = f"SELECT Patient_ID,Count(*) FROM global Where Patient_ID={dic.get('Patient_ID')}"
        cursor.execute(query)
        loc_check = list(cursor.fetchone())

        if loc_check[0] == None:
            add_info = "INSERT INTO global (Patient_ID) VALUES (%(Patient_ID)s)"
            cursor.execute(add_info, dic)
            connection.commit()

        else:
            count = loc_check[1]
            count += 1
            # dic['Count'] = count+1
            update_info = f"UPDATE global set Count={count} WHERE Patient_ID={dic.get('Patient_ID')}"
            cursor.execute(update_info)
            connection.commit()

        try:
            # with connection.cursor() as cursor:
            add_info = (
                "INSERT INTO patient_info "
                "(Study_date,Modality,Patient_ID,Patient_position,Patient_sex,Object) "
                "VALUES (%(Study_date)s,%(Modality)s,%(Patient_ID)s,%(Patient_position)s,%(Patient_sex)s,%(Object)s)"
            )
            cursor.execute(add_info, dic)
            connection.commit()

            dic["Treatment"] = treatment
            dic["Direction"] = direction
            dic["Full_name"] = full_name
            dic["Recomendation"] = recomendation

            add_info = (
                "INSERT INTO rec_dir (Patient_ID,Treatment,Direction,Recommendation,Full_name,Study_date,Object) "
                "VALUES (%(Patient_ID)s,%(Treatment)s,%(Direction)s,%(Recomendation)s,%(Full_name)s,%(Study_date)s,%(Object)s)"
            )
            cursor.execute(add_info, dic)
            connection.commit()

            print("Success ADD")
            connection.close()

        except:
            connection.close()
            return "false", "This entry exists"

    return "true", ""


if __name__ == "__main__":
    app.run(debug=True)
