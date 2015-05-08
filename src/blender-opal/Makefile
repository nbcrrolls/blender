# $Id: Exp $
#
# @Copyright@
# @Copyright@
#

REDHAT.ROOT = $(PWD)/../../
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk
include $(NBCRDEVEL)/NBCR.mk

OPALDIR = /opt/opal/deployed
DEPLOYDIR = /opt/blender/bin

SCRIPTS = render.xml 

ADDSED = \
	-e s%@BLENDERVER@%$(BLENDERVER)%g 

$(VERSION.MK.INCLUDE): 
	if [ -f $(VERSION.MK.MASTER.DIR)/$(VERSION.MK.MASTER) ]; then \
	  /bin/cp $(VERSION.MK.MASTER.DIR)/$(VERSION.MK.MASTER) $@; \
	fi

pretar:: $(VERSION.MK.INCLUDE)

%: %.in
	$(SED) $(SEDSCRIPT) $(ADDSED) $^ > $@

build: $(SCRIPTS)

install:: 
	mkdir -p $(ROOT)/$(OPALDIR)
	$(INSTALL)  -m 0644  render.xml $(ROOT)/$(OPALDIR)/render_$(BLENDERVER).xml
	mkdir -p $(ROOT)/$(DEPLOYDIR)
	install -m 755 render.py  $(ROOT)/$(DEPLOYDIR)


clean::
	rm -rf $(SCRIPTS)
	rm -rf $(VERSION.MK.INCLUDE)
