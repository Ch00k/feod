from feod import app
from feod.model import db
from feod.controllers import admin_controller

app.debug = True
db.create_all()
app.run()