import json
import re

from flask import (Blueprint, request, jsonify)
from oocfg import cfg

from backend.lextool.models.poem import *
from backend.lextool.common.cache import cache
from backend.lextool.common.logger import LOG
from backend.lextool.common.response import not_found_resp, success_resp
from backend.lextool.utils.simp2tra import simp2tra
from backend.lextool.common.exceptions import FiltersTypeError


poem = Blueprint('poem', __name__)


def _make_cache_key(request, req_info: dict):
    """
    make cache key
    :param request: current wsgi request
    :param req_info: the info to make cache. depends on each models
    :return: json.dumps()
    """
    cache_key = {'url': request.path}
    cache_key.update(req_info)
    return json.dumps(cache_key)


def _make_poets_dict(request):
    param = request.args
    return {
        'dynasty': param.get('dynasty', '唐'),
        'page': param.get('page', 1, type=int),
        'per_page': param.get('per_page', cfg.CONF.TOOLS.pagination, type=int)
    }

@poem.route('/poets', methods=['GET'])
def get_poets():
    """
    获取指定朝代的所有作者，若不指定朝代，则默认返回“唐”朝的作者信息
    """
    req_info = _make_poets_dict(request)
    LOG.info("Get Poets of {dynasty} in page {page}, as per page {per_page}".format(**req_info))
    
    cache_key = _make_cache_key(request, req_info)
    cache_data = cache.get(cache_key)
    
    if cache_data and not cfg.CONF.TOOLS.debug:
        data = cache_data
        LOG.info("Get Poets of {} in page {} by cache".format(req_info['dynasty'], req_info['page']))
        return success_resp(data)
    else:
        try:
            paginate_obj = Poet.query.filter(Poet.dynasty == req_info['dynasty']).paginate(
                page=req_info['page'],
                per_page=req_info['per_page'],
                error_out=True
            )
            if not paginate_obj.items:
                return not_found_resp(req_info)
            
            data = {
                'total': paginate_obj.total,
                'poets': [item.poet for item in paginate_obj.items],
                'per_page': req_info['per_page'],
                'has_next': paginate_obj.has_next,
                'has_prev': paginate_obj.has_prev,
            }
            
            cache.set(cache_key, data)
            return success_resp(req_info, data)
        except Exception as e:
            LOG.error(e)
            resp_data = {'msg': 'error'}
            return not_found_resp(resp_data)


@poem.route('/poems', methods=['GET'])
def get_poems():
    """
    获取诗人的诗作， 若不指定诗人，则默认返回唐-李白的诗作
    """
    param = request.args
    poet = simp2tra(param.get('poet', '李白'))
    dynasty = param.get('dynasty', '唐')
    req_info = {'poet': poet, 'dynasty': dynasty}
    
    LOG.info("Get {} {}'s Poems".format(dynasty, poet))
    cache_key = _make_cache_key(request, req_info)
    cache_data = cache.get(cache_key)
    
    if cache_data and not cfg.CONF.TOOLS.debug:
        LOG.info("Get {} {}'s Poems by cache".format(dynasty, poet))
        poems = cache_data
        return success_resp(req_info, {'poems': poems})
    else:
        try:
            poet_obj = Poet.query.filter_by(poet=poet, dynasty=dynasty).first()
            poems = [item.poem for item in poet_obj.poems]
            req_info.update({'poems': poems})
            cache.set(cache_key, poems)
        except Exception as e:
            LOG.error("Error : {}".format(e))
            return not_found_resp(req_info)
        return success_resp(req_info, {'poems': poems})


