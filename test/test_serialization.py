from unittest import TestCase
from lunnaris.serializer import Serializer, ExtendedSerializer


class TestSerializer(TestCase):
    def test_serialize(self):
        serializer = Serializer()
        self.assertEqual(serializer.serialize("test"), ("test", "text/html"))
        self.assertEqual(serializer.serialize(1), ("1", "text/html"))
        self.assertEqual(serializer.serialize(1.0), ("1.0", "text/html"))
        self.assertEqual(serializer.serialize(True), ("True", "text/html"))
        self.assertEqual(serializer.serialize(b"test"), ("test", "text/html"))
        self.assertEqual(serializer.serialize({"test": "test"}), ('{"test": "test"}', "application/json"))
        self.assertEqual(serializer.serialize([1, 2, 3]), ("[1, 2, 3]", "application/json"))

    def test_add_serializer(self):
        serializer = Serializer()
        serializer.add_serializer(int, lambda x: str(x))
        self.assertEqual(serializer.serialize(1), ("1", "text/html"))

    def test_add_type_serializer(self):
        class DummyClass:
            def __init__(self, name):
                self.name = name

        def custom_serializer(data):
            return data.name

        serializer = Serializer()
        serializer.add_serializer(DummyClass, custom_serializer)
        self.assertEqual(serializer.serialize(DummyClass("John Doe")), ("John Doe", "text/html"))

    def test_add_object_serializer(self):
        class TestSerializer(ExtendedSerializer):
            def match(self, obj):
                return isinstance(obj, int)

            def serialize(self, obj):
                return str(obj)

        serializer = Serializer()
        serializer.add_object_serializer(TestSerializer())
        self.assertEqual(serializer.serialize(1), ("1", "text/html"))

    def test_type_error(self):
        serializer = Serializer()
        with self.assertRaises(TypeError):
            serializer.serialize(object())
    
    def test_extended_serializer_error(self):
        class TestSerializer(ExtendedSerializer):
            def match(self, obj):
                return False

            def serialize(self, obj):
                return str(obj)

        serializer = Serializer()
        serializer.add_object_serializer(TestSerializer())
        with self.assertRaises(TypeError):
            serializer.serialize(object())
