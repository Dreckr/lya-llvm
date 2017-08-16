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
	mov	dword ptr [rbp - 32], 0
	lea	rdi, [rip + L_.str]
	xor	eax, eax
	call	_printf
	lea	rdi, [rip + L_.str.1]
	lea	rsi, [rbp - 28]
	lea	rdx, [rbp - 24]
	xor	eax, eax
	call	_scanf
	mov	esi, dword ptr [rbp - 28]
	mov	edx, dword ptr [rbp - 24]
	lea	rdi, [rip + L_.str.2]
	xor	eax, eax
	call	_printf
	mov	eax, dword ptr [rbp - 28]
	mov	dword ptr [rbp - 16], eax
	lea	rbx, [rip + L_.str.3]
	jmp	LBB0_1
	.p2align	4, 0x90
LBB0_8:                                 ##   in Loop: Header=BB0_1 Depth=1
	inc	dword ptr [rbp - 16]
LBB0_1:                                 ## =>This Loop Header: Depth=1
                                        ##     Child Loop BB0_3 Depth 2
	mov	eax, dword ptr [rbp - 16]
	cmp	eax, dword ptr [rbp - 24]
	jge	LBB0_9
## BB#2:                                ##   in Loop: Header=BB0_1 Depth=1
	mov	byte ptr [rbp - 9], 1
	mov	dword ptr [rbp - 20], 2
	jmp	LBB0_3
	.p2align	4, 0x90
LBB0_10:                                ##   in Loop: Header=BB0_3 Depth=2
	inc	dword ptr [rbp - 20]
LBB0_3:                                 ##   Parent Loop BB0_1 Depth=1
                                        ## =>  This Inner Loop Header: Depth=2
	mov	eax, dword ptr [rbp - 16]
	mov	ecx, eax
	shr	ecx, 31
	add	ecx, eax
	sar	ecx
	cmp	dword ptr [rbp - 20], ecx
	jge	LBB0_6
## BB#4:                                ##   in Loop: Header=BB0_3 Depth=2
	mov	eax, dword ptr [rbp - 16]
	cdq
	idiv	dword ptr [rbp - 20]
	test	edx, edx
	jne	LBB0_10
## BB#5:                                ##   in Loop: Header=BB0_1 Depth=1
	mov	byte ptr [rbp - 9], 0
LBB0_6:                                 ##   in Loop: Header=BB0_1 Depth=1
	test	byte ptr [rbp - 9], 1
	je	LBB0_8
## BB#7:                                ##   in Loop: Header=BB0_1 Depth=1
	mov	esi, dword ptr [rbp - 16]
	xor	eax, eax
	mov	rdi, rbx
	call	_printf
	jmp	LBB0_8
LBB0_9:
	xor	eax, eax
	add	rsp, 24
	pop	rbx
	pop	rbp
	ret
	.cfi_endproc

	.section	__TEXT,__cstring,cstring_literals
L_.str:                                 ## @.str
	.asciz	"Enter 2 numbers (intervals) separated by space: \n"

L_.str.1:                               ## @.str.1
	.asciz	"%d %d"

L_.str.2:                               ## @.str.2
	.asciz	"Prime numbers between %d and %d are:\n"

L_.str.3:                               ## @.str.3
	.asciz	"%d\n"


.subsections_via_symbols
