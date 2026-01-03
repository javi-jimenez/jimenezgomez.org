# Makefile additions for OG generation
.PHONY: gen-og

gen-og:
	python3 tools/generate-og-image.py $(POST)
