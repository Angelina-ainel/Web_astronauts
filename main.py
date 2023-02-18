from flask import Flask, render_template, redirect
from data.jobs import Jobs
from data.users import User
from login_form import LoginForm
from data import db_session
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init('db/mars_explorer.db')
    data_list = [{'surname': 'Scott', 'name': 'Ridley', 'age': 21, 'position': 'captain',
                  'speciality': 'research engineer', 'address': 'module_1', 'email': 'scott_chief@mars.org',
                  'hashed_password': 'cap'},
                 {'surname': 'Jonson', 'name': 'Angelina', 'age': 17, 'position': 'daughter',
                  'speciality': 'dancer', 'address': 'module_2', 'email': 'angel_dance@mars.org',
                  'hashed_password': 'sword'},
                 {'surname': 'Kon', 'name': 'Lisa', 'age': 27, 'position': 'master',
                  'speciality': 'beauty', 'address': 'module_3', 'email': 'lisa_con@mars.org',
                  'hashed_password': 'cap'},
                 {'surname': 'Baggins', 'name': 'Frodo', 'age': 21, 'position': 'main_hero',
                  'speciality': 'the_owner', 'address': 'module_4', 'email': 'frodo_bag@mars.org',
                  'hashed_password': 'cap'}]
    session = db_session.create_session()
    for user_data in data_list:
        user = User(**user_data)
        session.add(user)
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
