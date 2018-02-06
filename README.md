# perfevents-result-collector

Authors: Jan Smerda, Michael Petlan

This is a tool allowing to collect results from PERF and OProfile testing
on various systems. PERF and OProfile are measuring/profiling tools that
can count occurrences of various hardware events implemented in CPUs, such
as cache-misses, instructions, cycles, uncore events etc. As it is hard to
verify, whether the tools give correct values within the measurements, it
would be interesting to have a tool that collects the values centrally in
a database, allowing the user to compare them and do statistics upon it.

The database contains tables of events, microarchitectures, experiments
(since we need to store results of different measurements), the tools and
their versions. The basic function is to store records like:

  * tool = perf-3.10.0-327.13.1.el7
  * event = cpu-cycles
  * arch = x86_64
  * kernel version = 3.10.0-327.13.1.el7
  * microarchitecture = Intel Ivy Bridge
  * experiment = E (= perf stat against /bin/true)
  * value = 805623

We need to tie the events together, since the same events are represented
differently within different tools (the cpu-cycles in PERF is the same as
CPU_CLK_UNHALTED in OProfile). Similarly, it would be nice to have a list
of events supported on various microarchitectures, so we could query the
database to figure out whether an event should be available.

When having stored enough data, we will be able to:

  * figure out the distribution of the event occurrences per event
  * measure the "stability" (variability) of the values per experiment
  * mark suspicious values and detect bugs
  * compare the tools (OProfile/PERF) in a more reliable way

There is a vision of having also a coefficient of trust in every data row.
It could be assigned either by humans or by an AI and it could help with
further event verification.

The tool consists of a PostgreSQL database and a Python API/wrapper that
would take care of the queries and importing data in it. Thus a testcase
could report its results to the DB along with the environment data.

## Developer guide

Clone repository:
```bash
# example of working directory: /home/user/
git clone https://github.com/rfmvh/perfevents-result-collector/
cd perfevents-result-collector
```

Checkout `develop` branch for bleeding edge changes:
```bash
git checkout develop
```

Install dependencies:
```bash
# system wide RPM package
dnf install python-psycopg2

# OR

# via pip
pip install psycopg2

# OR

# using virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Setup your credentials for database:
```bash
cp defaults.conf ~/.config/perfevents-result-collector.conf
# edit ~/.config/perfevents-result-collector.conf accordingly
```

Update your `PYTHONPATH` environment variable. It's recommended to put this line into `~/.bashrc` (or `~/.zshrc` or any other file like that - depends on your shell) to have it persistent.
```bash
# within just cloned repo, so current working directory should contains
# directory 'perfresultcollector', 'README.md' and so on.
# example of working directory: /home/user/perfevents-result-collector
export PYTHONPATH=$PYTHONPATH:$PWD

# verify the PYTHONPATH (example)
echo $PYTHONPATH
:/home/user/perfevents-result-collector
```
