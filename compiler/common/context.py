# Glossary
# Symbol - Variable
# Mode - Type
# Procedure - Function


class Mode:
    """
    A type in Lya.

    A mode can be one of the native types (bool, char, int) or it can be a struct composed of several fields.
    """

    def __init__(self, name, is_struct=False, fields=None, size_in_bytes=1):
        self.name = name
        self.is_struct = is_struct
        self.fields = fields
        self.size_in_bytes = size_in_bytes

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        return hash((self.name, self.is_struct, self.fields, self.size_in_bytes))


class Type:

    def __init__(self, mode, is_reference=False, is_array=False, array_size=None):
        self.mode = mode
        self.is_reference = is_reference
        self.is_array = is_array
        self.array_size = array_size

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        return hash((self.mode.__hash__(), self.is_reference, self.is_array, self.array_size))


class Field:
    """
    A field of a struct in Lya.
    """

    def __init__(self, name, field_type):
        self.name = name
        self.type = field_type

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        return hash((self.name, self.type.__hash__()))


class Symbol:
    """
    A variable in Lya.

    A symbol is defined as a name associated with a type.
    """

    def __init__(self, name, symbol_type):
        self.name = name
        self.type = symbol_type

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        return hash((self.name, self.type.__hash__()))


class Definition:
    """
    An attribution of a value to a symbol.

    This class is used to track the register of the last definition of a variable.
    """

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        return hash((self.name.__hash__(), self.value.__hash__()))


class Constant:
    """
    A compilation time constant value attributed to a symbol.

    Constant values can be used to describe the size of arrays or be used in expressions.
    """

    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        return hash((self.symbol.__hash__(), self.value))


class Procedure:
    """
    A definition of function.

    Procedures are named and have ordinal mandatory parameters. A procedure may or may not have a return type.
    Parameters are defined as symbols inside the scope of the procedure.
    """

    def __init__(self, name, parameters=list(), return_type=None):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        return hash((self.name, self.parameters, self.return_type))


class Alias:
    """
    An alias for a mode.

    Provides a way to define multiple names to the same mode.
    """

    def __init__(self, name, mode):
        self.name = name
        self.mode = mode

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        return hash((self.name, self.mode.__hash__()))


class Label:

    def __init__(self, name, position):
        self.name = name
        self.position = position

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        return hash((self.name, self.position))


class Scope:

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.definitions = dict()

    def find_definition(self, symbol_name):
        definition = None

        if symbol_name in self.definitions:
            definition = self.definitions[symbol_name]
        elif self.parent is not None:
            definition = self.parent.find_definition(symbol_name)

        return definition

    def put_definition(self, definition):
        self.definitions[definition.symbol] = definition

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

INT_MODE = Mode("int")
BOOL_MODE = Mode("bool")
CHAR_MODE = Mode("char")
EMPTY_MODE = Mode("null")
STRING_MODE = Mode("string")


class LyaContext:

    def __init__(self):
        self.symbols = dict()
        self.modes = dict()
        self.constants = dict()
        self.scopes = dict()
        self.procedures = dict()
        self.aliases = dict()
        self.labels = dict()
        self.definitions = dict()

        self.root_scope = Scope("root")
        self.scopes[self.root_scope.name] = self.root_scope
        self.current_scope = self.root_scope

        self.register_mode(INT_MODE)
        self.register_mode(BOOL_MODE)
        self.register_mode(CHAR_MODE)
        self.register_mode(STRING_MODE)
        self.register_mode(EMPTY_MODE)

    def register_scope(self, scope):
        self.scopes[scope.name] = scope

    def enter_scope(self, scope_name):
        if scope_name not in self.scopes:
            raise ScopeNotRegisteredException()

        self.current_scope = self.scopes[scope_name]
        
    def register_symbol(self, symbol):
        self.symbols[symbol.name] = symbol
        
    def find_symbol(self, symbol_name):
        if symbol_name not in self.symbols:
            return None

        return self.symbols[symbol_name]
        
    def register_mode(self, mode):
        self.modes[mode.name] = mode
        
    def find_mode(self, mode_name):
        if mode_name not in self.modes:
            return None

        return self.modes[mode_name]
        
    def register_constant(self, constant):
        self.constants[constant.symbol] = constant
        
    def find_constant(self, symbol):
        if symbol not in self.constants:
            return None

        return self.constants[symbol]

    def register_alias(self, alias):
        self.aliases[alias.name] = alias

    def find_alias(self, alias_name):
        if alias_name not in self.aliases:
            return None

        return self.aliases[alias_name]

    def register_label(self, label):
        self.labels[label.name] = label

    def find_label(self, label_name):
        if label_name not in self.labels:
            return None

        return self.labels[label_name]

    def register_procedure(self, procedure):
        self.procedures[procedure.name] = procedure

    def find_procedure(self, procedure_name):
        if procedure_name not in self.procedures:
            return None

        return self.procedures[procedure_name]

    def register_definition(self, definition):
        self.definitions[definition.name] = definition

    def find_definition(self, name):
        if name not in self.definitions:
            return None

        return self.definitions[name]


class ScopeNotRegisteredException(Exception):

    def __init__(self):
        pass
