import datetime

from flask import Flask, redirect, request

from backend.Tools.config.default import DefaultConfig
from backend.Tools.views import register_blueprints
from backend.Tools.cache import cache
from backend.Tools.models import db


__version__ = '1.0'
__status__ = 'dev'
__description__ = 'tools'
__github__ = 'https://github.com/Prolht/Tools'
__license__ = "MIT License"


def create_app():
	app = Flask(__name__)
	# 数据库配置
	app.config['SQLALCHEMY_DATABASE_URI'] = DefaultConfig.SQLALCHEMY_DATABASE_URI
	app.config['SQLALCHEMY_BINDS'] = DefaultConfig.SQLALCHEMY_BINDS
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = DefaultConfig.SQLALCHEMY_TRACK_MODIFICATIONS
	app.config['SECRET_KEY'] = DefaultConfig.SECRET_KEY
	app.permanent_session_lifetime = datetime.timedelta(seconds=DefaultConfig.SESSION_TIME)
	register_blueprint(app)
	register_database(app)
	cache.init_app(app, config=DefaultConfig.FILESYSTEM)
	return app


def register_database(app):
	db.init_app(app)
	db.app = app


def register_blueprint(app):
	register_blueprints(app)
