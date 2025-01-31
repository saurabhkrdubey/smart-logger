from setuptools import setup, find_packages

setup(
    name='smart-logger',
    version='0.1.0',
    packages=find_packages(),
    description='A smart logger that enhances Python logging.',
    author='Saurabh Dubey',
    author_email='saurabh.dubey@genzeon.com',
    url='https://github.com/saurabhkrdubey/smart-logger',  # Replace with your actual GitHub URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[  
        'psycopg2', "requests"
    ],
)