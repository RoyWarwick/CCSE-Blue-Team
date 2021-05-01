from flask import Flask, render_template
from flask_wtf import FlaskForm, validators
from wtforms import StringField, DateField
from flask_bootstrap import Bootstrap
from wtforms.validators import InputRequired
from datetime import date
import dataHandler
import sendFile


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretRandomKey'

class requestForm(FlaskForm):
    farm_id = StringField("Farm_id", validators=[InputRequired("Which farm are you referencing")])
    tunnel_id = StringField("Tunnel_id", validators=[InputRequired("Which tunnel are you referencing")])
    sdate = DateField("Start Date", format='%d/%m/%Y', validators=[InputRequired("From which date onwards do you want the data?")])
    edate = DateField("End Date", format='%d/%m/%Y', default=date.today(), validators=[InputRequired("Till which date do you want the data?")])

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
    APIRequest = []
    if form.validate_on_submit():
        string_to_arno = "{},{},{},{}".format(form.farm_id.data, form.tunnel_id.data, form.sdate.data, form.edate.data)
        send_to_arno = open("send_to_arno","w")
        send_to_arno.write(string_to_arno)
        send_to_arno.close()
        sendFile.send_file(send_to_arno)
        try:
            APIRequest = dataHandler.getAPIData()
        except TypeError:
            None
        return render_template('log.html', APIRequest = APIRequest, form=form)
    else:
        return render_template('log.html', APIRequest = APIRequest, form=form)


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