@poem.route('/search', methods=['GET'])
def search_poets():
    """
    获取诗人的诗作
    TODO(lex):优化代码逻辑
    """
    param = request.args
    keyword = simp2tra(param.get('keyword'))
    page = param.get('page', 1, type=int)
    LOG.info("Search Poets has {}".format(keyword))

    req_info = {'keyword': keyword, 'page': page}
    cache_key = _make_cache_key(request, req_info)
    cache_data = cache.get(cache_key)
    if not keyword or not isinstance(keyword, str):
        return jsonify({'code': 200, 'poets': []})
    if cache_data:
        data = json.loads(cache_data)
        poets = data['poets']
        total = data['total']
    else:
        try:
            poets = Poet.search_poet(keyword, page)
            total = Poet.search_keyword_total(keyword)
            cache.set('/poet/search' + keyword + str(page), poets)
            cache.set('/poet/search' + keyword + 'total', total)
        except Exception as e:
            poets = []
            total = 0
            LOG.error("Error : {}".format(e))
    return jsonify({
        'code': 200,
        'poets': poets,
        'total': total
    })


def _make_content_dict(request) -> dict:
    """
    tranfer request to dict which needed in get_content()
    """
    param = request.args
    return {
        'poet': param.get('poet'),
        'dynasty': param.get('dynasty'),
        'poem': param.get('poem')
    }


@poem.route('/content', methods=['GET'])
def get_content():
    """
    获取诗歌内容
    """    
    req_info = _make_content_dict(request)
    cache_key = _make_cache_key(request, req_info)
    LOG.info("Get {dynasty} {poet}'s {poem}'s content".format(**req_info))
    
    if cache.get(cache_key) and not cfg.CONF.TOOLS.debug:
        resp_data = cache.get(cache_key)
        return success_resp(req_info, resp_data)
    else:
        try:
            poet_obj = Poet.query.filter(
                Poet.dynasty == req_info['dynasty'],
                Poet.poet == req_info['poet']
            ).first()
            content = poet_obj.poems.filter(Poem.poem == req_info['poem']).\
                first().paragraphs
            
            content['paragraphs'] = content['paragraphs'].split('。')
            
            resp_data = {'content': content}
            cache.set(cache_key, resp_data)
            
            return success_resp(req_info, resp_data)
        except Exception as e:
            LOG.error("Error is: {}".format(e))
            return not_found_resp(req_info)
        


def get_lunyu_chapters():
    """
    获取论语所有的章名
    """
    try:
        items = Lunyu.query.all()
        chapters = [item.chapter for item in items]
    except Exception as e:
        chapters = []
        LOG.error(e)
    return chapters


def get_lunyu_paragraphs(chapter):
    try:
        paragraphs_data = Lunyu.query.filter(Lunyu.chapter == chapter).first().to_dict()

        paragraphs_data['paragraphs'] = paragraphs_data['paragraphs'].split('|')
        return paragraphs_data
    except Exception as e:
        paragraphs = ''
        LOG.error(e)
        raise Exception("Error")
    

def _make_lunyu_dict(request):
    param = request.args
    return {
        'chapter': param.get('chapter', None),
    }


@poem.route('/lunyu', methods=['GET'])
def get_lunyu():
    """
    获取论语的内容
    chapter: 章
    """
    req_info = _make_lunyu_dict(request)
    cache_key = _make_cache_key(request, req_info)
    if req_info['chapter'] is None:
        # 若不指定chapter，则处理逻辑为, 获取论语的所有章，简化接口
        if cache.get(cache_key) and not cfg.CONF.TOOLS.debug:
            resp_data = cache.get(cache_key)
            return success_resp(req_info, resp_data)
        else:
            chapters = get_lunyu_chapters()
            resp_data = {'chapters': chapters}
            cache.set(cache_key, resp_data)
            req_info.pop('chapter')  # in this case, `chapter` is None, so we pop it
            return success_resp(req_info, resp_data)
    else:
        LOG.info('chapter: ' + req_info['chapter'])
        if cache.get(cache_key) and not cfg.CONF.TOOLS.debug:
            resp_data = cache.get(cache_key)
            return success_resp(req_info, resp_data)
        else:
            paragraphs = get_lunyu_paragraphs(req_info['chapter'])
            resp_data = {'paragraphs': paragraphs}
            cache.set(cache_key, resp_data)
        return success_resp(req_info, resp_data)


