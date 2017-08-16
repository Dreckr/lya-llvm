	.section	__TEXT,__text,regular,pure_instructions
	.macosx_version_min 10, 12
	.intel_syntax noprefix
	.globl	_fat
	.p2align	4, 0x90
_fat:                                   ## @fat
	.cfi_startproc
## BB#0:
	push	rbp
Lcfi0:
	.cfi_def_cfa_offset 16
Lcfi1:
	.cfi_offset rbp, -16
	mov	rbp, rsp
Lcfi2:
	.cfi_def_cfa_register rbp
	push	rbx
	push	rax
Lcfi3:
	.cfi_offset rbx, -24
	mov	dword ptr [rbp - 16], edi
	test	edi, edi
	je	LBB0_1
## BB#2:
	mov	ebx, dword ptr [rbp - 16]
	lea	edi, [rbx - 1]
	call	_fat
	imul	eax, ebx
	mov	dword ptr [rbp - 12], eax
	jmp	LBB0_3
LBB0_1:
	mov	dword ptr [rbp - 12], 1
LBB0_3:
	mov	eax, dword ptr [rbp - 12]
	add	rsp, 8
	pop	rbx
	pop	rbp
	ret
	.cfi_endproc

	.globl	_main
	.p2align	4, 0x90
_main:                                  ## @main
	.cfi_startproc
## BB#0:
	push	rbp
Lcfi4:
	.cfi_def_cfa_offset 16
Lcfi5:
	.cfi_offset rbp, -16
	mov	rbp, rsp
Lcfi6:
	.cfi_def_cfa_register rbp
	push	rbx
	push	rax
Lcfi7:
	.cfi_offset rbx, -24
	mov	dword ptr [rbp - 12], 0
	lea	rdi, [rip + L_.str]
	xor	eax, eax
	call	_printf
	lea	rdi, [rip + L_.str.1]
	mov	rbx, qword ptr [rip + _x@GOTPCREL]
	xor	eax, eax
	mov	rsi, rbx
	call	_scanf
	mov	ebx, dword ptr [rbx]
	mov	edi, ebx
	call	_fat
	mov	ecx, eax
	lea	rdi, [rip + L_.str.2]
	xor	eax, eax
	mov	esi, ebx
	mov	edx, ecx
	call	_printf
	xor	eax, eax
	add	rsp, 8
	pop	rbx
	pop	rbp
	ret
	.cfi_endproc

	.section	__TEXT,__cstring,cstring_literals
L_.str:                                 ## @.str
	.asciz	"give-me a positive integer:\n"

L_.str.1:                               ## @.str.1
	.asciz	"%d"

	.comm	_x,4,2                  ## @x
L_.str.2:                               ## @.str.2
	.asciz	"factorial of %d = %d\n"


.subsections_via_symbols
