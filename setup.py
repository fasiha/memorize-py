from setuptools import setup

setup(
    name='memorizesrs',
    version='1.0.0',
    description='The Memorize algorithm for scheduling flashcard review time',
    long_description=(
        'The algorithm by Tabibian et al. that balances the rate of reviews with probability of forgetting'
    ),
    keywords=('memorize quiz review schedule spaced repetition system srs'),
    url='https://github.com/fasiha/memorize-py',
    author='Ahmed Fasih',
    author_email='wuzzyview@gmail.com',
    license='Unlicense',
    py_modules=['memorizesrs'],
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires=[],
    zip_safe=True)
