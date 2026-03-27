from setuptools import setup, find_namespace_packages


setup(
    name="puwhakahua_api_client",
    description="Python client for the Pūwhakahua API.",
    url="https://github.com/puwhakahua/puwhakahua-api-client",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
    ],
    license='GNU General Public License version 3.0 (GPLv3)',
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    install_requires=[
        "setuptools",
        "wheel",
        "requests",
        "pydub",
        "wai_logging",
    ],
    version="0.0.1",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    entry_points={
        "console_scripts": [
            "puwhakahua-client=puwhakahua.client:sys_main",
        ],
    },
)
