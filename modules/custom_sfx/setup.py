from os import environ, remove
from platform import uname
from os.path import join, isfile, exists
from subprocess import check_output

import kivy

if environ.get('KIVENT_USE_SETUPTOOLS'):
    from setuptools import setup, Extension
    print('Using setuptools')
else:
    from distutils.core import setup
    from distutils.extension import Extension
    print('Using distutils')

try:
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext

    have_cython = True
except ImportError:
    have_cython = False
import sys

platform = sys.platform
cstdarg = '-std=gnu99'
libraries = ['GL']
extra_compile_args = []
extra_link_args = []
global_include_dirs = []
library_dirs = []

if environ.get('NDKPLATFORM') and environ.get('LIBLINK'):
    platform = 'android'
    libraries = ['GLESv2']
elif environ.get('KIVYIOSROOT'):
    platform = 'ios'
    libraries = ['GLESv2']
    sysroot = environ.get('IOSSDKROOT', environ.get('SDKROOT'))
    global_include_dirs = [sysroot]
    extra_compile_args = ['-isysroot', sysroot] #v da Q for GDB debugging
    extra_link_args = ['-isysroot', sysroot, '-framework', 'OpenGLES']
elif exists('/opt/vc/include/bcm_host.h'):
    platform = 'rpi'
    global_include_dirs = ['/opt/vc/include',
                           '/opt/vc/include/interface/vcos/pthreads',
                           '/opt/vc/include/interface/vmcs_host/linux']
    library_dirs = ['/opt/vc/lib']
    libraries = ['bcm_host', 'EGL', 'GLESv2']
elif exists('/usr/lib/arm-linux-gnueabihf/libMali.so'):
    platform = 'mali'
    global_include_dirs = ['/usr/include']
    library_dirs = ['/usr/lib/arm-linux-gnueabihf']
    libraries = ['GLESv2']
elif platform == 'win32':
    cstdarg = '-std=gnu99'
    libraries = ['opengl32', 'glu32', 'glew32']
elif platform.startswith('freebsd'):
    localbase = environ.get('LOCALBASE', '/usr/local')
    global_include_dirs = [join(localbase, 'include')]
    extra_link_args = ['-L', join(localbase, 'lib')]
elif platform.startswith('openbsd'):
    global_include_dirs = ['/usr/X11R6/include']
    extra_link_args = ['-L', '/usr/X11R6/lib']
elif platform == 'darwin':
    if sys.maxsize > 2 ** 32:
        osx_arch = 'x86_64'
    else:
        osx_arch = 'i386'
    v = uname()
    if v[2] >= '13.0.0':
        import platform as _platform

        xcode_dev = check_output(['xcode-select', '-p']).decode().strip()
        sdk_mac_ver = '.'.join(_platform.mac_ver()[0].split('.')[:2])
        sysroot = join(xcode_dev,
                       'Platforms/MacOSX.platform/Developer/SDKs',
                       'MacOSX{}.sdk'.format(sdk_mac_ver),
                       'System/Library/Frameworks')
    else:
        sysroot = ('/System/Library/Frameworks/'
                   'ApplicationServices.framework/Frameworks')
    extra_compile_args = ['-F' + sysroot, '-arch', osx_arch]
    extra_link_args = ['-F' + sysroot, '-arch', osx_arch,
                       '-framework', 'OpenGL']
    libraries = []

do_clear_existing = True

nemo_sfx_modules = {
    'nemo_sfx.sfx':['nemo_sfx/sfx.pyx'],
    'nemo_sfx.sfx_renderer': ['nemo_sfx/sfx_renderer.pyx'],
    'nemo_sfx.sfx_formats': ['nemo_sfx/sfx_formats.pyx',],
    
}

nemo_sfx_modules_c = {
    'nemo_sfx.sfx': ['nemo_sfx/sfx.c'],
    'nemo_sfx.sfx_renderer': ['nemo_sfx/sfx_renderer.c'],
    'nemo_sfx.sfx_formats': ['nemo_sfx/sfx_formats.c',],

}

check_for_removal = [
    'nemo_sfx/sfx_renderer.c',
    'nemo_sfx/sfx_formats.c',
    'nemo_sfx/sfx.c'
]


def build_ext(ext_name, files, include_dirs=[]):
    return Extension(ext_name, files, global_include_dirs + include_dirs,
                     extra_compile_args=[cstdarg, '-ffast-math', ] + extra_compile_args,
                     libraries=libraries, extra_link_args=extra_link_args,
                     library_dirs=library_dirs)


extensions = []
nemo_sfx_extensions = []
cmdclass = {}


def build_extensions_for_modules_cython(ext_list, modules):
    ext_a = ext_list.append
    for module_name in modules:
        ext = build_ext(module_name, modules[module_name],
                        include_dirs=kivy.get_includes())
        if environ.get('READTHEDOCS', None) == 'True':
            ext.pyrex_directives = {'embedsignature': True}
        ext_a(ext)
    return cythonize(ext_list)


def build_extensions_for_modules(ext_list, modules):
    ext_a = ext_list.append
    for module_name in modules:
        ext = build_ext(module_name, modules[module_name],
                        include_dirs=kivy.get_includes())
        if environ.get('READTHEDOCS', None) == 'True':
            ext.pyrex_directives = {'embedsignature': True}
        ext_a(ext)
    return ext_list


if have_cython:
    if do_clear_existing:
        for file_name in check_for_removal:
            if isfile(file_name):
                remove(file_name)
    nemo_sfx_extensions = build_extensions_for_modules_cython(
        nemo_sfx_extensions, nemo_sfx_modules)
else:
    nemo_sfx_extensions = build_extensions_for_modules(nemo_sfx_extensions,
                                                        nemo_sfx_modules_c)

setup(
    name='ElectricNemo sfx renderer',
    version='.3',
    description='''An extension for kivent for accessing shader variables
        https://github.com/Kovak/KivEnt for more info.''',
    author='Lawrence Du',
    author_email='larrydu88@gmail.com',
    ext_modules=nemo_sfx_extensions,
    cmdclass=cmdclass,
    packages=[
        'nemo_sfx',
    ],
    package_dir={'nemo_sfx': 'nemo_sfx'},
    package_data={'nemo_sfx': ['*.pxd', ]}
)
