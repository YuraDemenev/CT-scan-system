from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, IntegerField
from wtforms.validators import InputRequired


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


class TestNumber(FlaskForm):
    number_of_axial = IntegerField("Number of axial ", validators=[InputRequired()])
    submit_axial = SubmitField("Show Axilal")

    number_of_sagital = IntegerField("Number of sagital", validators=[InputRequired()])
    submit_sagital = SubmitField("Show Sagital")

    number_of_coronal = IntegerField("Number of coronal", validators=[InputRequired()])
    submit_coronal = SubmitField("Show Coronal")


# def input_image_number(shape: int, volume3d: np.ndarray):
#     # Ввод номера картинки
#     number_axial = int(256)
#     number_sagital = int(256)
#     number_coronal = int(256)

#     form = TestNumber()

#     if form.submit_axial.data and form.validate_on_submit():
#         if number_axial > shape:
#             number_axial = shape
#         elif number_axial < 0:
#             number_axial = 0
#         else:
#             number_axial = form.number_of_axial.data

#     create_image(volume3d[:, :, number_axial], "axial", "axial" + str(number_axial))

#     axial_image_path = "static/images/axial/axial" + str(number_axial) + ".jpg"
#     app.logger.info("axial = " + str(number_axial))

#     if form.submit_sagital.data and form.validate_on_submit():
#         if number_sagital > shape:
#             number_sagital = shape
#         elif number_sagital < 0:
#             number_sagital = 0
#         else:
#             number_sagital = form.number_of_sagital.data

#     create_image(
#         volume3d[:, number_sagital, :], "sagital", "sagital" + str(number_sagital)
#     )

#     sagital_image_path = "static/images/sagital/sagital" + str(number_sagital) + ".jpg"
#     app.logger.info("sagital = " + str(number_sagital))

#     if form.submit_coronal.data and form.validate_on_submit():
#         if number_coronal > shape:
#             number_coronal = shape
#         elif number_coronal < 0:
#             number_coronal = 0
#         else:
#             number_coronal = form.number_of_coronal.data

#     create_image(
#         volume3d[511 - number_coronal, :, :], "coronal", "coronal" + str(number_coronal)
#     )

#     coronal_image_path = "static/images/coronal/coronal" + str(number_coronal) + ".jpg"
#     app.logger.info("coronal = " + str(number_coronal))

#     return axial_image_path, sagital_image_path, coronal_image_path, form
