from ctypes import CFUNCTYPE, c_int32

import llvmlite.binding as llvm

from compiler.codegen.llvm_codegen_visitor import LLVMCodeGenVisitor
from compiler.semantic.procedure_definition_visitor import ProcedureDefinitionVisitor
from compiler.semantic.symbol_declaration_visitor import SymbolDefinitionVisitor
from compiler.common.context import LyaContext
from compiler.syntatic.parser import parser
from compiler.main import print_visit


class LyaVM:

    def __init__(self):
        self.context = LyaContext()
        self.procedure_definition_visitor = ProcedureDefinitionVisitor(self.context)
        self.symbol_definition_visitor = SymbolDefinitionVisitor(self.context)
        self.llvm_codegen_visitor = LLVMCodeGenVisitor(self.context)

        # All these initializations are required for code generation!
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()  # yes, even this one

        llvm.load_library_permanently("liblya.so")

    def execute(self, lya_program):
        lya_ast = parser.parse(lya_program)
        print_visit(lya_ast)

        print()

        self.procedure_definition_visitor.visit(lya_ast)
        self.symbol_definition_visitor.visit(lya_ast)
        module = self.llvm_codegen_visitor.visit_program(lya_ast)

        # Print the module IR
        print(str(module))

        engine = self.create_execution_engine()
        mod = self.compile_ir(engine, str(module))

        # Look up the function pointer (a Python int)
        func_ptr = engine.get_function_address("main")

        # Run the function via ctypes
        cfunc = CFUNCTYPE(c_int32)(func_ptr)
        result = cfunc()
        print(result)

    def create_execution_engine(self):
        """
        Create an ExecutionEngine suitable for JIT code generation on
        the host CPU.  The engine is reusable for an arbitrary number of
        modules.
        """
        # Create a target machine representing the host
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        # And an execution engine with an empty backing module
        backing_mod = llvm.parse_assembly("")
        engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
        return engine

    def compile_ir(self, engine, llvm_ir):
        """
        Compile the LLVM IR string with the given engine.
        The compiled module object is returned.
        """
        # Create a LLVM module object from the IR
        mod = llvm.parse_assembly(llvm_ir)
        mod.verify()
        # Now add the module and make sure it is ready for execution
        engine.add_module(mod)
        engine.finalize_object()
        return mod


test_program = """
    dcl a int = 10, b int = 12 + 2;
    dcl c int = 3 + 1, e bool = 10 == b, f bool = e == true;
    
    a = a + c + b;
    b = a + 4;
    
    print(f);
    
    foo: proc(a int, b int) returns (int);
        return a + b;
    end;
    
    bar: proc(a int loc, b int) returns (int);
        a = 10;
        return a + b;
    end;
    
    bar(a, 12);
    
    print(a);
    print(b);
    
    a = foo(a, b);
    
    print(a);
    
    if b > 10 then 
        foo(a + b, b);
        
        b = b - 20;
    fi;
    
    do while b > 0;
        foo(a + b, b * 2);
        b = b - 1;
    od;
"""

lyaVM = LyaVM()
lyaVM.execute(test_program)
