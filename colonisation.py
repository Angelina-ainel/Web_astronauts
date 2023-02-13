from flask import Flask, url_for
import random

app = Flask(__name__)


@app.route('/')
def root():
    return "Миссия Колонизация Марса"


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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
