from flask import Flask, render_template
from forms import SignUpForm
from flask_bootstrap import Bootstrap
import dataHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretRandomKey'

global json_data


@app.route('/')  # Default directory
def index():
    sensor_info = dataHandler.getSensorInfo()
    return render_template('index.html',
                           variable='The value of this string can be accessed in the html page using {{}}',
                           json_data=sensor_info)


@app.route('/sensor')  # inputs the value of the sensor number in the URL    #/sensor/<string:sensor_id>
def sensorDetails():
    return render_template('sensor.html')


@app.route('/farm')  # inputs the value of the sensor number in the URL    #/farm/<string:farm_id>
def farmDetails():
    return render_template('farm.html')


@app.route('/index')
def reroute():
    return 'You have clicked a broken link'


@app.route('/log')
def log():
    return render_template('log.html')


@app.route('/signup')
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form)


@app.route('/status')
def status():
    extreme_humidity = dataHandler.getTooHumidSensors()
    extreme_temperature = dataHandler.getTooHotSensors()
    if len(extreme_humidity) > len(extreme_temperature):
        humid_is_larger = True
    else:
        humid_is_larger = False

    def exception_handler(value):
        try:
            return value
        except IndexError:
            return None
    app.jinja_env.filters['exception_handler'] = exception_handler
    return render_template('status.html', extreme_humidity=extreme_humidity, extreme_temperature=extreme_temperature, larger_array = humid_is_larger, none = None)


if __name__ == '__main__':
    Bootstrap(app)
    app.run()
