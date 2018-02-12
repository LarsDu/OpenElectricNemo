#!/bin/bash

VERSION_nemo_sfx=0.1.0
URL_nemo_sfx=https://github.com/LarsDu/OpenElectricNemo/archive/master.zip
MD5_nemo_sfx=
DEPS_nemo_sfx=(python kivy)
BUILD_nemo_sfx=$BUILD_PATH/nemo_sfx/master/modules/particles
RECIPE_nemo_sfx=$RECIPES_PATH/nemo_sfx

function prebuild_nemo_sfx() {
	true
}

function build_nemo_sfx() {
	cd $BUILD_nemo_sfx

	push_arm

	export LDSHARED="$LIBLINK"
	export PYTHONPATH=$BUILD_kivy/:$PYTHONPATH
	export PYTHONPATH=$BUILD_kivent_core/:$PYTHONPATH
	try find . -iname '*.pyx' -exec $CYTHON {} \;
	try $BUILD_PATH/python-install/bin/python.host setup.py build_ext -v
	try find build/lib.* -name "*.o" -exec $STRIP {} \;

	export PYTHONPATH=$BUILD_PATH/python-install/lib/python2.7/site-packages:$PYTHONPATH
	try $BUILD_hostpython/hostpython setup.py install -O2 --root=$BUILD_PATH/python-install --install-lib=lib/python2.7/site-packages

	unset LDSHARED
	pop_arm
}

function postbuild_nemo_sfx() {
	true
}
