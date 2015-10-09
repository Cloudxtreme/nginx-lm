from setuptools import setup

setup(
    name="nginx-lm",
    packages=["app"],
    include_package_data=True,
    entry_points={
        "console_scripts": ["nlm = app:run"]
    },
    version="0.0.1",
    author="The Dark Lord Awal Garg aka Rash",
    author_email="awalgarg@gmail.com"
)
