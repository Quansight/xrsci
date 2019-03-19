import subprocess
from numpy.distutils.core import setup, Extension
from distutils.sysconfig import get_python_lib,get_python_inc
from os.path import join
from os import environ
from numpy.distutils.misc_util import Configuration
from glob import glob

prefix = environ.get('CONDA_PREFIX','/usr/local')
site_packages = get_python_lib()

srcdir = 'src'
fn = 'zfft.h'
name = fn.split('.')[0]

libs = ['fftpack','ndtypes','gumath', 'xnd','xndtools/kernel_generator','numpy/f2py/src','numpy/core/include']
lib_dirs = [f'{site_packages}/{lib}' for lib in libs]
system_libs = []

#This is only true if  
create_signature = input("Generate kernel config? y/[n]").lower()
if create_signature == 'y':
       subprocess.call(['xnd_tools', 'config',fn]) 

kernel_source = input("Generate kernel source? y/[n]")
if kernel_source == 'y':
       subprocess.call(['xnd_tools','kernel',f'{name}-kernels.cfg'])

create_module = input("Generate module y/[n]").lower()
if create_module == 'y':

       subprocess.call(['xnd_tools','module',f'{name}-kernels.cfg'])


build_archive = input("Compile kernels? y/[n]")
if build_archive == 'y':
       c_string = f'gcc -fPIC -c {name}.c {name}-kernels.c {name}-python.c \
       -I{site_packages}/ndtypes \
       -I{site_packages}/xnd \
       -I{site_packages}/gumath \
       -I{site_packages}/xndtools/kernel_generator \
       -I{get_python_inc()} \
       -I{prefix+"/include"}'
       
       print(c_string)
       subprocess.call(c_string,shell=True)
       
       subprocess.call(['gfortran','-c','-fPIC','-g',*glob(join('fftpack','*.f'))])
       subprocess.call(['ar','rcs',f'lib{name}-kernels.a',f'{name}-kernels.o',f'{name}.o',*glob(join('fftpack','*.o'))])
       subprocess.call(['mv',f'lib{name}-kernels.a',join(f'{prefix}','lib')])
# fftpack objects
# config = Configuration('fftpack','',None)

# fftpack_src = [join('src/fftpack','*.f')]
# config.add_library('fftpack', sources=fftpack_src)

# dfftpack_src = [join('src/dfftpack','*.f')]
# config.add_library('dfftpack', sources=dfftpack_src)

# config.add_extension('zfft',
#         sources='src/zfft.c',
#         libraries=['dfftpack', 'fftpack'],
#         include_dirs=['src'],
#         depends=(dfftpack_src + fftpack_src),
#         extra_f77_compile_args=['-fPIC'])


install_module=input("Install module y/[n]").lower()
if install_module=='y':
       module1 = Extension(name,
                     include_dirs = lib_dirs,
                     libraries = ['zfft-kernels'] + system_libs + libs,
                     library_dirs = ['.'] + lib_dirs,
                     sources = [f'{name}.c']
                     )

       setup (#name = 'zfft',
              version = '0.1',
              description = 'This is a gumath kernel extension that performs fftpack operations using XND containers',
              ext_modules = [module1],
       #       ÷ **config.todict()
              )




