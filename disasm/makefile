RGBDS ?=

RGBASM ?= $(RGBDS)rgbasm
RGBFIX ?= $(RGBDS)rgbfix
RGBGFX ?= $(RGBDS)rgbgfx
RGBLINK ?= $(RGBDS)rgblink

COMPARE := python tools/script/compare.py
INCLIST := tools/inclist/inclist

TARGET := gbfe2.gbc

SOURCES := \
  main.asm

OBJECTS := $(SOURCES:.asm=.obj)

compare: $(TARGET)
	$(COMPARE) $(TARGET:.gbc=.map) baserom.gbc $(TARGET)

.PHONY: compare

RGBLINKFLAGS := -w
RGBFIXFLAGS := -v

$(TARGET): $(OBJECTS)
	$(RGBLINK) $(RGBLINKFLAGS) -n $(TARGET:.gbc=.sym) -m $(TARGET:.gbc=.map) -o $(TARGET) $(OBJECTS)
	$(RGBFIX) $(RGBFIXFLAGS) $(TARGET)

RGBASMFLAGS := -Weverything -E -L -h

define AsmRule
$1: $2 $$(shell $$(INCLIST) $2)
	$$(RGBASM) $$(RGBASMFLAGS) -o $$@ $$<
endef

$(foreach source, $(SOURCES), $(eval $(call AsmRule,$(source:.asm=.obj),$(source))))

%.2bpp: %.png
	$(RGBGFX) -o $@ $<
