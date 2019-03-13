import subprocess
from distutils.core import setup, Extension
from distutils.sysconfig import get_python_lib

site_packages = get_python_lib()

fn = 'zfft.c'
name = fn.split('.')[0]

libs = ['ndtypes','gumath', 'xnd','xndtools/kernel_generator','numpy/f2py/src','numpy/core/include']
lib_dirs = [f'{site_packages}/{lib}' for lib in libs]
system_libs = []

#This is only true if you make it 
if False:
       subprocess.call(['xnd_tools', 'config',fn]) 
       input("Press Enter to continue...")

       subprocess.call(['xnd_tools','kernel',f'{name}-kernels.cfg'])
       input("Press Enter to continue...")

       subprocess.call(['xnd_tools','module',f'{name}-kernels.cfg'])

       c_string = f'gcc -fPIC -c {name}.c {name}-kernels.c {name}-python.c \
       -I{site_packages}/ndtypes \
       -I{site_packages}/xnd \
       -I{site_packages}/gumath \
       -I{site_packages}/xndtools/kernel_generator \
       -I/Users/mpeaton/anaconda3/envs/scipy-dev/include/python3.7m/  \
       -I ../../build/src.macosx-10.7-x86_64-3.7/scipy/fftpack \
       -I /Users/mpeaton/anaconda3/envs/scipy-dev/lib/python3.7/site-packages/xndtools-0.2.0.dev3-py3.7-macosx-10.7-x86_64.egg/xndtools/kernel_generator/ \
       -I /Users/mpeaton/anaconda3/envs/numpy-dev/include/ \
       -I /Users/mpeaton/anaconda3/envs/xnd-env/lib/python3.6/site-packages/numpy/core/includegcc'

       input(f"Press Enter to compile...\n{c_string}")

       subprocess.call(c_string,shell=True)


       input("Press Enter to create archive...")
       subprocess.call(['ar','rcs',f'lib{name}-kernels.a',f'{name}-kernels.o',f'{name}.o'])

       input("Press Enter to install module...")

module1 = Extension(name,
                    include_dirs = lib_dirs,
                    libraries = ['zfft-kernels'] + system_libs + libs,
                    library_dirs = ['.'] + lib_dirs,
                    sources = ['zfft.c']
                    )

setup (name = 'zfft',
       version = '0.1',
       description = 'This is a gumath kernel extension that performs fftpack operations using XND containers',
       ext_modules = [module1]
       )