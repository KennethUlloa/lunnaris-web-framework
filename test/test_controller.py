from unittest import TestCase
from lunnaris.handler import get
from lunnaris.controller import Controller


class TestController(TestCase):
    def test_get_handlers_empty(self):
        controller = Controller()
        self.assertEqual(controller.get_handlers(), [])

    def test_get_handlers(self):
        class TestController(Controller):
            @get("/")
            def a_handler(self):
                pass

            def some_other_method(self):
                pass

        controller = TestController()
        self.assertEqual(len(controller.get_handlers()), 1)

    def test_get_handlers_with_route(self):
        class TestController(Controller):
            __route__ = "test"

            @get("handler")
            def a_handler(self):
                pass

        controller = TestController()
        handlers = controller.get_handlers()
        self.assertEqual(len(handlers), 1)
        self.assertEqual(handlers[0].path, "/test/handler")
        self.assertEqual(handlers[0].callback, controller.a_handler)