from flask import Flask, render_template, redirect, request, make_response, session
from data.jobs import Jobs
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users import User
# from login_form import LoginForm
from data import db_session
from forms.users import LoginForm, RegisterForm
from forms.jobs import JobForm
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YANDEX_LYCEUM_KEY'
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init('db/mars_explorer.db')
    # session = db_session.create_session()
    # user = User(name='Angelina', email='testAinel@gmail.com')
    # user.set_password('Undomiel3241')
    # session.add(user)
    # session.commit()
    app.run(port=8080, host='127.0.0.1')


@app.route('/')
@app.route('/base_page')
def base_page():
    return render_template('base.html', title='главная страница')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.email = form.email.data
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/job_journal')
def job_journal():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template('journal.html', jobs=jobs, title='works log')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job', methods=["GET", "POST"])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        # jobs.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.is_finished = form.is_finished.data
        current_user.jobs.append(job)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/job_journal')
    return render_template('job_adding.html', title='Добавление работы',
                           form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/index')
def index():
    return render_template('index.html', title='Заготовка')


@app.route('/training/<prof>')
def training(prof):
    return render_template('training.html', prof=prof)


@app.route('/list_prof/<list>')
def list_prof(list):
    prof = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог',
                         'врач', 'инженер по терраформированию', 'климатолог',
                         'специалист по радиационной защите', 'астрогеолог', 'гляциолог',
                         'инженер жизнеобеспечения', 'метеоролог', 'оператор марсохода',
                         'киберинженер', 'штурман', 'пилот дронов']
    return render_template('profs.html', list=list, prof=prof)


@app.route('/answer')
@app.route('/auto_answer')
def auto_answer():
    params = {'title': 'Анкета',
              'surname': 'Могилко',
              'name': 'Марина',
              'education': 'Университет',
              'profession': 'Инфлюэнсер',
              'sex': 'Женский',
              'motivation': 'Реклама',
              'ready': 'конечно',

    }
    return render_template('auto_answer.html', **params)


@app.route('/distribution')
def distribution():
    names = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни', 'Венката Капур', 'Тедди Сандерс', 'Шон Бин']
    return render_template('distribution.html', astronauts_list=names)


if __name__ == '__main__':
    main()

