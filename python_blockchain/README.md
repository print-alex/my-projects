**Activate the virtual enviroment**
```
/env/Scripts/Activate
```
**Install all packages**

```
pip3 install -r requirements.txt
```

**Run from module ,run as a script**

``
 py -m backend.blockchain.block
``

***Run tests**
Make sure to activate virtual environment
``
py -m pytest backend/tests
``

**Run the application and API**
Make sure to activate virtual environment

```
python3 -m backend.app

```

**Run a peer instance**
Make sure to activate virtual environment
```
set PEER=True && python -m backend.app
```