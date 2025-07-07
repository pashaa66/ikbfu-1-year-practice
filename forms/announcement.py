from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms import SelectField, BooleanField, MultipleFileField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired


class CreateAnnouncementForm(FlaskForm):

    title = StringField("Название объекта", validators=[DataRequired()])
    description = StringField("Описание", validators=[DataRequired(),
                                                      Length(max=300)]
                              )
    city = StringField("Город", validators=[DataRequired()])
    street = StringField("Улица", validators=[DataRequired()])
    number_of_house = StringField(
        "Номер дома", validators=[DataRequired(), Length(min=1, max=999)])
    price = IntegerField("Цена",
                         validators=[DataRequired(), NumberRange(min=1)]
                         )
    announcement_type = SelectField("Тип объявления",
                                    choices=[("flat", "Квартира"),
                                             ("house", "Дом")],
                                    validators=[DataRequired()]
                                    )
    square = FloatField("Площадь", validators=[DataRequired()])
    kitchen_square = FloatField("Площадь кухни",
                                validators=[DataRequired()], default=1
                                )
    number_of_rooms = IntegerField(
        "Количество комнат", validators=[DataRequired()])
    floor = IntegerField("Этаж", validators=[DataRequired()], default=1)
    number_of_floors = IntegerField(
        "Этажи", validators=[DataRequired()], default=1
        )
    year_of_construction = IntegerField(
        "Год постройки", validators=[DataRequired()], default=2000
        )

    main_image = FileField(
        "Основное фото",
        validators=[FileRequired(), FileAllowed(["jpg", "png", "jpeg"],
                                                "Только изображения!")]
    )

    extra_images = MultipleFileField(
        "Дополнительные изображения",
        validators=[FileRequired(),
                    FileAllowed(["jpg", "jpeg", "png"], "Только изображения")]
        )

    is_sell = BooleanField("Продаётся")
    submit = SubmitField("Создать")
