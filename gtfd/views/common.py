from flask import render_template
from gtfd import conf
from gtfd.site import app

def render(template, **kwargs):
	kwargs.update(app.config)
	return render_template(template, **kwargs)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return ref_url.netloc == test_url.netloc
