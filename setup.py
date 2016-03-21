import os
from setuptools import setup, find_packages


def read_file(filename):
    basename = os.path.dirname(os.path.dirname(__file__))
    filepath = os.path.join(basename, filename)
    if os.path.exists(filepath):
        return open(filepath).read()
    else:
        return ''


setup(
  name='guestbook-pro',
  version='1.0.0',
  description='An enterprise guestbook web application.',
  long_description=read_file('README.md'),
  author='anl-mcampos',
  author_email='fedhelp@anl.gov',
  url='https://github.com/anl-mcampos/GuestBook.git',
  classifiers=[
      'Development Status :: 4 - beta',
      'Framework :: Flask',
      'License :: MIT',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2.6',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.2',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5'
  ],
  packages=find_packages(),
  include_package_data=True,
  keywords=['web', 'guestbook', 'anl'],
  license='MIT License',
  install_requires=[
    'Flask',
  ],
  entry_points={
      'console_scripts': [
          'guestbook = guestbook:main',
      ]
  }
)
