# Blockchain

Blockchain evolution simulation and visualization

## Introduction


#### Features



#### Technologies used



## Directory structure

#### Nodes (implemented in Python 3)

| Directory or file      | Contents
| -----------------------|:-----------------------------------------------------
| `.bc/`                 | Python virtual environment will be installed here
| `.conda/`              | Python (miniconda) will be installed here
| `.data/`               | ECDSA private keys will be saved here
| `.tmp/`                | Temporary files will be stored here
| `blockchain/`          | Python library package implementing blockchain-related functionality: blocks, transactions, Merkle tree etc.
| `blockchain_rpc/`      | Python library package implementing RPC-related functionality: initializing gRPC server and client, Node base class, peer sharing
| `dns_seeder/`          | Python executable package that implements DNS seeder node
| `full_node/`           | Python executable package that implements full node
| `protos/`              | Protobuf gRPC service definition (shared between Python and Node.js code)
| `scripts/`             | Helper bash scripts for nodes
| `tests_manual/`        | Integration tests for manual verification
| `tests_unit/`          | Automated unit tests
| `.env     `            | Configuration for the visualization app
| `.env.defaults`        | Configuration defaults for the visualization app

#### Visualization web app (implemented in Node.js)

| Directory or file      | Contents
|------------------------|------------------------------------------------------
| `viewer/`              | Visualization app
| `viewer/.tmp/`         | Temporary files will be stored here
| `viewer/app/`          | Express.js-based Node.js server application that serves Next.js client app as well as REST API
| `viewer/client/`       | Next.js-based client application
| `viewer/common/`       | Code shared between server and client
| `viewer/node/`         | Node.js will be installed here
| `viewer/node_modules/` | Node.js packages will be installed here
| `viewer/scripts/`      | Helper bash scripts for the viewer
| `viewer/.babel`        | Configuration for Babel JavaScript transpiler
| `viewer/.eslintrc`     | Configuration for ESLint static analyzer
| `viewer/.env     `     | Configuration for the visualization app
| `viewer/.env.defaults` | Configuration defaults for the visualization app
| `viewer/package.json`  | Package definition for the visualization app


## System tequirements

This software is cross-platform and will run anywhere where there is a Python 3.6
and Node.js 8 available. The code was developed and tested on Ubuntu 14.04 and 16.04.




## Installing and running

### 1. Nodes

Blockchain nodes are implemented in Python 3.
The source code is contained in the directories in of the project root 
(with the exception of directory `viewer/`),

#### Installing dependencies

Provided script will install a fresh version of python via conda 
(miniconda, actually), will create a local python virtual environment in 
directory `.bc` and will install python packages required for the project 
(see `requirements.txt`).

```
cd <PROJECT ROOT>

# Optionally, remove the previous artifacts
rm -rf .bc .data .conda .tmp

# Run the installer script
scripts/install
```

#### Configuring the environment

Nodes use the settings read from the file `.env` in the root directory.
The default configuration example is provided in `.env.defaults`

Copy the default configuration file:

```
cp .env.defaults .env
```

Modify the default settings in `.env` file if necessary.


Activate virtual environment "bc"

```
source .bc/bin/activate
```

#### Running unit tests

In order to run all unit tests, run:

```
./scripts/test
```

#### Running the DNS seeder node:

DNS seeder is a trusted node, which address is hardcoded by software maintainers
into all nodes. It provides initial node discovery in order to bootstrap the
peer-to-peer network.

```
./scripts/run dns_seeder
```


#### Running the full node:

Full node maintains the blockchain and mines new blocks

```
./scripts/run full_node <host>:<port>
```



## 2. Viewer

Blockchain visualization is implemented as a React/Node.js web application.
The source code for it is located in subdirectory `viewer/`

#### Installing dependencies

The installer script will install the LTS version of Node.js locally and will
install the required packages via NPM (see `package.json`)

```

cd <PROJECT ROOT>/viewer

# Optionally, remove the previous artifacts
rm -rf .build .tmp node_modules 

# Run the installer script
scripts/install
```

#### Configuring the environment

Nodes use the settings read from the file `.env` in the root directory.
The default configuration example is provided in `.env.defaults`

Copy the default configuration file:

```
cp .env.defaults .env
```

Modify the default settings in `.env` file if necessary.



#### Running the app in production (release) mode

Production build of the app (both client and server) can be triggered by the 
included script:

```
./scripts/build
```

The result will be generated in directory `.build/`.

After that, the production app can be started with:

```
./scripts/start
```

By default, the app will be served at `http://localhost:3000` (
this can be changed in `viewer/.env`)


#### Running the app in development (debug) mode

Development version of the app, with hot reloading and additinal debugging 
capabilities, can be started with:

```
./scripts/dev
```
