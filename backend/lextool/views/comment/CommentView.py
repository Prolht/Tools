from flask import Blueprint, request
from flask import jsonify

from ...models.comment import Comment
from ...logger import logger
from ...cache import cache

comment = Blueprint('comment', __name__)


# ---------------------------------------------------------------------------------
# 用户反馈 相关接口
# ---------------------------------------------------------------------------------


@comment.route("", methods=['GET'])
@cache.cached(timeout=1000*60, key_prefix='all_comments')
def get_all_comments():
    data = Comment.load_show_able_comment()
    return jsonify({'data': data})


@comment.route("/new", methods=['POST'])
def add_comment():
    email = request.get_json()['mail']
    comment_type = request.get_json()['type']
    content = request.get_json()['content']
    create_at = request.get_json()['date']
    logger.info("Insert a new comment {}, {} at {}".format(email, comment_type, create_at))
    code, msg = Comment(content, comment_type, email).save()
    return jsonify({'code': code, 'msg': msg})


@comment.route("/update", methods=['POST'])
def review_comment():
    comment_id = request.get_json()['id']
    can_show = request.get_json()['can_show']
    logger.info("Review a comment id:{}".format(comment_id))
    msg, code = Comment.update(comment_id, can_show)
    return jsonify({'code': code, 'msg': msg})



