# Rest capstone project
## Description
REST API for Animals Sales Web Project

## Install
```bash
git clone https://github.com/Dkozakk/Rest_capstone_project.git
```
### Make an virtual environment
```bash
python3 -m venv .venv
```
#### Windows
```bash
\.venv\Scripts\activate
```

#### MacOs or linux
```bash
source .venv/bin/activate
```
### Install requirements
```bash 
pip3 install -r requirements.txt
```
or

```bash
pyton3 -m pip3 install -r requirements.txt
```

### Run server

```bash
cd Rest_capstone_project
python3 app.py
```

### Config
In file config.ini you may change database_uri, port and debug_mode

### Quick start
First you need to register your center

```bash
curl -d '{"login": "testlogin", "password": "testpassword", "address": "test_address"}' -H "Content-Type: application/json" -X POST 'http://localhost:{port, default:5000}/register'
```

Next step is generating your token. You need this for making POST, PUT and DELETE requests. All GET requests
you are able to do without jwt token

```bash
curl -d '{"login": "testlogin", "password": "testpassword"}' -H "Content-Type: application/json" -X GET 'http://localhost:{port}/login'
```

You shoud save it

Before adding new animal you must create specie first

```bash
curl -d '{"name": "cat", "description": "simple cat"}' -H "Content-Type: application/json" -X POST http://localhost:{port}/species?token={token from previous step}
```

If you are seeing a success message, you are able to add your first animal

```bash
curl -d '{"name": "test_name", "description": "", "price": "10.24", "age": 5, "specie": "cat"}' -H "Content-Type: application/json" -X POST 'http://localhost:{port}/animals?token={token}'
```

Some other urls to get information about center/animal/specie

- GET:
    - urls to get all animals, species or centers:
        * /animals
        * /species
        * /centers
    - urls to get animal, specie or center by id:
        * /center/<id>
        * /animal/<id>
        * /specie/<id>
- PUT:
    - url to edit animal:
        * /animal/<id>
- DELETE:
    - url to delete animal:
        * /animal/<id>

### P.S.
if *python3* command doesn't work for you, try to use *py* or *python* instead
