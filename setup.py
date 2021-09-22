import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brain_atlas_toolkit",
    version="0.4.2",
    author="Austin Hoag",
    author_email="austinthomashoag@gmail.com",
    description="A set of tools for navigating, viewing and manipulating hierarchical brain atlases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/BrainCOGS/brain_atlas_toolkit",
    project_urls={
        "Bug Tracker": "https://github.com/BrainCOGS/brain_atlas_toolkit/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['graphviz'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)