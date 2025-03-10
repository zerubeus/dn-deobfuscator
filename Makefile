.PHONY: wavetone

wavetone:
	rm -rf data/wavetone.md
	poetry run python -m dn_deobfuscator.app --patches-dir data/dn2_wavetone_patches --output-md data/wavetone.md
	rm -rf extracted_dn2pst


