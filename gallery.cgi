from wsgiref.handlers import CGIHandler
from gallery import app

app.debug = True
CGIHandler().run(app)
