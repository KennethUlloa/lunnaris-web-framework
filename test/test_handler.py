from unittest import TestCase
from lunnaris.handler import RequestHandler, get_handler, get, post, patch, put, delete, request_handler
from lunnaris.request import Query, QueryParam, Request


class TestRequestHandler(TestCase):
    def test_request_handler_decorator(self):
        @request_handler("some_url", "GET", status_code=201, headers={"h1":"v1"})
        def some_func():
            pass

        self.assertTrue(hasattr(some_func, "__handler__"))
        handler: RequestHandler = some_func.__handler__
        self.assertIsInstance(handler, RequestHandler)
        self.assertEqual(handler.path, "some_url")
        self.assertEqual(handler.method, "GET")
        self.assertEqual(handler.status_code, 201)
        self.assertEqual(handler.headers, {"h1":"v1"})
    
    def test_get_handler(self):
        @request_handler("some_url", "GET", status_code=201, headers={"h1":"v1"})
        def some_func():
            pass

        def other_func():
            pass

        handler = get_handler(some_func)
        self.assertIsInstance(handler, RequestHandler)
        handler = get_handler(other_func)
        self.assertIsNone(handler)


    def test_GET_decorator(self):
        @get("path", status_code=201, headers={"h1":"v1"})
        def path():
            pass
        
        self.assertTrue(hasattr(path, "__handler__"))
        handler: RequestHandler = path.__handler__
        self.assertIsInstance(handler, RequestHandler)
        self.assertEqual(handler.path, "path")
        self.assertEqual(handler.method, "GET")
        self.assertEqual(handler.status_code, 201)
        self.assertEqual(handler.headers, {"h1":"v1"})

    def test_POST_decorator(self):
        @post("path", status_code=201, headers={"h1":"v1"})
        def path():
            pass
        
        self.assertTrue(hasattr(path, "__handler__"))
        handler: RequestHandler = path.__handler__
        self.assertIsInstance(handler, RequestHandler)
        self.assertEqual(handler.path, "path")
        self.assertEqual(handler.method, "POST")
        self.assertEqual(handler.status_code, 201)
        self.assertEqual(handler.headers, {"h1":"v1"})

    def test_PUT_decorator(self):
        @put("path", status_code=201, headers={"h1":"v1"})
        def path():
            pass
        
        self.assertTrue(hasattr(path, "__handler__"))
        handler: RequestHandler = path.__handler__
        self.assertIsInstance(handler, RequestHandler)
        self.assertEqual(handler.path, "path")
        self.assertEqual(handler.method, "PUT")
        self.assertEqual(handler.status_code, 201)
        self.assertEqual(handler.headers, {"h1":"v1"})

    def test_PATCH_decorator(self):
        @patch("path", status_code=201, headers={"h1":"v1"})
        def path():
            pass
        
        self.assertTrue(hasattr(path, "__handler__"))
        handler: RequestHandler = path.__handler__
        self.assertIsInstance(handler, RequestHandler)
        self.assertEqual(handler.path, "path")
        self.assertEqual(handler.method, "PATCH")
        self.assertEqual(handler.status_code, 201)
        self.assertEqual(handler.headers, {"h1":"v1"})

    def test_DELETE_decorator(self):
        @delete("path", status_code=201, headers={"h1":"v1"})
        def path():
            pass
        
        self.assertTrue(hasattr(path, "__handler__"))
        handler: RequestHandler = path.__handler__
        self.assertIsInstance(handler, RequestHandler)
        self.assertEqual(handler.path, "path")
        self.assertEqual(handler.method, "DELETE")
        self.assertEqual(handler.status_code, 201)
        self.assertEqual(handler.headers, {"h1":"v1"})
    
    def test_annotated_handler(self):
        @get("path")
        def path(a: int, b: str):
            return f"a={a}, b={b}"
        
        handler = get_handler(path)
        req = Request("GET", "path", params={"a":1, "b":"str"})
        res = handler(req)

        self.assertIsInstance(handler, RequestHandler)
        self.assertEqual(handler.path, "path")
        self.assertEqual(handler.method, "GET")
        self.assertEqual(handler.status_code, 200)
        self.assertEqual(handler.headers, {})
        self.assertEqual(res, "a=1, b=str")

    def test_annotated_handler_with_default(self):
        @get("path")
        def path(a: int = 1, b: str = "str"):
            return f"a={a}, b={b}"
        
        handler = get_handler(path)
        req = Request("GET", "path", params={})
        res = handler(req)

        self.assertIsInstance(handler, RequestHandler)
        self.assertEqual(handler.path, "path")
        self.assertEqual(handler.method, "GET")
        self.assertEqual(handler.status_code, 200)
        self.assertEqual(res, "a=1, b=str")

    def test_annotated_handler_with_query(self):
        @get("path")
        def path(q: dict = Query()):
            return f"q={q}"
        
        handler = get_handler(path)
        req = Request("GET", "path", query={"q":"query"})
        res = handler(req)

        self.assertIsInstance(handler, RequestHandler)
        self.assertEqual(handler.path, "path")
        self.assertEqual(handler.method, "GET")
        self.assertEqual(handler.status_code, 200)
        self.assertEqual(handler.headers, {})
        self.assertEqual(res, "q={'q': 'query'}")

    def test_annotated_handler_with_query_and_default(self):
        @get("path")
        def path(q: dict = Query({"q":"default"})):
            return f"q={q}"
        
        handler = get_handler(path)
        req = Request("GET", "path", query={})
        res = handler(req)

        self.assertIsInstance(handler, RequestHandler)
        self.assertEqual(handler.path, "path")
        self.assertEqual(handler.method, "GET")
        self.assertEqual(handler.status_code, 200)
        self.assertEqual(handler.headers, {})
        self.assertEqual(res, "q={'q': 'default'}")

    def test_annotated_handler_with_query_param(self):
        @get("path")
        def path(q: int = QueryParam()):
            return f"q={q+1}"
        
        handler = get_handler(path)
        req = Request("GET", "path", query={"q":"2", "p":"param"})
        res = handler(req)

        self.assertIsInstance(handler, RequestHandler)
        self.assertEqual(handler.path, "path")
        self.assertEqual(handler.method, "GET")
        self.assertEqual(handler.status_code, 200)
        self.assertEqual(handler.headers, {})
        self.assertEqual(res, "q=3")