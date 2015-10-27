VERSION.MK.MASTER = version.mk
VERSION.MK.MASTER.DIR = ..
VERSION.MK.INCLUDE = blender.version.mk
include $(VERSION.MK.INCLUDE)

PACKAGE     = blender
CATEGORY    = applications
NAME        = $(PACKAGE)-module
VERSION     = $(BLENDERVER)
RELEASE     = 0
PKGROOT     = /opt/modulefiles/$(CATEGORY)/$(PACKAGE)

BLENDERDIR   = /opt/blender

RPM.REQUIRES    = environment-modules
RPM.EXTRAS  = AutoReq:No
