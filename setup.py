from distutils.core import setup

setup(name='datawandcli',
      version='0.1',
      description="Datawand Command Line Interface",
      url='',
      author='Ferenc Beres',
      author_email='fberes@info.ilab.sztaki.hu',
      packages=['datawandcli','datawandcli.cli','datawandcli.components'],
      install_requires=[
          'argparse',
          'jinja2',
          'luigi',
          'pytest',
          'codecov',
          'pytest-cov',
          'pandas',
          'psutil',
          'jupyter',
          'networkx',
          'matplotlib',
          'comet_ml'
      ],
      entry_points={
          'console_scripts': ['datawand = datawandcli.cli.main:execute']
      },
      zip_safe=False
)
