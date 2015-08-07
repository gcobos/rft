import web
from config import db

# Does not work with unicode because of webpy bug!
# http://groups.google.com/group/webpy/browse_thread/thread/baa5b603ec9c692c#

# Tags are not used

def search (query, offset=0, limit=10):
    query = query.strip()
    
    if not query:
        return [], False
    
    def sqlands(left, lst):
        return left + (' and %s ' % left).join(lst)

    q = [str(web.sqlquote(w)) for w in query.split()]
    tag_query = web.sqlors('tag = ', q)

    q = [str(web.sqlquote('%%' + w + '%%')) for w in query.split()]
    where = []
    for c in ['title', 'url', 'description', 'author']:
        where.append(sqlands('%s like ' % c, q))
    text_query = ' or '.join(where)
    
    params = {'tag_query':tag_query, 'text_query':text_query, 
              'offset':offset, 'limit':limit+1, 'size':len(query)}
    
    m = list(db.query('\
    (select distinct m.id, name, aliases, description, author, \
        m.datetime_created as dates \
        from function as m left join tags as t on m.id = t.module_id \
        where %(tag_query)s \
        group by t.module_id \
        having count(t.module_id) >= %(size)d) \
    union \
    (select distinct m.id, name, aliases, description, author, \
        m.datetime_created as dates \
        from function as m \
        where %(text_query)s \
        order by datetime_created desc) \
    order by votes desc, dates desc limit %(limit)d offset %(offset)d' \
    % params))
    
    has_next = len(m) > limit
    
    return m[:limit], has_next

