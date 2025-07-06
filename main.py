from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required
from forms.login import LoginForm
from forms.register import RegisterFormUser, RegisterFormRealtor
from data.users import User
from data import db_session
import os

# Настройка
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(os.basedir,
                                           "static", "img", "uploads")
app.config["SECRET_KEY"] = "ikbfu_secret_key"
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(
            User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message='Неправильный логин или пароль',
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# Регистрация
@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register_menu.html", title="Регистрация")


@app.route('/register_buyer', methods=['GET', 'POST'])
def register_buyer():
    form = RegisterFormUser()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register_buyer.html',
                                   title='Регистрация покупателя',
                                   form=form,
                                   message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register_buyer.html',
                                   title='Регистрация покупателя',
                                   form=form,
                                   message='Такой пользователь уже есть')
        buyer = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data,
            role='buyer'
        )
        buyer.set_password(form.password.data)
        db_sess.add(buyer)
        db_sess.commit()
        return redirect('/login')
    return render_template('register_buyer.html',
                           title='Регистрация покупателя',
                           form=form)


@app.route('/register_realtor', methods=['GET', 'POST'])
def register_realtor():
    form = RegisterFormRealtor()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register_realtor.html',
                                   title='Регистрация риэлтора',
                                   form=form,
                                   message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register_realtor.html',
                                   title='Регистрация риэлтора',
                                   form=form,
                                   message='Такой пользователь уже есть')
        existing_user = db_sess.query(
            User).filter(User.email == form.email.data).first()
        if existing_user:
            return render_template('register_buyer.html',
                                   title='Регистрация риэлтора',
                                   form=form,
                                   message='Такой пользователь уже есть')
        realtor = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            experience=form.experience.data,
            role='realtor'
        )
        realtor.set_password(form.password.data)
        db_sess.add(realtor)
        db_sess.commit()
        return redirect('/login')
    return render_template('register_realtor.html',
                           title='Регистрация риэлтора',
                           form=form)


@app.route("/")
def index():
    # db_sess = db_session.create_session()
    # announcement_list = db_sess.query(Announcements).all()
    return render_template('index.html', title='Объявления')


if __name__ == "__main__":
    main()
