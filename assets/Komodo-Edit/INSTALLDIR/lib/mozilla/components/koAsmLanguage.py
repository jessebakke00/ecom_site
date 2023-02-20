# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
# 
# The contents of this file are subject to the Mozilla Public License
# Version 1.1 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
# 
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
# License for the specific language governing rights and limitations
# under the License.
# 
# The Original Code is Komodo code.
# 
# The Initial Developer of the Original Code is ActiveState Software Inc.
# Portions created by ActiveState Software Inc are Copyright (C) 2000-2007
# ActiveState Software Inc. All Rights Reserved.
# 
# Contributor(s):
#   ActiveState Software Inc
# 
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
# 
# ***** END LICENSE BLOCK *****

from xpcom import components, ServerException

from koLanguageServiceBase import *

class koAsmLanguage(KoLanguageBase):
    name = "Assembler"
    _reg_desc_ = "%s Language" % name
    _reg_contractid_ = "@activestate.com/koLanguage?language=%s;1" \
                       % (name)
    _reg_clsid_ = "{118a7eda-be0f-41e3-ac27-32c32db32583}"
    _reg_categories_ = [("komodo-language", name)]

    _stateMap = {
        'operators': ('SCE_ASM_OPERATOR',),
        'directives': ('SCE_ASM_DIRECTIVE',
                       'SCE_ASM_DIRECTIVEOPERAND',),
        'instructions': ('SCE_ASM_CPUINSTRUCTION',
                         'SCE_ASM_MATHINSTRUCTION',
                         'SCE_ASM_EXTINSTRUCTION',),
        'register': ('SCE_ASM_REGISTER',),
        'default': ('SCE_ASM_DEFAULT',),
        'numbers': ('SCE_ASM_NUMBER',),
        'identifiers': ('SCE_ASM_IDENTIFIER',),
        'strings': ('SCE_ASM_STRING',
                    'SCE_ASM_CHARACTER',),
        'comments': ('SCE_ASM_COMMENT',
                     'SCE_ASM_COMMENTBLOCK',),
        'stringeol': ('SCE_ASM_STRINGEOL',),
        }
    defaultExtension = '.asm'
    commentDelimiterInfo = { "line": [ ";" ]  }
    _dedenting_statements = [u'.endif']
    
    sample = """
SAMPLE NOT AVAILABLE
"""
    def get_lexer(self):
        if self._lexer is None:
            self._lexer = KoLexerLanguageService()
            self._lexer.setLexer(components.interfaces.ISciMoz.SCLEX_ASM)
            self._lexer.setKeywords(0, self.cpu_instruction + self.cpu_instruction2)
            self._lexer.setKeywords(1, self.fpu_instruction)
            self._lexer.setKeywords(2, self.register)
            self._lexer.setKeywords(3, self.directive + self.directive_nasm)
            self._lexer.setKeywords(4, self.directive_operand + self.directive_operand_nasm)
            self._lexer.setKeywords(5, self.ext_instruction)
        return self._lexer


    cpu_instruction="""aaa aad aam aas adc add and call cbw
        clc cld cli cmc cmp cmps cmpsb cmpsw cwd daa das dec div esc hlt
        idiv imul in inc int into iret ja jae jb jbe jc jcxz je jg jge jl
        jle jmp jna jnae jnb jnbe jnc jne jng jnge jnl jnle jno jnp jns
        jnz jo jp jpe jpo js jz lahf lds lea les lods lodsb lodsw loop
        loope loopew loopne loopnew loopnz loopnzw loopw loopz loopzw
        mov movs movsb movsw mul neg nop not or out pop popf push pushf
        rcl rcr ret retf retn rol ror sahf sal sar sbb scas scasb scasw
        shl shr stc std sti stos stosb stosw sub test wait xchg xlat
        xlatb xor
        bound enter ins insb insw leave outs outsb outsw popa pusha pushw
        arpl lar lsl sgdt sidt sldt smsw str verr verw clts lgdt lidt lldt lmsw ltr
        bsf bsr bt btc btr bts cdq cmpsd cwde insd iretd iretdf  iretf
        jecxz lfs lgs lodsd loopd  looped  loopned  loopnzd  loopzd  lss
        movsd movsx movzx outsd popad popfd pushad pushd  pushfd scasd seta
        setae setb setbe setc sete setg setge setl setle setna setnae setnb
        setnbe setnc setne setng setnge setnl setnle setno setnp setns
        setnz seto setp setpe setpo sets setz shld shrd stosd
        bswap cmpxchg invd  invlpg  wbinvd  xadd
        lock rep repe repne repnz repz""".split()

    # these are mostly non-MMX/SSE/SSE2 486+ instructions
    
    cpu_instruction2="""cflush cpuid emms femms
            cmovo cmovno cmovb cmovc cmovnae cmovae cmovnb cmovnc
            cmove cmovz cmovne cmovnz cmovbe cmovna cmova cmovnbe
            cmovs cmovns cmovp cmovpe cmovnp cmovpo cmovl cmovnge
            cmovge cmovnl cmovle cmovng cmovg cmovnle
            cmpxchg486 cmpxchg8b 
            loadall loadall286 ibts icebp int1 int3 int01 int03 iretw
            popaw popfw pushaw pushfw rdmsr rdpmc rdshr rdtsc
            rsdc rsldt rsm rsts salc smi smint smintold svdc svldt svts
            syscall sysenter sysexit sysret ud0 ud1 ud2 umov
            xbts wrmsr wrshr""".split()
    
    # fpu instructions, updated for 486+
    
    fpu_instruction="""f2xm1 fabs fadd faddp fbld fbstp fchs fclex fcom fcomp fcompp fdecstp
            fdisi fdiv fdivp fdivr fdivrp feni ffree fiadd ficom ficomp fidiv
            fidivr fild fimul fincstp finit fist fistp fisub fisubr fld fld1
            fldcw fldenv fldenvw fldl2e fldl2t fldlg2 fldln2 fldpi fldz fmul
            fmulp fnclex fndisi fneni fninit fnop fnsave fnsavew fnstcw fnstenv
            fnstenvw fnstsw fpatan fprem fptan frndint frstor frstorw fsave
            fsavew fscale fsqrt fst fstcw fstenv fstenvw fstp fstsw fsub fsubp
            fsubr fsubrp ftst fwait fxam fxch fxtract fyl2x fyl2xp1
            fsetpm fcos fldenvd fnsaved fnstenvd fprem1 frstord fsaved fsin fsincos
            fstenvd fucom fucomp fucompp fcomi fcomip ffreep
            fcmovb fcmove fcmovbe fcmovu fcmovnb fcmovne fcmovnbe
            fcmovnu""".split()
    
    # these are MMX, SSE, SSE2 instructions
    
    ext_instruction="""addpd addps addsd addss andpd andps andnpd andnps
            cmpeqpd cmpltpd cmplepd cmpunordpd cmpnepd cmpnltpd cmpnlepd cmpordpd
            cmpeqps cmpltps cmpleps cmpunordps cmpneps cmpnltps cmpnleps cmpordps
            cmpeqsd cmpltsd cmplesd cmpunordsd cmpnesd cmpnltsd cmpnlesd cmpordsd
            cmpeqss cmpltss cmpless cmpunordss cmpness cmpnltss cmpnless cmpordss
            comisd comiss cvtdq2pd cvtdq2ps cvtpd2dq cvtpd2pi cvtpd2ps
            cvtpi2pd cvtpi2ps cvtps2dq cvtps2pd cvtps2pi cvtss2sd cvtss2si
            cvtsd2si cvtsd2ss cvtsi2sd cvtsi2ss
            cvttpd2dq cvttpd2pi cvttps2dq cvttps2pi cvttsd2si cvttss2si
            divpd divps divsd divss fxrstor fxsave ldmxscr lfence mfence
            maskmovdqu maskmovdq maxpd maxps paxsd maxss minpd minps minsd minss
            movapd movaps movdq2q movdqa movdqu movhlps movhpd movhps movd movq
            movlhps movlpd movlps movmskpd movmskps movntdq movnti movntpd movntps
            movntq movq2dq movsd movss movupd movups mulpd mulps mulsd mulss
            orpd orps packssdw packsswb packuswb paddb paddsb paddw paddsw
            paddd paddsiw paddq paddusb paddusw pand pandn pause paveb pavgb pavgw
            pavgusb pdistib pextrw pcmpeqb pcmpeqw pcmpeqd pcmpgtb pcmpgtw pcmpgtd
            pf2id pf2iw pfacc pfadd pfcmpeq pfcmpge pfcmpgt pfmax pfmin pfmul
            pmachriw pmaddwd pmagw pmaxsw pmaxub pminsw pminub pmovmskb
            pmulhrwc pmulhriw pmulhrwa pmulhuw pmulhw pmullw pmuludq
            pmvzb pmvnzb pmvlzb pmvgezb pfnacc pfpnacc por prefetch prefetchw
            prefetchnta prefetcht0 prefetcht1 prefetcht2 pfrcp pfrcpit1 pfrcpit2
            pfrsqit1 pfrsqrt pfsub pfsubr pi2fd pf2iw pinsrw psadbw pshufd
            pshufhw pshuflw pshufw psllw pslld psllq pslldq psraw psrad
            psrlw psrld psrlq psrldq psubb psubw psubd psubq psubsb psubsw
            psubusb psubusw psubsiw pswapd punpckhbw punpckhwd punpckhdq punpckhqdq
            punpcklbw punpcklwd punpckldq punpcklqdq pxor rcpps rcpss
            rsqrtps rsqrtss sfence shufpd shufps sqrtpd sqrtps sqrtsd sqrtss
            stmxcsr subpd subps subsd subss ucomisd ucomiss
            unpckhpd unpckhps unpcklpd unpcklps xorpd xorps""".split()
    
    register="""ah al ax bh bl bp bx ch cl cr0 cr2 cr3 cr4 cs
            cx dh di dl dr0 dr1 dr2 dr3 dr6 dr7 ds dx eax ebp ebx ecx edi edx
            es esi esp fs gs si sp ss st tr3 tr4 tr5 tr6 tr7
            st0 st1 st2 st3 st4 st5 st6 st7 mm0 mm1 mm2 mm3 mm4 mm5 mm6 mm7
            xmm0 xmm1 xmm2 xmm3 xmm4 xmm5 xmm6 xmm7""".split()
    
    # masm directives
    
    directive=""".186 .286 .286c .286p .287 .386 .386c .386p .387 .486 .486p
            .8086 .8087 .alpha .break .code .const .continue .cref .data .data? 
            .dosseg .else .elseif .endif .endw .err .err1 .err2 .errb
            .errdef .errdif .errdifi .erre .erridn .erridni .errnb .errndef
            .errnz .exit .fardata .fardata? .if .lall .lfcond .list .listall
            .listif .listmacro .listmacroall  .model .no87 .nocref .nolist
            .nolistif .nolistmacro .radix .repeat .sall .seq .sfcond .stack
            .startup .tfcond .type .until .untilcxz .while .xall .xcref
            .xlist alias align assume catstr comm comment db dd df dosseg dq
            dt dup dw echo else elseif elseif1 elseif2 elseifb elseifdef elseifdif
            elseifdifi elseife elseifidn elseifidni elseifnb elseifndef end
            endif endm endp ends eq equ even exitm extern externdef extrn for
            forc ge goto group gt high highword if if1 if2 ifb ifdef ifdif
            ifdifi ife  ifidn ifidni ifnb ifndef include includelib instr invoke
            irp irpc label le length lengthof local low lowword lroffset
            lt macro mask mod .msfloat name ne offset opattr option org %out
            page popcontext proc proto ptr public purge pushcontext record
            repeat rept seg segment short size sizeof sizestr struc struct
            substr subtitle subttl textequ this title type typedef
            union while width""".split()
    
    directive_operand="""$ ? @b @f addr basic byte c carry? dword
            far far16 fortran fword near near16 overflow? parity? pascal qword 
            real4  real8 real10 sbyte sdword sign? stdcall sword syscall tbyte
            vararg word zero? flat near32 far32
            abs all assumes at casemap common compact
            cpu dotname emulator epilogue error export expr16 expr32 farstack flat
            forceframe huge language large listing ljmp loadds m510 medium memory
            nearstack nodotname noemulator nokeyword noljmp nom510 none nonunique
            nooldmacros nooldstructs noreadonly noscoped nosignextend nothing
            notpublic oldmacros oldstructs os_dos para private prologue radix
            readonly req scoped setif2 smallstack tiny use16 use32 uses""".split()
    
    # nasm directives, mostly complete, does not parse properly
    # the following: %!<env>, %%, %+, %+n %-n, %{n}
    
    directive_nasm="""db dw dd dq dt resb resw resd resq rest incbin equ times
            %define %idefine %xdefine %xidefine %undef %assign %iassign
            %strlen %substr %macro %imacro %endmacro %rotate .nolist
            %if %elif %else %endif %ifdef %ifndef %elifdef %elifndef
            %ifmacro %ifnmacro %elifmacro %elifnmacro %ifctk %ifnctk %elifctk %elifnctk
            %ifidn %ifnidn %elifidn %elifnidn %ifidni %ifnidni %elifidni %elifnidni
            %ifid %ifnid %elifid %elifnid %ifstr %ifnstr %elifstr %elifnstr
            %ifnum %ifnnum %elifnum %elifnnum %error %rep %endrep %exitrep
            %include %push %pop %repl struct endstruc istruc at iend align alignb
            %arg %stacksize %local %line
            bits use16 use32 section absolute extern global common cpu org
            section group import export""".split()
    
    directive_operand_nasm="""a16 a32 o16 o32 byte word dword nosplit $ $$ seq wrt
            flat large small .text .data .bss near far
            %0 %1 %2 %3 %4 %5 %6 %7 %8 %9""".split()

