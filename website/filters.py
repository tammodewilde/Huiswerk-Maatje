from flask import Markup

def nl2br(value):
    return Markup(value.replace('\n', '<br>'))