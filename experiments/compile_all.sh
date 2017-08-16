clang -S c/example1.c -o llvm/example1.ll -emit-llvm
clang -S c/example2.c -o llvm/example2.ll -emit-llvm
clang -S c/factorial.c -o llvm/factorial.ll -emit-llvm
clang -S c/prime.c -o llvm/prime.ll -emit-llvm

llc --x86-asm-syntax=intel llvm/example1.ll -o x86/example1.s
llc --x86-asm-syntax=intel llvm/example2.ll -o x86/example2.s
llc --x86-asm-syntax=intel llvm/factorial.ll -o x86/factorial.s
llc --x86-asm-syntax=intel llvm/prime.ll -o x86/prime.s

clang -mllvm --x86-asm-syntax=intel x86/example1.s -o executable/example1
clang -mllvm --x86-asm-syntax=intel x86/example2.s -o executable/example2
clang -mllvm --x86-asm-syntax=intel x86/factorial.s -o executable/factorial
clang -mllvm --x86-asm-syntax=intel x86/prime.s -o executable/prime