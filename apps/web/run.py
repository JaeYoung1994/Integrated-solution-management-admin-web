#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.index.controller.indexController import bp_index_index
from app.index.controller.signController import bp_index_sign
from app.index.controller.errorController import bp_index_error
from app.menu.setting.auth.controller.mainController import bp_menu_setting_auth_main
from app.menu.page.client.device.controller.mainController import bp_menu_page_client_device_main
from app.worker.command.controller.commandController import bp_client_command
from app.worker.client.controller.clientController import bp_worker_client


app = Flask(__name__)


app.register_blueprint(bp_index_index, url_prefix="/")
app.register_blueprint(bp_index_sign, url_prefix="/")
app.register_blueprint(bp_index_error, url_prefix="/")

app.register_blueprint(bp_client_command, url_prefix="/worker/command")
app.register_blueprint(bp_worker_client, url_prefix="/worker/client")

app.register_blueprint(bp_menu_page_client_device_main, url_prefix="/client/device")
app.register_blueprint(bp_menu_setting_auth_main, url_prefix="/setting")

app.config['SECRET_KEY'] = 'shiptrollCompany'
csrf = CSRFProtect()
csrf.init_app(app)

if __name__ == '__main__':
    app.run("0.0.0.0", 80, True)

