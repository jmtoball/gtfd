from flask import render_template, request, redirect, flash
from gtfd import conf
from gtfd.site import app

def render(template, **kwargs):
    kwargs.update(app.config)
    return render_template(template, **kwargs)

def safe_reload(fallback):
    for target in (request.values.get('next'), request.form.get('next'), request.referrer):
        if target and conf.SITE_URL in target:
            return redirect(target)
    return redirect(fallback)
