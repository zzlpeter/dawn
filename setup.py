import os
from setuptools import setup, find_packages


install_requires = [line.rstrip() for line in open(os.path.join(os.path.dirname(__file__), "requirements.txt"))]


setup(
    name='dawn',
    version='0.1.0',
    author='zhangzhiliang',
    author_email='823515849@qq.com',
    description='',
    long_description='',
    url='https://github.com/zzlpeter/dawn',
    packages=find_packages(),
    ext_modules=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    install_requires=install_requires,
)
