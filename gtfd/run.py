from gtfd.site import app, init_db

app.run(host='0.0.0.0', port=8000, debug=True)
init_db()
