# Makefile additions for OG generation
.PHONY: gen-og

gen-og:
	python3 tools/generate-og-image.py $(POST)

.PHONY: gen-og-png
gen-og-png:
	./tools/generate-og-thumbnails.sh