def _make_songci_req_info(request, filters=None) -> dict:
    """
    make songci request info dict
    :param request: wsgi request
    :param filters: list, for what you need when use this func
    :return: 
    """
    param = request.args
    if filters is None:
        return {
            'poet': param.get('poet'),
            'rhythmic': param.get('rhythmic'),
            'page': param.get('page', 1, type=int),
            'limits': param.get('limits', 0, type=int)
            }
    else:
        if not isinstance(filters, list):
            raise FiltersTypeError()
        return {key: param.get(key) for key in filters}


@poem.route('/songci/content', methods=['GET'])
def get_songci_content():
    """
    获取宋词的内容
    param
    poet: must
    rhythmic: must   
    """
    req_info = _make_songci_req_info(request, filters=['poet', 'rhythmic'])
    cache_key = _make_cache_key(request, req_info)
    cache_data = cache.get(cache_key)
    if cache_data and not cfg.CONF.TOOLS.debug:
        LOG.info("GET SongCi Content By Cache")
        resp_data = cache_data
        return success_resp(req_info, resp_data)
    else:
        try:
            poet_obj = CiPoet.query.filter(CiPoet.poet == req_info['poet']).first()
            poem_dict = poet_obj.ci.filter(Songci.rhythmic == req_info['rhythmic']).first().to_dict()

            poem_dict['paragraphs'] = re.split('。|？', poem_dict['paragraphs'])

            resp_data = poem_dict
            cache.set(cache_key, resp_data)
            return success_resp(req_info, resp_data)
        except Exception as e:
            paragraphs = ''
            LOG.error(e)
            return not_found_resp(req_info)


@poem.route('/songci/poet/poems', methods=['GET'])
def get_songci_poem():
    """
    获取作者名下的所有词
    param:
    poet: must
    """
    req_info = _make_songci_req_info(request, filters=['poet'])
    cache_key = _make_cache_key(request, req_info)
    cache_data = cache.get(cache_key)
    if cache_data and not cfg.CONF.TOOLS.debug:
        LOG.info("GET By Cache Req {}".format(cache_key))
        return success_resp(req_info, cache_data)
    else:
        try:
            ci_poet_obj = CiPoet.query.filter(CiPoet.poet == req_info['poet']).first()

            rhythmics = list(set(ci.rhythmic for ci in ci_poet_obj.ci))

            resp_data = {'rhythmics': rhythmics}

            cache.set(cache_key, resp_data)
        except Exception as e:
            LOG.error(e)
            return not_found_resp(req_info)
        return success_resp(req_info, resp_data)


@poem.route('/songci/poets', methods=['GET'])
def get_songci_poets():
    """
    获取宋词的所有作者
    """
    req_info = _make_songci_req_info(request, filters=['limits', 'page'])
    cache_key = _make_cache_key(request, req_info)
    
    LOG.info("GET {}".format(cache_key))
    
    cache_data = cache.get(cache_key)
    if cache_data and not cfg.CONF.TOOLS.debug:
        return success_resp(cache_data)
    else:
        try:
            query_obj = CiPoet.query.paginate(
                page=req_info['page'],
                per_page=req_info['limits'] if req_info['limits'] else cfg.CONF.TOOLS.pagination,
                error_out=False)
            total = query_obj.total
            poets = [item.poet for item in query_obj.items]
            resp_data = {'total': total, 'poets': poets}
            
            cache.set(cache_key, resp_data)
            
            req_info['limits'] = req_info['limits'] if req_info['limits'] else cfg.CONF.TOOLS.pagination
            req_info['page'] = req_info['page'] if req_info['page'] else 1
            
            return success_resp(req_info, resp_data)
        
        except Exception as e:
            poets = []
            total = 0
            return not_found_resp(req_info)


