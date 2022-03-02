import requests, datetime
from forex_python.converter import CurrencyRates
from flask import flash, session, redirect, request, url_for, render_template
from app import app
from app.config import Config as cfg
from app.forms import OptionsForm

c = CurrencyRates()



def get_weather_data(city, som):
    if som == standart:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={ city }&units=standart&lang=ru&appid={ cfg.API }'
    elif som == imperial:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&lang=ru&appid={cfg.API}'
    else:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={cfg.API}'
    r = requests.get(url).json()
    #print(r)
    return r

standart = {'temp': 'K', 'speed': 'метр/сек.'}
imperial = {'temp': 'F', 'speed': 'миль/час'}
metric = {'temp': 'C', 'speed': 'метр/сек.'}

@app.route('/', methods=["GET", "POST"])
def index():
    usd = round(c.get_rate('USD', 'RUB'), 2)
    eur = round(c.get_rate('EUR', 'RUB'), 2)
    if session.get('som') == None:
        session['som'] = metric
    if request.method == 'POST':
        data = get_weather_data(request.form['city'], som=session.get('som'))
        #print(data)
        if data['cod'] == '404':
            flash('Город не найден :(')
            return redirect(url_for('index'))
        time = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=data['timezone']))).strftime("%H:%M")
        session['city'] = data['name']
        return render_template('weather.html', data=data, time=time, som=session.get('som'), usd=usd, eur=eur)
    data = get_weather_data(session.get('city'), som=session.get('som'))
    time = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(seconds=data['timezone']))).strftime("%H:%M")
    return render_template('weather.html', data=data, time=time, som=session.get('som'), usd=usd, eur=eur)

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
