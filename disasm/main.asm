    section "rom0_3FA3", rom0[$3FA3]

Code_3FA3: ; 00:3FA3
    /* 00:3FA3 */ push af
    /* 00:3FA4 */ push bc
    /* 00:3FA5 */ push de
    /* 00:3FA6 */ push hl
    /* 00:3FA7 */ ld a, [de]
    /* 00:3FA8 */ add a, 3
    /* 00:3FAA */ ld c, a
    /* 00:3FAB */ inc de
    /* 00:3FAC */ ld h, HIGH($7000)
    /* 00:3FAE */ ld l, LOW($7000)
    /* 00:3FB0 */ ld [hl], $96
    /* 00:3FB2 */ inc l

.lop: ; 00:3FB3
    /* 00:3FB3 */ ld a, [de]
    /* 00:3FB4 */ ld [hli], a
    /* 00:3FB5 */ inc de
    /* 00:3FB6 */ dec c
    /* 00:3FB7 */ jr nz, .lop

    /* 00:3FB9 */ ld l, $0
    /* 00:3FBB */ ld a, [de]
    /* 00:3FBC */ ld [hl], a
    /* 00:3FBD */ ld l, $F
    /* 00:3FBF */ ld [hl], $96
    /* 00:3FC1 */ pop hl
    /* 00:3FC2 */ pop de
    /* 00:3FC3 */ pop bc
    /* 00:3FC4 */ pop af
    /* 00:3FC5 */ ret

    section "romx_01_4000", romx[$4000], bank[$01]

Data_01_4000::
    db $01
    db $02
    db $02
    db $2A
    db $02
    db $02
    db $03
    db $02 ; BANK(Code_02_758D) == BANK(Code_02_75C6)

Data_01_4008::
    dw $5871
    dw $4FAB
    dw $556F
    dw $4B39
    dw $55A5
    dw $5DCD
    dw $600F
    dw $758D

Data_01_4018::
    dw $5892
    dw $4FF3
    dw $5598
    dw $4BD4
    dw $55D9
    dw $5DFA
    dw $602C
    dw $75C6

Data_01_4028::
    dw $4C5D
    dw $4022
    dw $5242
    dw $40E2
    dw $4022
    dw $5610
    dw $5C82
    dw $5F2D

    section "romx_01_4058", romx[$4058], bank[$01]

Data_01_4058::
    ; this don't make sense, more than $100 entries
    ; those are banks btw
    db $09, $09, $09, $09, $09, $09, $09, $09
    db $09, $09, $0A, $0A, $0A, $0A, $0A, $0A
    db $0A, $0A, $0A, $0B, $0B, $0B, $0B, $0B
    db $0B, $0B, $0B, $0C, $0C, $0C, $0C, $0C
    db $0C, $0C, $0C, $0C, $0C, $0D, $0D, $0D
    db $0D, $0D, $0D, $0D, $0D, $1B, $0E, $0E
    db $0E, $0E, $0E, $0E, $0E, $0E, $0E, $0E
    db $0E, $0E, $0E, $0E, $0F, $0F, $0F, $0F
    db $0F, $0F, $0F, $0F, $0F, $0F, $10, $10
    db $10, $10, $10, $10, $10, $10, $10, $10
    db $10, $10, $11, $11, $11, $11, $11, $11
    db $11, $11, $11, $11, $11, $11, $11, $11
    db $11, $11, $12, $12, $12, $12, $12, $12
    db $12, $12, $12, $13, $14, $14, $15, $15
    db $15, $15, $15, $15, $15, $16, $16, $16
    db $16, $16, $16, $16, $16, $16, $16, $16
    db $17, $17, $17, $17, $17, $17, $17, $17
    db $17, $17, $17, $18, $18, $18, $18, $18
    db $18, $18, $18, $18, $18, $19, $19, $19
    db $19, $19, $19, $19, $19, $19, $1A, $1A
    db $1A, $1A, $1A, $1A, $1A, $1A, $1A, $1A
    db $1B, $1B, $1B, $1B, $1B, $1B, $1B, $1B
    db $1C, $1C, $1D, $1D, $1D

    section "romx_05_42E0", romx[$42E0], bank[$05]

Unk_05_42E0::
    ; width * y lut
    for W, $40
    for Y, $40
    dw W * Y
    endr
    endr
