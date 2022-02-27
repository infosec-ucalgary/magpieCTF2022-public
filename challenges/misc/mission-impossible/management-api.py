from dotenv import dotenv_values
import flask
from flask import request, jsonify, render_template
import laser_control
from laser_control import init, laser_bp

ENV_VALUES = dotenv_values()

app = flask.Flask(__name__)
app.register_blueprint(laser_bp)

init()

CONFIG = {
    'API_KEY' : ENV_VALUES['API_KEY']
}

class Employees:
    def __init__(self, name, id, position):
        self.name = name
        self.id = id
        self.position = position

    def serialize(self):
        return {
            'name' : self.name,
            'id' : self.id,
            'position' : self.position
        }

    def get_id(self):
        return self.id

employees = [
    Employees('Ma', 0, 'CEO'), 
    Employees('Pa', 1, 'CEO'),
    Employees('Jim', 2, 'Marketing'),
    Employees('Diane', 3, 'Clerk')
]

@app.route('/api/docs', methods=['GET'])
def api_docs():
    return render_template('api-docs.html')

@app.route('/api/v1/employees/all', methods=['GET'])
def api_all():
    return jsonify([e.serialize() for e in employees])

@app.route('/api/v1/employees', methods=['GET'])
def api_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id parameter provided. Please specify an id.\n"

    results = []

    for person in employees:
        if person.get_id() == id:
            results.append(person.serialize())

    return jsonify(results)


# !!! EXPERIMENTAL !!!
#
# This API endpoint is functional but it has not been audited by our security team.
# While it is functional, we can not guarantee that there are no vulnerabilities.
@app.route('/api/v1/employees/format', methods=['GET'])
def format_employee():
    if 'template' in request.args:
        template = request.args['template']
        return template.format(person=employees[0])
    else:
        return "Error: No template parameter provided. Please specify an template.\n"


@app.route('/api/v1/security-controls/shutdown', methods=['POST'])
def shutdown():
    if 'X-API-Key' in request.headers and request.headers['X-API-Key'] == CONFIG['API_KEY']:

        request_data = request.get_json()

        if request_data and 'lasers' in request_data:
            lasers = request_data['lasers']
            return laser_control.shutdown_lasers(lasers, request)
        else:
            return "Invalid JSON body data!\n"
    return "You are not authorized to turn off the lasers!\n"

if __name__ == '__main__':
    app.run()
