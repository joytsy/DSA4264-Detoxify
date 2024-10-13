from setuptools import setup, find_packages

setup(
    name="hate_toxicity_detector",
    version="1.0",
    packages=find_packages(),
    install_requires=["scikit-learn>=0.24", "numpy>=1.19"],
    entry_points={"console_scripts": ["detect=detector:Detector"]},
)
