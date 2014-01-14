
ABOUT
GTFD (Getting Things Fucking Done) is a simplistic todo-list application focusing on motivating its use through ease of use and a tongue-in-cheek tone.

STATUS
Development is in an early stage although the core functionality (Task-CRUD and simple stats) is in place.
It is used in combination with velruse as authentication server, but local accounts will be added soon.

REQUIREMENTS
GTFD depends on the following Python modules:
 - Flask
 - Flask-Mail
 - Flask-Script
 - SQLAlchemy
 - parsedatetime
Database spcific packages like psycopg2 might be necessary depending on the database configuration.

DEMO
The current version is always available at http://gtd.gedankenacker.de
Authentication is currently possible against Twitter and Facebook, more providers will follow with the next velruse release. The author is actively using the demo setup, but future changes might require changes in the database layout, so if you plan on using this application let me know so I can take extra care when doing migrations.
