import shutil
import re
import os
from minitage.core.common import substitute, append_env_var

def pre_configure(options, buildout):
    cwd=buildout['buildout']['parts-directory']
    flex=buildout['flex']['location']
    libiconv=buildout['libiconv']['location']
    #os.environ['PATH'] = cwd+"/flex/bin/:"+ os.environ.get('PATH','')
    #os.environ['LD_LIBRARY_PATH'] = cwd+"/flex/lib/:"+ cwd+"/libiconv/lib/:"+os.environ.get('LD_LIBRARY_PATH','')
    os.environ['CFLAGS']="  -I%s/include -I%s/include"%(libiconv,flex)
    os.environ['CPPFLAGS']="-I%s/include -I%s/include"%(libiconv,flex)
    os.environ['CXXFLAGS']="-I%s/include -I%s/include"%(libiconv,flex)
    os.environ['LDFLAGS']= "-L%s/lib -Wl,-rpath -Wl,%s/lib -L%s/lib -Wl,-rpath -Wl,%s/lib"    %(libiconv,flex,libiconv,flex)
    if os.uname()[0] == 'Darwin':
        os.environ['LDFLAGS']= ' -mmacosx-version-min=10.5.0 ' + os.environ['LDFLAGS']

def pre_make(options, buildout):
    """Custom pre-make hook for patching PostGIS."""
    # ``make install`` fails because it tries to write files under
    # /etc. This will write under the corresponding parts directory
    # instead.
    substitute('extras/template_gis/Makefile',
               '\$\(DESTDIR\)',
               '$(prefix)')

    # Put in rpath info
    rpath = os.environ['LDFLAGS']
    substitute('Makefile.config',
               'DLFLAGS=-shared',
               'DLFLAGS=-shared %s' % rpath)

def pre_make_deb(options, buildout):
    """Custom pre-make hook for patching PostGIS."""
    # ``make install`` fails because it tries to write files under
    # /etc. This will write under the corresponding parts directory
    # instead.
    substitute('extras/template_gis/Makefile',
               '\$\(DESTDIR\)',
               '$(prefix)')


os_ldflags=''
uname=os.uname()[0]
if uname == 'Darwin':
    os_ldflags=' -mmacosx-version-min=10.5.0'


def getpostgisenv(options,buildout):
    for var in ['flex','openssl','libiconv','postgresql','libiconv','zlib','fontconfig','python','geos','proj','swig',]:
        append_env_var('LDFLAGS', ["-L%(lib)s/lib -Wl,-rpath -Wl,%(lib)s/lib %(os)s"%{'lib':buildout[var]['location'],'os':os_ldflags}],sep=' ',before=False)
        append_env_var('LD_RUN_PATH', ["%(lib)s/lib"%{'lib':buildout[var]['location']}],sep=':',before=False)
        append_env_var('CFLAGS',   ["-I%s/include "%(buildout[var]['location'])],sep=' ',before=False)
        append_env_var('CPPFLAGS', ["-I%s/include "%(buildout[var]['location'])],sep=' ',before=False)
        append_env_var('CXXFLAGS', ["-I%s/include "%(buildout[var]['location'])],sep=' ',before=False)

# vim:set ts=4 sts=4 et  :
