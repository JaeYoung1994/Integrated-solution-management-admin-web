from flask import Flask
from flask_restx import Api
from app.auth.user import auth_user
from app.data.user import data_user
from app.sys.main.menu import sys_main_menu

from app.worker.command.commandController import ra_worker_command
from app.worker.client.clientController import ra_worker_client

from common.security.encryption import Encryption

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shiptrollCompany'
app.config['BCRYPT_LEVEL'] = 10
Encryption().setBcrypt(app)
api = Api(
    app,
    version='dev_0.1',
    title='Integrated API Server',
    description='RestAPI for server management',
    terms_url="/",
    contact="shiptroll@gmail.com",
    license="MIT",
    url_scheme='http'
)

api.add_namespace(auth_user, '/auth/user')
api.add_namespace(data_user, '/user')
api.add_namespace(sys_main_menu, '/sys/main')

api.add_namespace(ra_worker_client, '/worker/client')
api.add_namespace(ra_worker_command, '/worker/command')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)