from flask import Flask, render_template, redirect, current_app, abort
from flask import url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_login import current_user
from forms.login import LoginForm
from forms.register import RegisterFormUser, RegisterFormRealtor
from forms.announcement import CreateAnnouncementForm
from data.users import User
from data.announcements import Announcements
from data.announcement_images import AnnouncementImages
from data import db_session
from werkzeug.utils import secure_filename
from config import Config
from forms.custom_validators import allowed_file
import os
import uuid

# Настройка

app = Flask(__name__)
app.config.from_object(Config)
os.makedirs(app.config["REALTOR_IMAGE_PATH"], exist_ok=True)
os.makedirs(app.config["ANNOUNCEMENT_IMAGE_PATH"], exist_ok=True)
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/dom_for_you.db")
    app.run(debug=True)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Авторизация и выход


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(
            User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html",
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template("login.html", title="Авторизация", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


# Регистрация

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register_menu.html", title="Регистрация")


@app.route("/register_buyer", methods=["GET", "POST"])
def register_buyer():
    form = RegisterFormUser()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register_buyer.html",
                                   title="Регистрация покупателя",
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template("register_buyer.html",
                                   title="Регистрация покупателя",
                                   form=form,
                                   message="Такой пользователь уже есть")
        buyer = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data,
            role="buyer"
        )
        buyer.set_password(form.password.data)
        db_sess.add(buyer)
        db_sess.commit()
        return redirect("")
    return render_template("register_buyer.html",
                           title="Регистрация покупателя",
                           form=form)


@app.route("/register_realtor", methods=["GET", "POST"])
def register_realtor():
    form = RegisterFormRealtor()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register_realtor.html",
                                   title="Регистрация риэлтора",
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template("register_realtor.html",
                                   title="Регистрация риэлтора",
                                   form=form,
                                   message="Такой пользователь уже есть")
        existing_user = db_sess.query(
            User).filter(User.phone_number == form.phone_number.data).first()
        if existing_user:
            return render_template("register_buyer.html",
                                   title="Регистрация риэлтора",
                                   form=form,
                                   message="Такой пользователь уже есть")
        filename = ""
        if form.profile_picture.data:
            file = form.profile_picture.data
            if allowed_file(file.filename,
                            current_app.config["ALLOWED_EXTENSIONS"]):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(
                    current_app.config["REALTOR_IMAGE_PATH"], filename)
                os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                file.save(upload_path)
            else:
                return render_template("register_realtor.html",
                                       title="Регистрация риэлтора",
                                       form=form,
                                       message="Неверный формат изображения." +
                                       "Разрешены: jpg, jpeg, png")
        realtor = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            experience=form.experience.data,
            role="realtor",
            profile_picture=filename
        )
        realtor.set_password(form.password.data)
        db_sess.add(realtor)
        db_sess.commit()
        return redirect("/")
    return render_template("register_realtor.html",
                           title="Регистрация риэлтора",
                           form=form)


# Создание объявлений

@app.route("/creating_an_announcement", methods=["GET", "POST"])
@login_required
def creating_an_announcement():
    if current_user.role != "realtor":
        abort(403)
    form = CreateAnnouncementForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        location = (
            f"{form.city.data}, "
            f"{form.street.data}, "
            f"{form.number_of_house.data}"
        )
        announcement = Announcements(
            title=form.title.data,
            description=form.description.data,
            location=location,
            price=form.price.data,
            announcement_type=form.announcement_type.data,
            square=form.square.data,
            kitchen_square=form.kitchen_square.data,
            number_of_rooms=form.number_of_rooms.data,
            floor=form.floor.data,
            number_of_floors=form.number_of_floors.data,
            year_of_construction=form.year_of_construction.data,
            is_sell=form.is_sell.data,
            user_id=current_user.id
        )
        db_sess.add(announcement)
        db_sess.commit()

        folder = os.path.join(
            current_app.config["ANNOUNCEMENT_IMAGE_PATH"],
            f"announcement_{announcement.id}"
        )
        os.makedirs(folder, exist_ok=True)

        if form.main_image.data:
            file = form.main_image.data
            filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
            save_path = os.path.join(folder, filename)
            file.save(save_path)
            announcement.main_image = (
                f"announcement_{announcement.id}/{filename}"
                )

        if form.extra_images.data:
            for file in form.extra_images.data:
                if file and file.filename:
                    extra_filename = (
                        f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
                        )
                    extra_path = os.path.join(folder, extra_filename)
                    file.save(extra_path)
                    image = AnnouncementImages(
                        path=(
                            f"announcement_{announcement.id}/{extra_filename}"
                            ),
                        announcement_id=announcement.id
                    )
                    db_sess.add(image)

        db_sess.commit()

        return redirect("/")
    return render_template("creating_an_announcement.html",
                           title="Создание объявления", form=form)


