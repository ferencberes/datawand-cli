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
          'nbconvert',
          'pytest',
          'pandas',
          'psutil'
      ],
      entry_points={
          'console_scripts': ['datawand = datawandcli.cli.main:execute']
      },
      zip_safe=False
)
