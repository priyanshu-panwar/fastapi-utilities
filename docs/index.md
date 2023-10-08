<p align="center">
    <em>🎨⚡️🔥 Reusable Utilities for FastAPI</em>
</p>
<p align="center">
<img src="https://img.shields.io/github/last-commit/priyanshu-panwar/fastapi-utilities.svg" />
<a href="https://github.com/priyanshu-panwar/fastapi-utilities/actions/workflows/build.yaml" > 
 <img src="https://github.com/priyanshu-panwar/fastapi-utilities/actions/workflows/build.yaml/badge.svg"/> 
 </a>
<a href="https://codecov.io/gh/priyanshu-panwar/fastapi-utilities" > 
 <img src="https://codecov.io/gh/priyanshu-panwar/fastapi-utilities/graph/badge.svg?token=8ACG93WM6I"/> 
 </a>
<br />
<a href="https://pypi.org/project/fastapi-utilities" target="_blank">
<img src="https://badge.fury.io/py/fastapi-utilities.svg" alt="Package version">
</a>
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/fastapi-utilities">
<img alt="PyPI - Python Version" src="https://img.shields.io/github/license/priyanshu-panwar/fastapi-utilities.svg">
<br />
<a href="https://pepy.tech/project/fastapi-utilities" > 
 <img src="https://static.pepy.tech/badge/fastapi-utilities"/> 
 </a>
<a href="https://pepy.tech/project/fastapi-utilities" > 
 <img src="https://static.pepy.tech/badge/fastapi-utilities/month"/> 
 </a>
<a href="https://pepy.tech/project/fastapi-utilities" > 
 <img src="https://static.pepy.tech/badge/fastapi-utilities/week"/> 
 </a>
</p>


---

**Source Code**: <a href="https://github.com/priyanshu-panwar/fastapi-utilities" target="_blank">https://github.com/priyanshu-panwar/fastapi-utilities</a>

*Inspired From*: <a href="https://github.com/dmontagu/fastapi-utils" target="_blank">dmontagu/fastapi-utils</a>

---

## Features

This package includes a number of utilities to help reduce boilerplate and reuse common functionality across projects:

* **Repeated Tasks**: Easily trigger periodic tasks on server startup using **repeat_every**.

```

from fastapi_utilities import repeat_every

@router.on_event('startup')
@repeat_every(seconds=3)
async def print_hello():

    print("hello")
```

* **Cron Jobs**: Easily trigger cron jobs on server startup using **repeat_at** by providing a cron expression.

```

from fastapi_utilities import repeat_at

@router.on_event("startup")
@repeat_at(cron="*/2 * * * *") #every 2nd minute
async def hey():
    print("hey")

```

* **Timer Middleware**: Add a middleware to the FastAPI app that logs the time taken to process a request. Optionally, also logs the average response time.The average response time is reset after every (reset_after)100,000 requests.


```

import asyncio
from fastapi import FastAPI, Request
from fastapi_utilities import add_timer_middleware

app = FastAPI()
add_timer_middleware(app, show_avg=True)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

```

Response Logs: 
```
INFO:     (fastapi-utilities) "GET - /" :: Time Taken :: 0.97 ms
INFO:     :: Average Response Time :: 0.97 ms
```


* **Cached Sessions**: Now use cached sessions along with context manager instead of `get_db`.

```
from fastapi import FastAPI
from .db import Base, engine
from fastapi_utilities import FastAPISessionMaker, repeat_every
from .models import User
import random

app = FastAPI()
Base.metadata.create_all(bind=engine)

session_maker = FastAPISessionMaker("sqlite:///db.sqlite3")


@app.on_event("startup")
@repeat_every(seconds=5, raise_exceptions=True)
async def startup():
    print("Starting up...")
    with session_maker.context_session() as session:
        x = User(id=random.randint(0, 10000))
        session.add(x)
    print("Startup complete!")

```


---

## Requirements

This package is intended for use with any recent version of FastAPI and Python 3.7+.

## Installation

```bash
pip install fastapi-utilities
```

## License

This project is licensed under the terms of the MIT license.
