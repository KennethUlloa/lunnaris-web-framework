from unittest import TestCase
from lunnaris.di import Dependency, Lazy, DIContainer, Swappable


class TestLazy(TestCase):
    def test_lazy_import(self):
        import os.path as path

        lazy = Lazy("os.path")
        imp = lazy()
        self.assertEqual(imp, path)

    def test_lazy_import_value(self):
        lazy = Lazy("test.mock.VALUE")
        value = lazy()
        self.assertEqual(value, 1)

    def test_lazy_import_class(self):
        lazy = Lazy("test.mock.MockType")
        value = lazy()
        self.assertEqual(value.__name__, "MockType")

    def test_lazy_import_cached(self):
        lazy = Lazy("test.mock.MockType")
        value1 = lazy()
        value2 = lazy()
        self.assertIs(value1, value2)


class TestDependency(TestCase):
    def test_dependency_reads_annotations(self):
        class Type1:
            def __init__(self):
                pass

        class Type2:
            def __init__(self, param1: Type1) -> None:
                pass

        dependency = Dependency(Type2)

        self.assertIn("param1", dependency.annotations)
        self.assertEqual(dependency.annotations["param1"], Type1)

    def test_dependency_reads_defaults(self):
        def callable1(param1=1, param2="2"):
            pass

        dependency = Dependency(callable1)

        self.assertIn("param1", dependency.defaults)
        self.assertIn("param2", dependency.defaults)
        self.assertEqual(dependency.defaults["param1"], 1)
        self.assertEqual(dependency.defaults["param2"], "2")

    def test_dependency_resolves_type(self):
        class Type1:
            def __init__(self):
                pass

        dependency = Dependency(Type1)

        obj = dependency()

        self.assertIsInstance(obj, Type1)

    def test_dependency_resolves_cached(self):
        class Type1:
            def __init__(self):
                pass

        dependency = Dependency(Type1, cached=True)

        obj1 = dependency()
        obj2 = dependency()

        self.assertIsInstance(obj1, Type1)
        self.assertIsInstance(obj2, Type1)
        self.assertIs(obj1, obj2)

    def test_dependency_resolves_defaults(self):
        def callable1(param1=1, param2="2"):
            return param1, param2

        dependency = Dependency(callable1)

        obj = dependency()

        self.assertEqual(obj, (1, "2"))

    def test_dependency_resolves_lazy(self):
        dependency = Dependency(Lazy("test.mock.MockType"))

        obj = dependency()

        self.assertEqual(obj.__class__.__name__, "MockType")

    def test_swappable_resolves_type(self):
        class Type1:
            def __init__(self):
                pass

        class Type2:
            def __init__(self) -> None:
                pass

        dependency = Swappable(Type2, Type1)

        obj = dependency()
        self.assertIsInstance(obj, Type1)
        self.assertEqual(dependency.key, Type2)

    def test_swappable_resolves_cached(self):
        class Type1:
            def __init__(self):
                pass

        class Type2:
            def __init__(self) -> None:
                pass

        dependency = Swappable(Type2, Type1, cached=True)

        obj1 = dependency()
        obj2 = dependency()

        self.assertIsInstance(obj1, Type1)
        self.assertIsInstance(obj2, Type1)
        self.assertIs(obj1, obj2)


class TestDI(TestCase):
    def test_di_container_resolves_type(self):
        class Type1:
            def __init__(self):
                pass

        di = DIContainer()
        di.add_dependency(Type1)

        obj = di.resolve(Type1)

        self.assertIsInstance(obj, Type1)

    def test_di_container_resolves_cached(self):
        class Type1:
            def __init__(self):
                pass

        di = DIContainer()
        di.add_dependency(Type1, cached=True)

        obj1 = di.resolve(Type1)
        obj2 = di.resolve(Type1)

        self.assertIsInstance(obj1, Type1)
        self.assertIsInstance(obj2, Type1)
        self.assertIs(obj1, obj2)

    def test_di_container_resolves_nested_types(self):
        class Type1:
            def __init__(self):
                pass

        class Type2:
            def __init__(self, param1: Type1) -> None:
                self.type1 = param1

        class Type3:
            def __init__(self, param1: Type1, param2: Type2):
                self.type1 = param1
                self.type2 = param2

        di = DIContainer()
        di.add_dependency(Type1)
        di.add_dependency(Type2)
        di.add_dependency(Type3)

        obj = di.resolve(Type3)

        self.assertIsInstance(obj, Type3)
        self.assertIsInstance(obj.type1, Type1)
        self.assertIsInstance(obj.type2, Type2)
        self.assertIsInstance(obj.type2.type1, Type1)

    def test_di_container_resolves_defaults(self):
        def callable1():
            return "callable1"

        class Type1:  # Value default
            def __init__(self, param1=3):
                self.param1 = param1

        class Type2:  # Callable default
            def __init__(self, param1=callable1) -> None:
                self.param1 = param1

        class Type3:
            def __init__(self, param1=Type1):
                self.param1 = param1

        di = DIContainer()
        di.add_dependency(Type1)
        di.add_dependency(Type2)
        di.add_dependency(Type3)

        obj1 = di.resolve(Type1)
        obj2 = di.resolve(Type2)
        obj3 = di.resolve(Type3)

        self.assertIsInstance(obj1, Type1)
        self.assertEqual(obj1.param1, 3)

        self.assertIsInstance(obj2, Type2)
        self.assertEqual(obj2.param1, "callable1")

        self.assertIsInstance(obj3, Type3)
        self.assertIsInstance(obj3.param1, Type1)
        self.assertEqual(obj3.param1.param1, 3)

    def test_di_container_resolves_lazy(self):
        class Type2:
            def __init__(self, param1=Lazy("test.mock.MockType")) -> None:
                self.param1 = param1

        di = DIContainer()
        di.add_dependency(Lazy("test.mock.MockType"))
        di.add_dependency(Type2)

        obj = di.resolve(Type2)

        self.assertIsInstance(obj, Type2)
        self.assertEqual(obj.param1.__class__.__name__, "MockType")

    def test_di_container_raises_on_undefined_dependency(self):
        class Type1:
            def __init__(self):
                pass

        di = DIContainer()

        with self.assertRaisesRegex(ValueError, "Undefined dependency"):
            di.resolve(Type1)

    def test_di_container_raises_on_nested_undefined_dependency(self):
        class Type1:
            def __init__(self):
                pass

        class Type2:
            def __init__(self, param1: Type1) -> None:
                pass

        di = DIContainer()
        di.add_dependency(Type2)

        with self.assertRaisesRegex(ValueError, "Undefined dependency"):
            di.resolve(Type2)
