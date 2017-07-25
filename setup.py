from setuptools import setup

setup(name='qjira',
      version='0.99.1',
      description='Query JIRA Cloud REST API',
      author='Andrew Hamlin',
      author_email='andrew.hamlin@sailpoint.com',
      packages=['qjira'],
      entry_points={
          'console_scripts': [
              'qjira = qjira.__main__:main'
          ]
      },
      install_requires=[
          'requests',
          'python-dateutil',
          'keyring',
      ]
)
     
