# StarkNet-CC CTF 2022 Challenges

The repository hosts challenges given at the StarkNet-CC CTF, held on Nov 1st 2022 in Lisbon.
The infra is based on the [Paradigm CTF]("https://github.com/paradigmxyz/paradigm-ctf-2022") infrastructure.
Each challenge is a separate directory containing the following

- Contracts in Cairo
- Deployment script using [starknet.py]("https://github.com/software-mansion/starknet.py")

## Versions

The challenges are targeting the following versions:

```
cairo-lang==0.10.0
starknet-devnet==0.3.3
starknet-py==0.5.2a0
```

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
./local-build.sh
```

### Run a challenge

Running a challenge will open a port which users will `nc` to.
Challenge name is the same as its directory.

```
./local-run.sh solve-me 31337 5050
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

All challenges come with a solution in the private directory (avoid if you do not want spoilers). To run the solution, start the challenge as explained above. _DO NOT_ run `nc`.
Comment out all but the challenge you want to solve in the `solve.sh` file.

Run:

```bash
./solve.sh
```

## Create new Challenge

To create a new challenge, please create a new PR, following a similar structure to the existing examples.
The new directory should contain:

- A `public` dir (this will be made public to the contesters)
- A `private` dir (this will remain private for testing and internal use)
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

The best way to make sure the challenge and the solution works is to build a local docker image, and to test it with the existing infra. Here are the instructions on how to do this:

1. Copy the same structure of the example challenges: `public`, `private`, `chal.py`, `Dockerfile`, etc. The infra expects the filenames in this format. The names `chal.py`, `solve.py` should be kept and only their content should be updated.
2. Update `Dockerfile` with the current contract names and the order in which they should be compiled (see examples)
3. Update the `chal.py` script for the correct contract names in your `public/contracts`
4. Update the `solve.py` to call and execute the correct sequence of calls. No need to setup new accounts etc.

Next are instructions to create a local image and test it

1. Inside the `public` directory of the challenge, which contains the file `Dockerfile`, run a docker build command:

```
docker build -t  <CHALLENGE_NAME> .
```

2. Update the `local-build.sh` file with the name of the challenge dir. (add it to the list of existing challenges)

3. Run the challenge with `./local-run.sh <CHALLENGE_NAME> 31337 5050`

4. Update the `solver.sh` file to include the challenge name, and comment out all other challenges

5. Run the solver file `./solver.sh`

The result of the run should be the template flag name

**NOTICE** first, check you can create a new instance by running the server with the <CHALLENGE*NAME> try to `nc` to it as described. To test the `solve.py` script, run the sever again \_without* running `nc`. Only run `solve.py` with on <CHALLENGE_NAME> uncommented.

## Running solutions manually

The dir `./manual-solutions` has the example for the solution as it should be written by the contesters.
You can write and run a similar solution as well.

1. Run the `run.sh` script as before
2. `nc` to the port and select create new instance (as before)
3. Update the `node_url`, `private_key`, `contract`, `player_address` variables after running `nc` and creating a new instance
4. Write the solution to the challenge
5. Run the script bring the state to the desired conditions
6. Run `nc` again and ask for the flag

### Questions

- Following the structure of the examples should solve most of the issues.

- For any question, please feel free to open an issue on this repo
