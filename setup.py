import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name = "preprocess_texts",
    version = "0.0.2",
    author = "Binita Nath",
    author_email="binitanath10@gmail.com",
    description = "Text Preprocessing",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages=setuptools.find_packages(),
    classifiers =[
        'Programming Language :: Python :: 3 ',
        'License :: OSI Approved :: MIT License',
        'Operating System:: OS Independent'
    ],
    python_requires = '>= 3'
)   
