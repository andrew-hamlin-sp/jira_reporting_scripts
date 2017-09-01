from setuptools import setup, find_packages

setup(name='qjira',
      version='0.99.4',
      description='Query JIRA Cloud REST API',
      author='Andrew Hamlin',
      author_email='andrew.hamlin@sailpoint.com',
      packages=find_packages(exclude='tests'),
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      entry_points={
          'console_scripts': [
              'qjira = qjira.__main__:main'
          ]
      },
      test_suite='tests.suite',
      use_2to3=True,
      use_2to3_exclude_fixers=['lib2to3.fixes.fix_urllib'],
      install_requires=[
          'requests',
          'python-dateutil',
          'keyring',
          'six',
      ],
)
     
