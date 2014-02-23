manpages1 = bartleby.1
doc: ${manpages1}

bartleby.1:

%.1: %.1.txt
	@echo "Generating $@"
	a2x --doctype manpage --format manpage $<

.PHONY: clean
clean:
	rm ${manpages1}
