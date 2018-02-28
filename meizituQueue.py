from pymongo import MongoClient, errors
from datetime import datetime, timedelta


class MeizituQueue:
    __OUTSTANDING = 1
    __PROCESSING = 2
    __COMPLETED = 3

    def __init__(self, db, collection, timeout=3):
        self.client = MongoClient()
        self.db = self.client[db]
        self.collection = self.db[collection]
        self.timeout = timeout

    def __bool__(self):
        if self.collection.find_one({'status': {'$ne': self.__COMPLETED}}):
            return True
        else:
            return False

    def push(self, url, title):
        try:
            self.collection.insert({'_id': url, 'status': self.__OUTSTANDING, 'title': title})
        except errors.DuplicateKeyError as e:
            print('push', e)
            pass

    def push_imgurl(self, title, url):
        try:
            self.collection.insert({'_id': title, 'status': self.__OUTSTANDING, 'url': url})
        except errors.DuplicateKeyError as e:
            print('push_imgurl', e)

    def pop(self):
        result = None
        try:
            result = self.collection.find_and_modify(query={'status': self.__OUTSTANDING},
                                                     update={'$set': {'status': self.__PROCESSING,
                                                                      'timestamp': datetime.now()}})
        except errors:
            print('pop', errors)

        if result:
            return result['_id']
        else:
            self.repair()
            raise KeyError

    def pop_title(self, url):
        result = self.collection.find_one({'_id': url})
        return result['title']

    def peek(self):
        result = self.collection.find_one({'status': self.__OUTSTANDING})
        if result:
            return result['_id']

    def complete(self, url):
        self.collection.update({'_id': url}, {'$set': {'status': self.__COMPLETED}})

    def repair(self):
        result = self.collection.find_and_modify(
            query={'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.timeout)},
                   'status': self.__PROCESSING}, update={'$set': {'status': self.__OUTSTANDING}})
        if result:
            print('collection', self.collection, '重置url', result['_id'])
