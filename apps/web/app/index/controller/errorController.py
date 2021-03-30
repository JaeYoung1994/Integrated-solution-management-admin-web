# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from common.init import Init

template_path = Init.tempPath()
bp_index_error = Blueprint("index_error", __name__, template_folder="/templates")

@bp_index_error.route("/404")
def Error404_view():
    return render_template(template_path + '/error/404.html')