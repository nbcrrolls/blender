# $Id$
#
# @Copyright@
# @Copyright@
#
# $Log$

REDHAT.ROOT = $(CURDIR)/../../

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

SOURCE_PKG = $(NAME)-$(VERSION)-$(EXTENDED)-$(ARCH)

build:
	echo "Using $(SOURCE_PKG) distro"
	
install::
	mkdir -p $(ROOT)/$(PKGROOT)
	tar xjvf $(SOURCE_PKG).$(TARBALL_POSTFIX) -C $(ROOT)/$(PKGROOT) --strip-components=1 

clean::
	rm -rf $(SOURCE_PKG)
