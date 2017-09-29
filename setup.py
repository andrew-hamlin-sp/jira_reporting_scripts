from setuptools import setup, find_packages

setup(name='qjira',
      version='0.99.10',
      description='Query JIRA Cloud REST API',
      author='Andrew Hamlin',
      author_email='andrew.hamlin@sailpoint.com',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
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
      install_requires=[
          'requests',
          'python-dateutil',
          'keyring',
          'six',
      ],
      tests_require=['contextlib2;python_version<"3.4"']
)
     