@poem.route('/shijing', methods=['GET'])
def get_shijing():
    """
    test
    """
    param = request.args
    poem = param.get('poem')
    page = param.get('page', 1, type=int)
    if page:  # 获取诗名翻页数据
        page = int(page)
        if cache.get('poem_num' + 'shijing'):
            total = int(cache.get('poem_num' + 'shijing'))
        else:
            total = len(ShiJing.query.all())
            cache.set('poem_num' + 'shijing', total)
        if cache.get(str(page) + 'shijing'):
            poems = cache.get(str(page) + 'shijing')
        else:
            try:
                items = ShiJing.query.paginate(page=page, per_page=cfg.CONF.TOOLS.pagination, error_out=False).items
                poems = list(set([item.poem for item in items]))
            except Exception as e:
                poems = []
                LOG.error(e)
            cache.set(str(page) + 'shijing', poems)
        return jsonify({
            'code': 200,
            'poems': poems,
            'total': total
        })
    else:  # 获取内容
        LOG.info(poem)
        if cache.get(poem + 'shijing'):
            content = cache.get(poem + 'shijing')
            chapter = cache.get(poem + 'chapter')
            section = cache.get(poem + 'section')
        else:
            try:
                query = ShiJing.query.filter_by(poem=poem).first()
                content = query.content.split('。')
                chapter = query.chapter
                section = query.section
            except Exception as e:
                content = []
                chapter = section = ''
                LOG.error(e)
            cache.set(poem + 'shijing', content)
            cache.set(poem + 'chapter', chapter)
            cache.set(poem + 'section', section)
        return jsonify({
            'code': 200,
            'content': content,
            'chapter': chapter,
            'section': section,
        })


def _make_intro_dict(request):
    """
    make poet's introduction dict
    :param request: wsgi request
    :return: dict
    """
    param = request.args
    return {
        'poet': param.get('poet', '李白'),
        'dynasty': param.get('dynasty', '唐')
    }


@poem.route('/introduction', methods=['GET'])
def get_introduction():
    """
    诗人简介
    """
    req_info = _make_intro_dict(request)
    cache_key = _make_cache_key(request, req_info)
    cache_data = cache.get(cache_key)
    if cache_data and not cfg.CONF.TOOLS.debug:
        return success_resp(req_info, cache_data)
    else:
        try:
            poet_obj = Poet.query.filter(
                Poet.dynasty == req_info['dynasty'],
                Poet.poet == req_info['poet']
            ).first()
            resp_data = poet_obj.to_dict()
            
            cache.set(cache_key, resp_data)
            
            return success_resp(req_info, resp_data)
        except Exception as e:
            LOG.error("Get Introduction Error {}".format(e))
            resp_data = {'msg': 'error'}
            return not_found_resp(resp_data)


def _make_poem_like_dict(request):
    param = request.args
    return {
        'page': param.get('page', 1, type=int),
        'per_page': param.get('per_page', cfg.CONF.TOOLS.pagination, type=int)
    }


def get_poet_intro_by_id(uid):
    """
    get poet intro by id
    :param uid:
    :return:
    """
    return Poet.get_poet_by_id(uid)


@poem.route('/get_poems_by_like', methods=['GET'])
def get_poem_by_like():
    req_info = _make_poem_like_dict(request)
    try:
        query_objs = LikePoem.query.order_by(LikePoem.i_like.desc()).paginate(
            page=req_info['page'],
            per_page=req_info['per_page'],
            error_out=False)
        items = query_objs.items
        resp_data = {
            'poems':
                [{'like': item.i_like,
                  'uid': item.uid,
                  'content': item.content.first().paragraphs.split('｜'),
                  'poem': item.content.first().poem,
                  'poet': get_poet_intro_by_id(item.content.first().poet_id),
                  } for item in items],
            'total': query_objs.total
        }

        return success_resp(req_info, resp_data)
    except Exception as e:
        LOG.error("Get like poem wrong %s" % e)
        resp_data = {'msg': 'error'}
        return not_found_resp(resp_data)


@poem.route('/i_like', methods=['POST'])
def i_like_poem():
    uid = request.get_json()['uid']

    return success_resp({}, {'like': LikePoem.i_like_it(uid)})
