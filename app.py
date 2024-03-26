import codecs
import json
import sys
from flask import Flask, render_template
from flask_cors import CORS
from flask_mail import Mail

from Routes.AccountRoute import accountRoute
from Routes.ClassRoute import classRoute
from Routes.PostRoute import postRoute
from Routes.CommentRoute import commentRoute
from Routes.ClassMemberRoute import classMemberRoute
from Routes.QuizzRoute import quizzRoute
from Routes.ResultsRoute import resultsRoute
from Routes.RouteTemplate.AccountRouteTemp import accountTemp_route
from Routes.RouteTemplate.HomeRouterTemp import homeRouteTemp
from Utilities.Config import login_manager, ConfigDatabase, ma, db

app = Flask(__name__)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
# Config login
login_manager.init_app(app)
login_manager.login_view = 'accountRouter.login_account'

# config cros
CORS(app)

# config sesion
app.config['SECRET_KEY'] = "nen_tao_ra_mot_chuoi_string_that_dai"

# config email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'hydrasneaker@gmail.com'
app.config['MAIL_PASSWORD'] = 'omlfwtrdxpwkbbfv'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# register router
app.register_blueprint(accountRoute)
app.register_blueprint(classRoute)
app.register_blueprint(postRoute)
app.register_blueprint(commentRoute)
app.register_blueprint(classMemberRoute)
app.register_blueprint(quizzRoute)
app.register_blueprint(resultsRoute)
# register router temp
app.register_blueprint(accountTemp_route)
app.register_blueprint(homeRouteTemp)

# config database
app.config.from_object(ConfigDatabase)
db.init_app(app)
ma.init_app(app)
if __name__ == '__main__':
    app.run()
