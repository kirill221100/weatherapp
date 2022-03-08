import requests, datetime, random
from flask import flash, session, redirect, request, url_for, render_template
from app import app, scheduler
from app.config import Config as cfg
from app.forms import OptionsForm



def get_weather_data(city, som):
    if som == standart:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=standart&lang=ru&appid={ cfg.API }'
    elif som == imperial:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&lang=ru&appid={cfg.API}'
    else:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={cfg.API}'
    r = requests.get(url).json()
    return r

standart = {'temp': 'K', 'speed': 'метр/сек.'}
imperial = {'temp': 'F', 'speed': 'миль/час'}
metric = {'temp': 'C', 'speed': 'метр/сек.'}

usd, eur, news = None, None, None


@app.before_first_request
def bfr():
    global usd, eur, news
    news = requests.get(f'https://newsapi.org/v2/top-headlines?country=ru&apiKey={cfg.NEWS_API}').json()['articles']
    usd = round(requests.get(f'https://freecurrencyapi.net/api/v2/latest?apikey={cfg.CURRENCY_API}&base_currency=USD').json()['data']['RUB'], 2)
    eur = round(requests.get(f'https://freecurrencyapi.net/api/v2/latest?apikey={cfg.CURRENCY_API}&base_currency=EUR').json()['data']['RUB'], 2)

@scheduler.task('interval', id='do_job_1', seconds=600)
def job1():
    global usd, eur
    usd = round(requests.get(f'https://freecurrencyapi.net/api/v2/latest?apikey={cfg.CURRENCY_API}&base_currency=USD').json()['data']['RUB'], 2)
    eur = round(requests.get(f'https://freecurrencyapi.net/api/v2/latest?apikey={cfg.CURRENCY_API}&base_currency=EUR').json()['data']['RUB'], 2)

@scheduler.task('interval', id='do_job_2', seconds=3600)
def job2():
    global news
    news = requests.get(f'https://newsapi.org/v2/top-headlines?country=ru&apiKey={cfg.NEWS_API}').json()['articles']

scheduler.start()


@app.route('/', methods=["GET", "POST"])
def index():
    if session.get('som') == None:
        session['som'] = metric
    if request.method == 'POST':
        data = get_weather_data(request.form['city'], som=session.get('som'))#print(data)
        if data['cod'] == '404':
            flash('Город не найден :(')
            return redirect(url_for('index'))
        session['city'] = data['name']
        return redirect(url_for('index'))
    data = get_weather_data(session.get('city'), som=session.get('som'))
    time = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=data['timezone']))).strftime("%H:%M")
    return render_template('weather.html', data=data, time=time, som=session.get('som'), usd=usd, eur=eur, news=random.sample(news, 3))

@app.route('/options', methods=["GET", "POST"])
def options():
    form = OptionsForm()
    if request.method == 'POST':
        som = form.option.data
        if som == 'standart':
            som = standart
        elif som == 'imperial':
            som = imperial
        else:
            som = metric
        session['som'] = som
        return redirect(url_for('index'))
    return render_template('options.html', form=form)

