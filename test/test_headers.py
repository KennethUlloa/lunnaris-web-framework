from unittest import TestCase
from lunnaris.types import Headers


class TestHeaders(TestCase):
    def test_frozen(self):
        headers = Headers({"Content-Type": "application/json"})
        headers.freeze()
        with self.assertRaises(TypeError):
            headers.clear()
        
        with self.assertRaises(TypeError):
            headers["Content-Type"] = "text/html"
        
        with self.assertRaises(TypeError):
            headers.update({"Content-Type": "text/html"})
        
        with self.assertRaises(TypeError):
            del headers["Content-Type"]

    def test_get(self):
        headers = Headers({"Content-Type": "application/json"})
        self.assertEqual(headers.get("Content-Type"), "application/json")
        self.assertEqual(headers.get("content-type"), "application/json")
        self.assertEqual(headers.get("Content-Type", "text/html"), "application/json")
        self.assertEqual(headers.get("Content-Length"), None)
        self.assertEqual(headers.get("Content-Length", 0), 0)
    
    def test_contains(self):
        headers = Headers({"Content-Type": "application/json"})
        self.assertTrue("Content-Type" in headers)
        self.assertTrue("content-type" in headers)
        self.assertFalse("Content-Length" in headers)
    
    def test_bool(self):
        headers = Headers({"Content-Type": "application/json"})
        self.assertTrue(headers)
        headers.clear()
        self.assertFalse(headers)

    def test_eq(self):
        headers = Headers({"Content-Type": "application/json"})
        headers2 = Headers({"Content-Type": "application/json"})
        self.assertEqual(headers, headers2)
        self.assertEqual(headers, {"Content-Type": "application/json"})
        self.assertNotEqual(headers, {"Content-Type": "text/html"})
        self.assertNotEqual(headers, {"Content-Length": "application/json"})