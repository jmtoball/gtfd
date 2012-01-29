from flask import render_template, request
from gtfd import conf
from gtfd.site import app

def render(template, **kwargs):
	kwargs.update(app.config)
	return render_template(template, **kwargs)

def safe_reload(fallback):
    if conf.SITE_URL in request.referrer:
        return redirect(request.referrer)
    return redirect(fallback)
