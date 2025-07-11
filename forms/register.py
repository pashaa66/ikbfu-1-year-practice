from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, StringField
from wtforms import IntegerField, TelField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, NumberRange
from forms.custom_validators import check_phone


class RegisterFormUser(FlaskForm):
    name = StringField("Имя пользователя", validators=[DataRequired()])
    surname = StringField("Фамилия пользователя", validators=[DataRequired()])
    age = IntegerField(
        "Возраст пользователя",
        validators=[DataRequired(),
                    NumberRange(min=18,
                                message="Возраст должен быть не меньше 18 лет")
                    ])
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль",
                             validators=[DataRequired(), Length(min=8)])
    password_again = PasswordField("Повторите пароль",
                                   validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Зарегистрироваться")


class RegisterFormRealtor(FlaskForm):
    name = StringField("Имя риэлтора", validators=[DataRequired()])
    surname = StringField("Фамилия риэлтора", validators=[DataRequired()])
    age = IntegerField(
        "Возраст риэлтора",
        validators=[DataRequired(),
                    NumberRange(min=20,
                                message="Возраст должен быть не меньше 20 лет")
                    ])
    email = EmailField("Почта", validators=[DataRequired()])
    phone_number = TelField("Номер телефона", validators=[DataRequired(),
                                                          check_phone])
    experience = IntegerField("Стаж работы", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired(),
                                                   Length(min=8)])
    password_again = PasswordField("Повторите пароль",
                                   validators=[DataRequired(), Length(min=8)])
    profile_picture = FileField("Фотография профиля", validators=[
        FileAllowed(["jpg", "png", "jpeg"], "Только изображения!")
    ])
    submit = SubmitField("Зарегистрироваться")
