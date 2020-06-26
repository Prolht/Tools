from . import db
from ..config.default import DefaultConfig


class PoetIntroduction(db.Model):
    __bind_key__ = 'poem'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'poet_introduction'  # 诗人简介

    id = db.Column(db.Integer, primary_key=True)
    descb = db.Column(db.Text(16777216))
    poet = db.Column(db.String(100), index=True)
    dynasty = db.Column(db.String(8))

    @classmethod
    def search_poet(cls, keyword, page):
        items = cls.query.filter(
                cls.poet.like("%%{}%%".format(keyword)) if keyword is not None else "")\
            .paginate(page=page, per_page=DefaultConfig.PER_PAGE, error_out=False).items
        return [item.poet for item in items]

    @classmethod
    def search_keyword_total(cls, keyword):
        total = len(cls.query.filter(
            cls.poet.like("%%{}%%".format(keyword)) if keyword is not None else "").all())
        return total


class PoemTangSong(db.Model):
    __bind_key__ = 'poem'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'tang_song_poem'

    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    paragraphs = db.Column(db.Text)
    poem = db.Column(db.Text)
    poet = db.Column(db.String(100))
    dynasty = db.Column(db.String(8))


class PoemLunyu(db.Model):
    __bind_key__ = 'poem'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'lun_yu'

    id = db.Column(db.Integer, primary_key=True)
    paragraphs = db.Column(db.Text)
    chapter = db.Column(db.String(50))


class PoemSongci(db.Model):
    __bind_key__ = 'poem'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'song_ci'

    id = db.Column(db.Integer, primary_key=True)
    paragraphs = db.Column(db.Text)
    rhythmic = db.Column(db.String(40))
    poet = db.Column(db.String(100))


class CiAuthor(db.Model):
    __bind_key__ = 'poem'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'ci_poet'

    id = db.Column(db.Integer, primary_key=True)
    long_desc = db.Column(db.Text)
    short_desc = db.Column(db.Text)
    poet = db.Column(db.String(100))


class ShiJing(db.Model):
    __bind_key__ = 'poem'  # 已设置__bind_key__,则采用设置的数据库引擎
    __tablename__ = 'shi_jing'

    id = db.Column(db.Integer, primary_key=True)
    poem = db.Column(db.TEXT)
    chapter = db.Column(db.String(30))
    section = db.Column(db.String(30))
    content = db.Column(db.Text)
