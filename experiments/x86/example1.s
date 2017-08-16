	.section	__TEXT,__text,regular,pure_instructions
	.macosx_version_min 10, 12
	.intel_syntax noprefix
	.globl	_main
	.p2align	4, 0x90
_main:                                  ## @main
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
	sub	rsp, 24
Lcfi3:
	.cfi_offset rbx, -24
	mov	dword ptr [rbp - 24], 0
	lea	rdi, [rip + L_.str]
	lea	rsi, [rbp - 12]
	lea	rdx, [rbp - 20]
	xor	eax, eax
	call	_scanf
	mov	dword ptr [rbp - 16], 0
	lea	rbx, [rip + L_.str.1]
	jmp	LBB0_1
	.p2align	4, 0x90
LBB0_2:                                 ##   in Loop: Header=BB0_1 Depth=1
	mov	edx, dword ptr [rbp - 12]
	imul	edx, dword ptr [rbp - 20]
	add	edx, dword ptr [rbp - 16]
	mov	dword ptr [rbp - 16], edx
	mov	esi, dword ptr [rbp - 12]
	xor	eax, eax
	mov	rdi, rbx
	call	_printf
	inc	dword ptr [rbp - 12]
LBB0_1:                                 ## =>This Inner Loop Header: Depth=1
	mov	eax, dword ptr [rbp - 12]
	cmp	eax, dword ptr [rbp - 20]
	jle	LBB0_2
## BB#3:
	xor	eax, eax
	add	rsp, 24
	pop	rbx
	pop	rbp
	ret
	.cfi_endproc

	.section	__TEXT,__cstring,cstring_literals
L_.str:                                 ## @.str
	.asciz	"%d %d"

L_.str.1:                               ## @.str.1
	.asciz	"%d %d\n"


.subsections_via_symbols
