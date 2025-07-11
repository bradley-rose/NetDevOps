# Bradley's Take on NetDevOps
Welcome to this repository. If you're here, I hope this will provide you with some amount of value. 

First, a couple of potentially relevant notes:

- There are likely existing API wrappers for the tools listed here. For example, for Netbox, `pynetbox` exists, and I have specifically chosen not to use it. There are likely other ones. I'm writing custom logic using the `requests` library so that if an API changes and the dependent library like `pynetbox` doesn't receive updates or PRs for a specific amount of time, that doesn't become an issue.
  - Noting the above, logic for new actions will have to be built out. The foundations are there (CRUDs), so you'll just have to build out the logic for the specific API endpoints as necessary.
- I am building out these frameworks within the specific stack of tools that I use in my homelab, and potentially in enterprise. Additional directories can be added with logic for additional applications.

I have toyed around with Netbox in a number of environments, but I have never been able to get it to a state of usability. I am now trying to explore what can be done with this repository. 

**Of note**: The common route here would be to use Ansible, but because I already am fluent enough with Python, Ansible feels too restrictive for my liking, so I preferred to write this code instead to be able to define the flexible logic required for various purposes. I can schedule the execution of code with Cron and/or webhooks just as easily as anything else, so here we are.

# Usage Instructions
Look at the [Examples](./Examples/) subdirectory for functioning examples.

1. Clone this repository to your local machine
2. Create a directory in the [Examples](./Examples/) subdirectory. Alternatively, use the examples that are already created.
3. Create a virtual environment in that directory. `mkdir venv && python3 -m venv venv`
4. Install the necessary requirements. Either manually do this with the `requirements.txt` file included in each application directory, or install the requirements from the `requirements.txt` file provided within the pre-generated example.
   1. [Netbox](./Netbox/requirements.txt)
   2. [OPNsense](./OPNsense/requirements.txt)
   3. [DNS Example](./Examples/Netbox-to-OPNsense-DNS/requirements.txt)
5. Write your Python code for your desired actions, or run the provided example file.

## Writing your own
```sh
git clone https://github.com/bradley-rose/NetDevOps.git
cd NetDevOps
mkdir Examples/customName
mkdir Examples/customName/venv
python3 -m venv Examples/customName/venv
source Examples/customName/venv/bin/activate
python -m pip install --upgrade pip wheel
python -m pip install -r appName/requirements.txt
```

## Using an existing example
```sh
git clone https://github.com/bradley-rose/NetDevOps.git
cd NetDevOps
cd Examples/dirName
mkdir venv
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip wheel
python -m pip install -r requirements.txt
python ./targetPythonFile.py
```