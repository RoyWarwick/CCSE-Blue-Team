from flask import Flask, render_template
from forms import SignUpForm
from flask_bootstrap import Bootstrap
import dataHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretRandomKey'

global json_data

@app.route('/home')
@app.route('/')  # Default directory
def index():
    return render_template('index.html')


@app.route('/sensor')  # inputs the value of the sensor number in the URL    #/sensor/<string:sensor_id>
def sensorDetails():
    sensor_info = dataHandler.getSensorInfo()
    return render_template('sensor.html', sensor_info=sensor_info)


@app.route('/tunnel')  # inputs the value of the sensor number in the URL
def farmDetails():
    Tunnel_Status = dataHandler.getTunnelData()
    return render_template('tunnel.html', Tunnel_Status=Tunnel_Status)


@app.route('/ERROR404')
def reroute():
    return render_template('404Page.html')


@app.route('/physicalAccess')
def physicalAccess():
    Physical_security_json = dataHandler.getPhysicalSecurityData()
    return render_template('physicalAccess.html', Physical_security_json = Physical_security_json)


@app.route('/log')
def log():
    form = SignUpForm()
    return render_template('log.html', form=form)


@app.route('/status')
def status():

    sorted_data = dataHandler.sortExtremeData()

    def exception_handler(value):
        try:
            return value
        except IndexError:
            return None

    app.jinja_env.filters['exception_handler'] = exception_handler
    return render_template('status.html', none=None, sorted_array=sorted_data)


if __name__ == '__main__':
    Bootstrap(app)
    app.run()
