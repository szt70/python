# -*- coding: utf-8 -*-
import sys
import time
from gensim.models import word2vec
import falcon
import urllib
import json
from wsgiref import simple_server
import traceback
import logging

#logger
logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
log_fmt = '[%(asctime)s] %(levelname)s - %(filename)s#%(funcName)s:%(lineno)d: %(message)s'
logging.basicConfig(format=log_fmt)

def load_model():
  global model
  timeStart = time.clock();
  model = word2vec.Word2Vec.load("sample.model")
  timeTotal = round(time.clock() - timeStart, 3)
  logging.debug("load model ... {0}s".format(timeTotal))

def get_keywords(out):
  keywords = []
  for x in out:
    keywords.append(x[0])
  return keywords


class ItemsResource:
    def on_get(self, req, resp):
        resp.content_type = 'text/plain'
        key = req.params['key']
        try:
            out = model.most_similar(positive=[key], topn=3)
            words = get_keywords(out)
            resp_str = json.dumps(words,ensure_ascii=False)
            resp.status = falcon.HTTP_200
            resp.content_type = 'text/plain'
            resp.body = str(words)

        except KeyError:
            logging.exception("not found word : " + key, traceback.format_exc())
            resp.status = falcon.HTTP_500
            resp.content_type = 'text/plain'
            resp.body = ""


load_model()
api = falcon.API()
api.add_route('/cooccur_word', ItemsResource())

httpd = simple_server.make_server("127.0.0.1", 8000, api)
httpd.serve_forever()

