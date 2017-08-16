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
	push	r15
	push	r14
	push	rbx
	push	rax
Lcfi3:
	.cfi_offset rbx, -40
Lcfi4:
	.cfi_offset r14, -32
Lcfi5:
	.cfi_offset r15, -24
	mov	dword ptr [rbp - 28], 0
	mov	rbx, qword ptr [rip + _z@GOTPCREL]
	mov	dword ptr [rbx], 4
	mov	r15, qword ptr [rip + _t@GOTPCREL]
	mov	dword ptr [r15], 4
	mov	edi, 4
	call	_g
	mov	esi, dword ptr [rbx]
	mov	edx, dword ptr [r15]
	lea	r14, [rip + L_.str]
	xor	eax, eax
	mov	rdi, r14
	call	_printf
	mov	edi, dword ptr [rbx]
	call	_g
	mov	esi, dword ptr [rbx]
	mov	edx, dword ptr [r15]
	xor	eax, eax
	mov	rdi, r14
	call	_printf
	mov	edi, dword ptr [r15]
	add	edi, dword ptr [rbx]
	call	_g
	mov	esi, dword ptr [rbx]
	mov	edx, dword ptr [r15]
	xor	eax, eax
	mov	rdi, r14
	call	_printf
	mov	edi, 7
	call	_g
	mov	esi, dword ptr [rbx]
	mov	edx, dword ptr [r15]
	xor	eax, eax
	mov	rdi, r14
	call	_printf
	xor	eax, eax
	add	rsp, 8
	pop	rbx
	pop	r14
	pop	r15
	pop	rbp
	ret
	.cfi_endproc

	.globl	_g
	.p2align	4, 0x90
_g:                                     ## @g
	.cfi_startproc
## BB#0:
	push	rbp
Lcfi6:
	.cfi_def_cfa_offset 16
Lcfi7:
	.cfi_offset rbp, -16
	mov	rbp, rsp
Lcfi8:
	.cfi_def_cfa_register rbp
                                        ## kill: %EDI<def> %EDI<kill> %RDI<def>
	mov	dword ptr [rbp - 4], edi
	lea	eax, [rdi + rdi]
	mov	dword ptr [rbp - 4], eax
	lea	eax, [4*rdi]
	mov	dword ptr [rbp - 8], eax
	lea	eax, [4*rdi + 1]
	mov	rcx, qword ptr [rip + _z@GOTPCREL]
	mov	dword ptr [rcx], eax
	pop	rbp
	ret
	.cfi_endproc

	.comm	_z,4,2                  ## @z
	.comm	_t,4,2                  ## @t
	.section	__TEXT,__cstring,cstring_literals
L_.str:                                 ## @.str
	.asciz	"%d %d\n"


.subsections_via_symbols
