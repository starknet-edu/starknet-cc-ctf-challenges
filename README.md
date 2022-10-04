# StarkNet.CC CTF 2022

_NOTICE_ This is currently a scratchpad for challenges for the StarkNet.CC CTF

Please add you challenge idea in a new directory via a PR.

Challanges here are taken from the paradigm CTF, but can be a usefull example of what should be the deliverables for the challenges:

- Contracts in Cairo
- Deployment script using starknet.py

## Installing

### Prerequisites

- Docker
- Python 3

### Configuration

You'll need to set the following environment variables:

- `PYTHONPATH` to point to mpwn
- You can source the existing `envs.sh` file: `source envs.sh`

It's recommended that you run everything from a `venv`:

```bash
python3 -m venv venv
. ./venv/bin/activate
```

Install the requirements in the requirements file if you are running the first time.
Requirements match those in the development environment

```bash
pip install -r requirements.txt
```

You'll also need to install the following:

- `pip install pyyaml ecdsa pysha3 web3`

## Usage

### Build everything

```bash
./build.sh
```

### Run a challenge

Running a challenge will open a port which users will `nc` to. For Starknet related
challenges, an additional port must be supplied so that users can connect to the Starknet
node

```
./run.sh riddle-of-the-sphinx 31337 5050
```

On another terminal:

```
nc localhost 31337
```

When prompted for the ticket, use any value

```
$ nc localhost 31337
1 - launch new instance
2 - kill instance
3 - get flag
action? 1
ticket please: ticket

your private blockchain has been deployed
it will automatically terminate in 30 minutes
here's some useful information
```

### Running the autosolver

```bash
./solve.sh
```

## Create new Challenge

To create a new challenge, please create a new PR, following a similar structure to the existing examples.
The new directory should contain:

- A `public` dir
- A `private` dir
- A `info.yaml` file, with the authors name, and a short description of the challenge

### The public dir

The public dir should have the following structure:

- `./public/contracts`
- `./public/deploy`

The contracts dir should have all the contract needed to setup the sandbox environment on the deployed devnet.
The deploy dir should have a file called `chal.py`, in charge of setting up the contracts and checking results

The public dir should also have the `Dockerfile` that will later be used during the event, and for local testing.

#### The structure of chal.py

- The script should have a `deploy` function which deploys the contracts, and gives some information on the deployment process
- The script should have a `check` function running the final check on the state, to make sure the challenges was solved correctly

### The private dir

The private dir should have a solution to the challenge, that we can easily run and test that all challenges are working well. The solution file should be called `solve.py`

## Checking challenge packaging with docker

The best way to make sure the challenge and the solution works is to build a local docker image, and to test it with the existing infra. Here are the instructios on how to do this:

1. Copy the same stracture of the example challneges: `public`, `private`, `chal.py`, `Dockerfile`, etc. The infra expects the filenames in this format. The names `chal.py`, `solve.py` should be kept and only their content should be updated.
2. Update the `chal.py` script for the correct contract names in your `public/contracts`
3. Update the `solve.py` to call and execute the correct sequence of calls. No need to setup new accounts etc.

Next are instructions to create a local image and test it

1. Inside the `public` directory of the challenge, which contains the file `Dockerfile`, run a docker build command:

```
docker build -t  <CHALLANE_NAME> .
```

2. Update the `local-run.sh` file with the name of the challenge dir. (add it to the list of existing challenges)

3. Run the challenge with `./local-run.sh <CHALLENGE_NAME> 31337 5050`

4. Update the `solver.sh` file to include the challenge name, and comment out all other challenges

5. Run the solver file `./solver.sh`

The result of the run should be the template flag name

### Questions

- Following the structure of the examples should solve most of the issues.

- For any question, please feel free to reach out to me @amanusk on Tg or open an issue here
