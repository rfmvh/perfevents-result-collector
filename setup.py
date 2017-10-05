from setuptools import setup

def get_version():
    with open('version') as fd:
        ver = fd.readline().strip()
    return ver


setup(
    name="perfevents-result-collector",
    packages=["perfresultcollector"],
    version=get_version(),
    licence='GPLv3',
    description="Collects benchmark data.",
    author="Jan Smerda, Michael Petlan",
    author_email="mpetlan@redhat.com",
    url="https://github.com/rfmvh/perfevents-result-collector",
    download_url="https://github.com/rfmvh/perfevents-result-collector",
    keywords=["data", "collect", "benchmark"],
    classifiers = [
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
        ],
    long_description = """
This is a tool allowing to collect results from PERF and OProfile testing
on various systems. PERF and OProfile are measuring/profiling tools that
can count occurrences of various hardware events implemented in CPUs, such
as cache-misses, instructions, cycles, uncore events etc. As it is hard to
verify, whether the tools give correct values within the measurements, it
would be interesting to have a tool that collects the values centrally in
a database, allowing the user to compare them and do statistics upon it.
"""
)
