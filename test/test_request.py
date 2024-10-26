from unittest import TestCase
from lunnaris.request import Json, Request


class TestRequest(TestCase):
    def test_raises_on_get_body_with_GET_method(self):
        req = Request(
            "GET",
            "",
            headers={"content-type": "text/plain"},
            body='{"name":"John Doe","age":22}'
        )

        with self.assertRaisesRegex(ValueError, "GET"):
            req.get_body()


class TestJsonTypeMatcher(TestCase):
    def test_parse_json_from_request(self):
        req = Request(
            "POST",
            "",
            headers={"content-type": "application/json"},
            body='{"name":"John Doe","age":22}'
        )

        class Client:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        expected = Client("John Doe", 22)
        actual = Json(Client).map(req)

        self.assertIsInstance(actual, Client)
        self.assertEqual(expected.age, actual.age)
        self.assertEqual(expected.name, actual.name)
    
    def test_raise_error_on_wrong_content_type(self):
        req = Request(
            "POST",
            "",
            headers={"content-type": "text/plain"},
            body='{"name":"John Doe","age":22}'
        )

        class Any:
            pass

        with self.assertRaisesRegex(ValueError, "Wrong mimetype for converter"):
            Json(Any).map(req)

    def test_raise_error_on_empty_body(self):
        req = Request(
            "POST",
            "",
            headers={"content-type": "application/json"},
            body=''
        )

        class Any:
            pass

        with self.assertRaisesRegex(ValueError, "Empty body"):
            Json(Any).map(req)

    def test_raise_error_on_wrong_method(self):
        req = Request(
            "GET",
            "",
            headers={"content-type": "application/json"},
            body=''
        )

        class Any:
            pass

        with self.assertRaisesRegex(ValueError, "body"):
            Json(Any).map(req)
