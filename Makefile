VERSION=$(shell awk '/ oj_version / { print $$3 }' ojuba-release.spec)
RELEASE=$(shell awk '/ oj_release / { print $$3 }' ojuba-release.spec)
GITTAG=ojuba-release-$(VERSION)

all:

tag-archive:
	@git tag -a -m "Tag as $(GITTAG)" -f $(GITTAG)
	@echo "Tagged as $(GITTAG)"

create-archive:
	@rm $(GITTAG).tar.bz2
	@mkdir -p $(GITTAG)/ 
	@find . -maxdepth 1 -type f  | xargs cp -t $(GITTAG)/
	@tar cvzf $(GITTAG).tar.bz2 $(GITTAG)/
	@#echo git archive --prefix $(GITTAG)/ --format tar $(GITTAG) |bzip2 > $(GITTAG).tar.bz2
	@rm -rf $(GITTAG)/ 
	@echo ""
	@echo "The final archive is in $(GITTAG).tar.bz2"
	@chmod 644 $(GITTAG).tar.bz2

archive: tag-archive create-archive
