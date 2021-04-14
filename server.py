from flask import Flask, render_template
from flask_wtf import FlaskForm, validators
from wtforms import StringField, DateField
from flask_bootstrap import Bootstrap
from wtforms.validators import InputRequired
import dataHandler
import connectionHandler


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretRandomKey'

class requestForm(FlaskForm):
    farm_id = StringField("Farm_id", validators=[InputRequired()])
    tunnel_id = StringField("Tunnel_id", validators=[InputRequired()])
    sdate = DateField("Start Date", format='%d/%m/%Y', validators=[InputRequired()])
    edate = DateField("End Date", format='%d/%m/%Y')

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


@app.route('/log', methods=['GET', 'POST'])
def log():
    form = requestForm()

    if form.validate():

        print(form.sdate.data, form.edate.data)
        string_to_arno = "{},{},{},{}".format(form.farm_id.data, form.tunnel_id.data, form.sdate.data, form.edate.data)
        send_to_arno = open("send_to_arno","w")
        send_to_arno.write(string_to_arno)
        send_to_arno.close()
        connectionHandler.sendFile(send_to_arno)
        return render_template('log.html', form=form)
    else:
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
    app.run(debug=True)
