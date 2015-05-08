VERSION.MK.MASTER = version.mk
VERSION.MK.MASTER.DIR = ..
VERSION.MK.INCLUDE = blender.version.mk
include $(VERSION.MK.INCLUDE)

PKGROOT	    = /opt/blender
NAME        = blender
EXTENDED    = linux-glibc211
VERSION     = $(BLENDERVER)

SOURCE_PKG = $(NAME)-$(VERSION)-$(EXTENDED)-$(ARCH)

RELEASE 	= 0
TARBALL_POSTFIX	= tar.bz2

RPM.EXTRAS = AutoReq:No


