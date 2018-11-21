#
#

__author__ = "yu zhang"

import asyncio,logging

import aiomysql

def log(sql,args = ()):
    logging.info("SQL:%s" % sql)

async def create_pool(loop,**kw):
     logging.info("create database connection pool...")
     global __pool
     #新的方法从yield from 转为await
     __pool = await aiomysql.create_pool(host= kw.get("host","localhost"),
                                              port = kw.get("port",3306),
                                              user=kw['user'],
                                              password=kw['password'],
                                              db=kw['db'],
                                              charset=kw.get('charset', 'utf8'),
                                              autocommit=kw.get('autocommit', True),
                                              maxsize=kw.get('maxsize', 10),
                                              minsize=kw.get('minsize', 1),
                                              loop=loop
                                              )


async def select(sql,args,size = None):
     log(sql,args)
     global  __pool
     async with __pool.get() as conn:
          async with  conn.cursor(aiomysql.DictCursor) as cur:
               await  cur.execte(sql.replace("?","%s"),args or ())
               if size:
                    rs = await cur.fetchmany(size)
               else:
                    rs = await cur.fetchall()
               logging.info("rows returnd:%s"%len(rs))
               return rs

async def execute(sql,args,autocommit=True):
     log(sql)
     async with __pool.get() as conn:
          if not autocommit:
               await conn.begin()
          try:
               async with conn.cursor(aiomysql.DictCursor) as cur:
                     await cur.execute(sql.replace("?","%s"),args)
                     affected = cur.rowcount
               if not autocommit:
                    await  conn.commit()
          except BaseException as e:
               if not autocommit:
                    await conn.rollback()
               raise
          return affected
class Field(object):
    def __init__(self,name,column_type,primary_key,default):
        self.name = name;
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
    def __str(self):
        return '<%s, %s:%s>'%(self.__class__.name,self.column_type,self.name)

class ModelMetaclass(type):
    def __new__(cls,name,bases,attrs):
        if name =="Model":
            return type.__new__(cls,name,bases,attrs)
        tableName = attrs.get("__table__",None) or name
        logging.info("found model: %s(table:%s)"%(name,tableName))
        mappings = dict()
        fields = []
        primaryKey = None
        for k,v in attrs.items():
            if isinstance(v,Field):
                logging.info("found mapping:%s====>%s"%(k,v))
                mappings[k] = v
                if v.primary_key:
                    if primaryKey:
                        raise RuntimeError("Duplicate primary key for field: %s"%k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise RuntimeError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f :  '`%s`' %f,fields))
        attrs['__mappings__'] = mappings
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名

        attrs["__select__"] = "select `%s`, %s from `%s`" %(primaryKey,",".join(escaped_fields),tableName)
        attrs['__insert__'] = "insert into `%s` (%s, `%s`) values (%s)" % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (
        tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)


