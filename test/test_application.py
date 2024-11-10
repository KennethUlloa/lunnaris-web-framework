from unittest import TestCase
from lunnaris.application import Application
from lunnaris.handler import get
from lunnaris.request import Request
from lunnaris.response import Response
from lunnaris.routes import RouteMatcher


class TestApplication(TestCase):
    def test_request_lifecycle(self):
        @get("/")
        def handler():
            return "Hello, world!"
        app = Application()
        app.add_function_handler(handler)

        req = Request("GET", "/")
        res = app.run(req)

        self.assertIsInstance(res, Response)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.body, b"Hello, world!")
        self.assertEqual(res.headers["Content-Type"], "text/html")
    
    def test_request_not_found(self):
        app = Application(router=RouteMatcher())
        req = Request("GET", "/")
        res = app.run(req)

        self.assertIsInstance(res, Response)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.body, b"404 - Resource not found")
        self.assertEqual(res.headers["Content-Type"], "text/plain")
    
    def test_request_internal_server_error(self):
        @get("/")
        def handler():
            raise ValueError("Error")
        app = Application()
        app.add_function_handler(handler)

        req = Request("GET", "/")
        res = app.run(req)

        self.assertIsInstance(res, Response)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.body, b"500 - Internal server error")
        self.assertEqual(res.headers["Content-Type"], "text/plain")
    
    def test_request_custom_exception(self):
        class CustomException(Exception):
            pass
        
        @get("/")
        def handler():
            raise CustomException()
        
        app = Application()
        app.add_function_handler(handler)

        req = Request("GET", "/")
        res = app.run(req)

        self.assertIsInstance(res, Response)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.body, b"500 - Internal server error")
        self.assertEqual(res.headers["Content-Type"], "text/plain")
    
    def test_request_custom_exception_handler(self):
        app = Application()
        class CustomException(Exception):
            pass
        
        @get("/")
        def handler():
            raise CustomException()
        
        def custom_handler(e):
            return Response(418, b"I'm a teapot")
        
        app.add_function_handler(handler)
        app.add_exception_handler(CustomException, custom_handler)

        req = Request("GET", "/")
        res = app.run(req)
        self.assertIsInstance(res, Response)
        self.assertEqual(res.status_code, 418)
        self.assertEqual(res.body, b"I'm a teapot")
        self.assertEqual(res.headers["Content-Type"], "text/html")

    def test_serialization(self):
        @get("/")
        def handler():
            return {"name": "John Doe"}
        
        app = Application()
        app.add_function_handler(handler)

        req = Request("GET", "/")
        res = app.run(req)

        self.assertIsInstance(res, Response)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.body, b'{"name": "John Doe"}')
        self.assertEqual(res.headers["Content-Type"], "application/json")

    def test_custom_serialization(self):
        class DummyClass:
            def __init__(self, name):
                self.name = name

        @get("/")
        def handler():
            return DummyClass("John Doe")
        
        def custom_serializer(data):
            return f"<name>{data.name}</name>", "application/xml"
        
        app = Application()
        app.serializer.add_serializer(DummyClass, custom_serializer)
        app.add_function_handler(handler)

        req = Request("GET", "/")
        res = app.run(req)

        self.assertIsInstance(res, Response)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.body, b'<name>John Doe</name>')
        self.assertEqual(res.headers["Content-Type"], "application/xml")