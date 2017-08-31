
from llvmlite import ir


def main():
    i32 = ir.IntType(32)

    main_function_type = ir.FunctionType(i32, ())

    module = ir.Module(name=__file__)

    main = ir.Function(module, main_function_type, name="main")

    block = main.append_basic_block(name="main")
    builder = ir.IRBuilder(block)

    builder.alloca(i32, 4, '3')

    builder.ret(ir.Constant(i32, 0))

    print(module)

if __name__ == "__main__":
    main()
