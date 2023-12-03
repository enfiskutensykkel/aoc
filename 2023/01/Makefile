space = $(strip) $(strip)#
eq = $(filter $1,$2)
map = $(if $2,$(call map,$1,$(call slice,$2),$3,$4 $(call $1,$(firstword $2),$3,$4)),$4)
slice = $(wordlist 2,$(words $1),$1)
fold = $(if $2,$(call fold,$1,$(call slice,$2),$(call $1,$3,$(firstword $2),$2)),$3)

is_digit = $(call fold,eq,$1,0 1 2 3 4 5 6 7 8 9)
first_and_last = $(firstword $1) $(lastword $1)
repeat = $(if $(call eq,$(words $4),$1),$3,$(call repeat,$1,$2,$3 $2,$(words $4) $4))
split = $(if $1,$(subst $(firstword $1),$(firstword $1) ,$(call split,$(call slice,$1),$2)),$2)
explode = $(call split,0 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z,$1)
implode = $(subst $(space),,$(strip $1))

calibvalue = $(call repeat,$(call implode,$(call first_and_last,$(call map,is_digit,$(call explode,$1)))),_)

FILENAME ?= input.txt
LINES = $(file < $(FILENAME))
result = $(words $(call map,calibvalue,$(LINES)))


.PHONY: all
all: ; $(info $(result))
