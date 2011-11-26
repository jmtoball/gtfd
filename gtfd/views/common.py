from flask import render_template
from gtfd import conf
from gtfd.site import app

def render(template, **kwargs):
	kwargs.update(app.config)
	return render_template(template, **kwargs)