@app.route("/announcement/<int:id>")
def announcement(id):
    if not current_user.is_authenticated:
        abort(403)
    db_sess = db_session.create_session()
    current_announcement = db_sess.query(Announcements).get(id)
    if not current_announcement:
        abort(404)
    current_announcement.visits = (current_announcement.visits or 0) + 1
    db_sess.commit()
    return render_template(
        "announcement.html",
        announcement=current_announcement,
        title=current_announcement.title
        )


@app.route("/edit_announcement/<int:id>", methods=["GET", "POST"])
@login_required
def edit_announcement(id):
    db_sess = db_session.create_session()
    announcement = db_sess.query(
        Announcements).filter(Announcements.id == id).first()
    if not announcement:
        abort(404)
    if (current_user.role != "realtor"
            or announcement.user_id != current_user.id):
        abort(403)
    form = CreateAnnouncementForm()
    if request.method == "GET":
        form.title.data = announcement.title
        form.description.data = announcement.description
        form.city.data = announcement.location.split(",")[0].strip()
        form.street.data = announcement.location.split(",")[1].strip()
        form.number_of_house.data = announcement.location.split(",")[2].strip()
        form.price.data = announcement.price
        form.announcement_type.data = announcement.announcement_type
        form.square.data = announcement.square
        form.kitchen_square.data = announcement.kitchen_square
        form.number_of_rooms.data = announcement.number_of_rooms
        form.floor.data = announcement.floor
        form.number_of_floors.data = announcement.number_of_floors
        form.year_of_construction.data = announcement.year_of_construction
        form.is_sell.data = announcement.is_sell

    if form.validate_on_submit():
        location = (
            f"{form.city.data}, "
            f"{form.street.data}, "
            f"{form.number_of_house.data}"
        )

        announcement.title = form.title.data
        announcement.description = form.description.data
        announcement.location = location
        announcement.price = form.price.data
        announcement.announcement_type = form.announcement_type.data
        announcement.square = form.square.data
        announcement.kitchen_square = form.kitchen_square.data
        announcement.number_of_rooms = form.number_of_rooms.data
        announcement.floor = form.floor.data
        announcement.number_of_floors = form.number_of_floors.data
        announcement.year_of_construction = form.year_of_construction.data
        announcement.is_sell = form.is_sell.data

        folder = os.path.join(
            current_app.config["ANNOUNCEMENT_IMAGE_PATH"],
            f"announcement_{announcement.id}"
        )
        os.makedirs(folder, exist_ok=True)

        if form.main_image.data:
            file = form.main_image.data
            filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
            save_path = os.path.join(folder, filename)
            file.save(save_path)
            announcement.main_image = (
                f"announcement_{announcement.id}/{filename}"
                )

        for img in announcement.images:
            image_path = os.path.join(
                current_app.config["ANNOUNCEMENT_IMAGE_PATH"], img.path
            )
            if os.path.exists(image_path):
                os.remove(image_path)
            db_sess.delete(img)

        if form.extra_images.data:
            for file in form.extra_images.data:
                if file and file.filename:
                    extra_filename = (
                        f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
                    )
                    extra_path = os.path.join(folder, extra_filename)
                    file.save(extra_path)
                    new_image = AnnouncementImages(
                        path=(
                            f"announcement_{announcement.id}/{extra_filename}"
                            ),
                        announcement=announcement
                    )
                    db_sess.add(new_image)

        db_sess.commit()
        return redirect(url_for("index"))

    return render_template(
        "creating_an_announcement.html",
        title="Редактирование объявления",
        form=form
        )


@app.route("/delete_announcement/<int:id>", methods=["POST"])
@login_required
def delete_announcement(id):
    db_sess = db_session.create_session()
    announcement = db_sess.query(
        Announcements).filter(Announcements.id == id).first()

    if not announcement:
        abort(404)

    if (current_user.role != "realtor" or
            announcement.user_id != current_user.id):
        abort(403)

    if announcement.main_image:
        main_path = os.path.join(
            current_app.root_path,
            current_app.config["ANNOUNCEMENT_IMAGE_PATH"],
            announcement.main_image
        )
        if os.path.exists(main_path):
            os.remove(main_path)

    for img in announcement.images:
        img_path = os.path.join(
            current_app.config["ANNOUNCEMENT_IMAGE_PATH"],
            img.path)
        if os.path.exists(img_path):
            os.remove(img_path)
        db_sess.delete(img)

    db_sess.delete(announcement)
    db_sess.commit()
    return redirect(url_for("profile", id=current_user.id))


@app.route("/profile/<int:id>")
@login_required
def profile(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    if not user or user.role != "realtor":
        abort(404)

    announcements = db_sess.query(
        Announcements).filter(Announcements.user_id == user.id).all()

    return render_template(
        "profile.html",
        user=user,
        announcements=announcements,
        title="Профиль")


@app.route("/")
def index():
    db_sess = db_session.create_session()
    announcement_list = db_sess.query(Announcements).all()
    return render_template(
        "index.html",
        title="Объявления",
        announcements=announcement_list
        )


if __name__ == "__main__":
    main()
