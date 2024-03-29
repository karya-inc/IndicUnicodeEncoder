from setuptools import find_packages, setup


setup(
    name="indic_unicode_encoder",
    packages=find_packages(),
    version="0.1.0",
    description="Convert ascii encoded text in Indic languages to unicode",
    author="karya-inc",
    install_requires=["pandas"],
    package_data={"": ["**/*.json", "**/*.csv"]},
)
