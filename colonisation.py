from flask import Flask, url_for, request, render_template
import random

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    user = "Ученик Яндекс.Лицея"
    return render_template('index.html', title='Домашняя страница',
                           username=user)

@app.route('/promotion')
def promotion():
    return '</br>'.join(['Человечество вырастает из детства.',

                         'Человечеству мала одна планета.',

                         'Мы сделаем обитаемыми безжизненные пока планеты.',

                         'И начнем с Марса!',

                         'Присоединяйся!'])


@app.route('/image_mars')
def image_mars():
    return f"""<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <title>Привет, Марс!</title>
                  </head>
                  <body>
                    <h1>Жди нас, Марс!</h1>
                    <img src="{url_for('static', filename='img/mars.jpg')}"
                    alt="здесь должна была быть картинка, но не нашлась">'''
                    </br><p>Вот она какая, красная планета.</p>
                  </body>
                </html>"""


@app.route('/promotion_image')
def promotion_image():
    promo = ['Человечество вырастает из детства.',

             'Человечеству мала одна планета.',

             'Мы сделаем обитаемыми безжизненные пока планеты.',

             'И начнем с Марса!',

             'Присоединяйся!']
    alerts = ['alert-primary', 'alert-secondary', 'alert-success', 'alert-warning', 'alert-danger']
    template = '<div class="alert {}" role="alert">{}</div>'
    divs = ''.join(template.format(random.choice(alerts), phrase) for phrase in promo)
    print(divs)

    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <title>Колонизация</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.2.1/dist/css/bootstrap.min.css" 
                    integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                  </head>
                  <body>
                    <h1>Жди нас, Марс!</h1>
                    <img src="{url_for('static', filename='img/mars.jpg')}">
                    {divs}
                  </body>
                </html>'''


@app.route('/astronaut_selection', methods=['POST', 'GET'])
def astronaut_selection():
    if request.method == 'GET':
        template = '''<div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
                        <label class="form-check-label" for="flexCheckDefault">{}</label>
                    </div>'''
        profs = ''.join(template.format(value) for value in
                        ('инженер-исследователь', 'пилот', 'строитель', 'экзобиолог',
                         'врач', 'инженер по терраформированию', 'климатолог',
                         'специалист по радиационной защите', 'астрогеолог', 'гляциолог',
                         'инженер жизнеобеспечения', 'метеоролог', 'оператор марсохода',
                         'киберинженер', 'штурман', 'пилот дронов'))
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Пример формы</title>
                          </head>
                          <body>                            
                            <div >                                
                                <form class="login_form" method="post" enctype="multipart/form-data">
                                    <h1>Анкета претендента</h1>
                                    <h3>на участие в миссии</h3>
                                    <input type="text" class="form-control" id="lastname" aria-describedby="lastnameHelp" placeholder="Введите фамилию" name="lastname">
                                    <input type="text" class="form-control" id="firstname" aria-describedby="firstnameHelp" placeholder="Введите имя" name="firstname">
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <label for="eduSelect" class="form-label">Какое у Вас образование</label>
                                    <select id="eduSelect" class="form-select" aria-label="Пример выбора по умолчанию">
                                      <option selected>Откройте это меню выбора</option>
                                      <option value="1">Начальное</option>
                                      <option value="2">Среднее</option>
                                      <option value="3">Высшее</option>
                                    </select>
                                    <label for="profSelect">Какие у Вас есть профессии?</label>
                                    <div id="profSelect" class="form-group">
                                        {profs}
                                     </div>
                                    <div class="form-group">
                                        <label for="photo">Приложите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div>
                                    </div>
                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                        <label class="form-check-label" for="acceptRules">Готов быть добровольцем</label>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Записаться</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        print(request.form)
        return "Форма отправлена"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
