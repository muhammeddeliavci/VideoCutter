from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="video-cutter",
    version="1.0.0",
    author="",
    author_email="",
    description="Video dosyalarını belirli sürelerde parçalara bölen uygulama",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kullanıcıadı/VideoCutter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "video-cutter=video_cutter:main",
        ],
    },
) 