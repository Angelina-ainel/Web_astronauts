from flask import Flask, render_template, redirect
from data.jobs import Jobs
from data.users import User
from login_form import LoginForm
from data import db_session
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init('db/mars_explorer.db')
    session = db_session.create_session()
    job = Jobs(team_leader=1, job='deployment of residential modules 1 and 2', work_size=15, collaborators='2, 3',
               is_finished=False)
    session.add(job)
    session.commit()

    # app.run()


@app.route('/')
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    astronaut = form.username_astro
    if form.validate_on_submit():
        return redirect(f'/success/{astronaut.data}')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/success/<astronaut>')
def success(astronaut):
    return render_template('success.html', title='Доступ', username=astronaut)


@app.route('/distribution')
def distribution():
    names = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни', 'Венката Капур', 'Тедди Сандерс', 'Шон Бин']
    return render_template('distribution.html', astronauts_list=names)


if __name__ == '__main__':
    # app.run(port=8080, host='127.0.0.1')
    main()
