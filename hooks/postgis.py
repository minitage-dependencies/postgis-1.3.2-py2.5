import os
from minitage.core.common import substitute

def pre_make(options, buildout):
    """Custom pre-make hook for patching PostGIS."""
    # ``make install`` fails because it tries to write files under
    # /etc. This will write under the corresponding parts directory
    # instead.
    substitute(
        os.path.join(
            options['compile-directory'],
            'extras',
            'template_gis',
            'Makefile'
        ),
        '\$\(DESTDIR\)',
        '$(prefix)'
    )

    # Put in rpath info
    rpath = os.environ['LDFLAGS']
    substitute(
        os.path.join(
            options['compile-directory'],
            'Makefile.config'
        ),
        'DLFLAGS=-shared',
        'DLFLAGS=-shared %s' % rpath
    )

def pre_make_deb(options, buildout):
    """Custom pre-make hook for patching PostGIS."""
    # ``make install`` fails because it tries to write files under
    # /etc. This will write under the corresponding parts directory
    # instead.
    substitute(
        os.path.join(
            options['compile-directory'],
            'extras',
            'template_gis',
            'Makefile'
        ),
        '\$\(DESTDIR\)',
        '$(prefix)')
