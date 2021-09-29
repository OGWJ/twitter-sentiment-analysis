# from werkzeug.wrappers import Request, Respone, ResponseStream
from werkzeug import wrappers

class QueryChecker:

    def __init__(self, app):
        self.app = app;
        self.invalid_query_error = 'Error: query should be in THIS format'


    def __call__(self, environ, start_response):

        req = wrappers.Request(environ)
        #params = req.params # or url

        query = self.get_query_from_url(req.url)
        print(query)

        if not self.is_valid_query(query):
            res = wrappers.Response(self.invalid_query_error)
            return res(environ, start_response)

        # successful path
        return self.app(environ, start_response)

    def get_query_from_url(self, url):
        # eval components to determine route
        components = url.split('/')
        query = components[-1]

        for i, component in enumerate(components):
            if component == 'sentiment' or component == 'future' and i != len(components)-1:
                query = components[i+1]

        print('query at middleware', query)

        return query


    def is_valid_query(self, query):

        if len(query) > 500 or len(query) < 1:
            return False

        # TODO: check operators, add more invalid chars
        #       maybe use whitelist instead of blacklist

        invalid_chars = '^*'

        for i, char in enumerate(query):
            if char in invalid_chars:
                return False
            # check for leading spaces
            elif i == 0 and char == ' ':
                return False
            # check for trailing spaces
            elif i == len(query) - 1 and char == ' ':
                return False
            #check for double spaces
            elif char == ' ':
                # check for double spaces
                if i < len(query) and query[i+1] == ' ':
                    return False

        return True


    def is_valid_operator(self, op):
        return True

