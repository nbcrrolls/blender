# $Id$
#
# @Copyright@
# @Copyright@
#
# $Log$

REDHAT.ROOT = $(CURDIR)/../../

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

pretar:: $(VERSION.MK.INCLUDE)

$(VERSION.MK.INCLUDE): 
	if [ -f $(VERSION.MK.MASTER.DIR)/$(VERSION.MK.MASTER) ]; then \
		/bin/cp $(VERSION.MK.MASTER.DIR)/$(VERSION.MK.MASTER) $@; \
	fi

build:
	echo "Using $(SOURCE_PKG) distro"
	
install::
	mkdir -p $(ROOT)/$(PKGROOT)
	tar xjvf $(SOURCE_PKG).$(TARBALL_POSTFIX) -C $(ROOT)/$(PKGROOT) --strip-components=1 

clean::
	rm -rf $(SOURCE_PKG)
	rm -rf $(VERSION.MK.INCLUDE)
