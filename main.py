from flask import Flask, render_template, redirect, request, make_response, session
from data.jobs import Jobs
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users import User
from login_form import LoginForm
from data import db_session
from forms.users import LoginForm
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
    # user = User(name='test_user', email='testing3@gmail.com')
    # user.set_password('ueo58nkk3')
    # session.add(user)
    # session.commit()
    app.run()


@app.route('/')
@app.route('/job_journal')
def job_journal():
    db_session.global_init('db/mars_explorer.db')
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template('journal.html', jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    db_session.global_init('db/mars_explorer.db')
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
        return redirect('/')
    return render_template('job_adding.html', title='Добавление работы',
                           form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    session.permanent = True
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


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

