abs = $(subst -,,$1)
eq = $(filter $1,$2)

maxN = $(words $(subst __,_,$(join $(call repeat,$1,_),$(call repeat,$2,_))))
minN = $(words $(subst __,_,$(filter __,$(join $(call repeat,$1,_),$(call repeat,$2,_)))))

max = $(strip $(if $(and $(call eq,$(call abs,$1),$1),$(call eq,$(call abs,$2),$2)),$(call maxN,$1,$2),\
      $(if $(and $(if $(call eq,$(call abs,$1),$1),,-),$(if $(call eq,$(call abs,$2),$2),,-)),-$(call minN,$(call abs,$1),$(call abs,$2)),\
      $(if $(call eq,$(call abs,$1),$1),$1,$2))))

gt = $(filter-out $2,$(call max,$1,$2))

repeat = $(if $(call eq,$(words $3),$1),$(strip $3),$(call repeat,$1,$2,$3 $2))

addN = $(words $(call repeat,$1,_) $(call repeat,$2,_))
subN = $(if $(call gt,$2,$1),-)$(words $(filter-out __,$(join $(call repeat,$1,_),$(call repeat,$2,_))))

add = $(strip $(if $(and $(call eq,$(call abs,$1),$1),$(call eq,$(call abs,$2),$2)),$(call addN,$1,$2),\
      $(if $(and $(if $(call eq,$(call abs,$1),$1),,-),$(if $(call eq,$(call abs,$2),$2),,-)),-$(call addN,$(call abs,$1),$(call abs,$2)),\
      $(if $(call eq,$(call abs,$1),$1),$(call subN,$1,$(call abs,$2)),$(call subN,$2,$(call abs,$1))))))

sub = $(strip $(if $(and $(call eq,$(call abs,$1),$1),$(call eq,$(call abs,$2),$2)),$(call subN,$1,$2),\
      $(if $(and $(if $(call eq,$(call abs,$1),$1),,-),$(if $(call eq,$(call abs,$2),$2),,-)),$(if $(call gt,$2,$1),-$(call subN,$(call abs,$1),$(call abs,$2)),$(call subN,$(call abs,$2),$(call abs,$1))),\
      $(if $(call eq,$(call abs,$1),$1),$(call addN,$1,$(call abs,$2)),-$(call addN,$2,$(call abs,$1))))))


left-slice = $(wordlist $(call add,1,$1),$(words $2),$2)
stripe = $(if $2,$(wordlist $1,$1,$2) $(call stripe,$1,$(call left-slice,$1,$2)))

fold = $(if $2,$(call fold,$1,$(call left-slice,1,$2),$(call $1,$3,$(firstword $2),$2)),$3)

range = $(if $(call eq,$(words $2),$1),$2,$(call range,$1,$2 $(words $2)))

differences = $(foreach i,$(call left-slice,1,$(call range,$(words $1))),\
	      $(call sub,$(wordlist $(call add,1,$i),$(call add,1,$i),$1),$(wordlist $i,$i,$1)))

all-zeroes = $(call fold,eq,$1,0)

sub-first-add-last = $(call sub,$(firstword $1),$(firstword $2)) $(call add,$(lastword $1),$(lastword $2))

extrapolate = $(if $(call all-zeroes,$1),0 0,$(call sub-first-add-last,$1,$(call extrapolate,$(call differences,$1))))


space = $(strip) $(strip)
FILENAME ?= /dev/stdin
lines = $(subst $(space),:,$(file < $(FILENAME)))

results := $(foreach line,$(lines),$(call extrapolate,$(subst :, ,$(line))))

part1 = $(call fold,add,$(call stripe,2,$(results)),0)
part2 = $(call fold,add,$(call stripe,2,$(firstword $(results)) $(results)),0)

.PHONY: all
all: ; $(info $(part1)) $(info $(part2))


#map = $(if $2,$(call map,$1,$(call left-slice,1,$2),$3,$4 $(call $1,$(firstword $2),$3,$4)),$4)
#min = $(strip $(if $(and $(call eq,$(call abs,$1),$1),$(call eq,$(call abs,$2),$2)),$(call minN,$1,$2),\
      $(if $(and $(if $(call eq,$(call abs,$1),$1),,-),$(if $(call eq,$(call abs,$2),$2),,-)),-$(call maxN,$(call abs,$1),$(call abs,$2)),\
      $(if $(call eq,$(call abs,$1),$1),$2,$1))))
#gte = $(call gt,$1,$2)$(call eq,$1,$2)
