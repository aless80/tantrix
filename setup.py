from distutils.core import setup

setup(name='tantrix',
		version='1.1',
		description='Tantrix, 2D game in Python for one or two players',
		author='Alessandro Marin',
		author_email='alessandro.marin80@gmail.com',
		url='https://github.com/aless80/tantrix',
		packages=['tantrix', 'server'],
		package_data={'': ['LICENSE', 'README.md'],'freegames': ['*.gif'],},
        classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment',
        'Topic :: Games/Entertainment :: Board Games',
        'Topic :: Games/Entertainment :: Turn Based Strategy',
        ),
    )