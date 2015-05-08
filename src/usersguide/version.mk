
VERSION.MK.MASTER = version.mk
VERSION.MK.MASTER.DIR = ..
VERSION.MK.INCLUDE = blender.version.mk
include $(VERSION.MK.INCLUDE)

RPM.ARCH                = noarch

ROLL			= blender
NAME    		= roll-$(ROLL)-usersguide
RELEASE			= 0

SUMMARY_COMPATIBLE	= $(VERSION)
SUMMARY_MAINTAINER	= Rocks Group
SUMMARY_ARCHITECTURE	= x86_64

ROLL_REQUIRES		= base kernel os python
ROLL_CONFLICTS		=

PKGROOT 		= /var/www/html/roll-documentation/blender/$(VERSION)

