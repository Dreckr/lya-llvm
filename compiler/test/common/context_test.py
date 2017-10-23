import unittest

from compiler.common.context import *

mode = Mode(name="Foo")
symbol = Symbol(name="bar", symbol_type=Type(mode))
definition = Definition(symbol=symbol, register_id=1)
constant = Constant(symbol, 10)


class ScopeTest(unittest.TestCase):

    def setUp(self):
        self.parent_scope = Scope("parent")
        self.scope = Scope(name="child", parent=self.parent_scope)

    def test_put_definition(self):
        self.scope.put_definition(definition)

        self.assertTrue(definition.symbol in self.scope.definitions)

    def test_find_definition(self):
        self.scope.put_definition(definition)

        self.assertEqual(self.scope.find_definition(definition.symbol), definition)

    def test_find_parent_definition(self):
        self.parent_scope.put_definition(definition)

        self.assertEqual(self.scope.find_definition(definition.symbol), definition)

    def test_find_definition_returns_none(self):
        self.assertEqual(self.scope.find_definition(definition.symbol), None)


class LyaContextTest(unittest.TestCase):

    def setUp(self):
        self.context = LyaContext()

    def test_register_symbol(self):
        self.context.register_symbol(symbol)

        self.assertTrue(symbol.name in self.context.symbols)

    def test_find_symbol(self):
        self.context.register_symbol(symbol)

        self.assertEqual(self.context.find_symbol(symbol.name), symbol)

    def test_find_symbol_returns_none(self):
        self.assertEqual(self.context.find_symbol("foo"), None)

    def test_register_mode(self):
        self.context.register_mode(mode)

        self.assertTrue(mode.name in self.context.modes)

    def test_find_mode(self):
        self.context.register_mode(mode)

        self.assertEqual(self.context.find_mode(mode.name), mode)

    def test_find_mode_returns_none(self):
        self.assertEqual(self.context.find_mode("Bar"), None)

    def test_register_constant(self):
        self.context.register_constant(constant)

        self.assertTrue(constant.symbol in self.context.constants)

    def test_find_constant(self):
        self.context.register_constant(constant)

        self.assertEqual(self.context.find_constant(symbol), constant)

    def test_find_constant_returns_none(self):
        self.assertEqual(self.context.find_constant(symbol), None)

    def test_next_register_increments(self):
        self.assertEqual(self.context.next_register(), 1)
        self.assertEqual(self.context.next_register(), 2)
        self.assertEqual(self.context.next_register(), 3)


if __name__ == "__main__":
    unittest.main()
