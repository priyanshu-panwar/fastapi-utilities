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

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Using with Latest FastAPI Version](#update-how-to-use-with-latest-fastapi-version)
- [New: TTL LRU Cache](#ttl-lru-cache)
- [New: FastAPI CLI Tool](#fastapi-cli-tool)
- [New: Rate Limiter](#rate-limiter)
- [Repeated Tasks](#repeated-tasks)
- [Cron Jobs](#cron-jobs)
- [Timer Middleware](#timer-middleware)
- [Cached Sessions](#cached-sessions)
- [License](#license)

---

## Features
- Repeat At / Every for scheduling cron jobs
- TTL LRU Cache
- Timing Middleware that logs the time taken by a request
- Session Middleware
- CLI tool to generate skeleton
- **🔥New: Rate Limiter** - Limit API requests per user/IP

---

## Rate Limiter

We have introduced a **Rate Limiter** that restricts the number of API requests within a defined time window per user/IP.

### How to use

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi_utilities import rate_limiter

app = FastAPI()

@app.get("/limited")
@rate_limiter(max_requests=2, time_window=5)
async def limited_endpoint(request: Request):
    return {"message": "Success"}
```

### Features
- **📅 Time-based limiting**: Restrict requests per second/minute/hour.
- **🔍 Per user/IP tracking**: Limits users individually.
- **🌐 Configurable limits**: Easily change request limits.
- **❌ Returns 429 Too Many Requests**: Blocks excessive requests.
- **Don't FORGET to pass request param in routes**

---

## [✨Update✨] How to use with Latest FastAPI version

With the latest FastAPI version, `on_event` lifespan functions are deprecated. Here is the official [doc](https://fastapi.tiangolo.com/advanced/events/#async-context-manager).
We need to make use of `asynccontextmanager` with the latest FastAPI.

Here is an example how to use lifespan (Repeated Tasks) functions with latest FastAPI:

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_utilities import repeat_every, repeat_at

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    await test()
    test2()
    yield
    # --- shutdown ---

app = FastAPI(lifespan=lifespan)

# Repeat Every Example
@repeat_every(seconds=2)
async def test():
    print("test")

# Repeat At Example
@repeat_at(cron="* * * * *")
def test2():
    print("test2")
```

Only difference is to call our tasks from lifespan function instead of using `on_event` function.

---

## TTL LRU CACHE

We have introduced `ttl_lru_cache` now in our library.

### How to use

```python
from fastapi_utilities import ttl_lru_cache

@ttl_lru_cache(ttl=2, max_size=128)
def sum(a: int, b: int) -> int:
    return a + b

sum(1, 3)
sum(1, 3)
```

---

## FastAPI CLI Tool

With our CLI Tool you can get a skeleton project built to get you started with the code.

### How to use

- Using `poetry`: `poetry run cli init`
- Using `pip`: `python3 -m cli init`

---

## Installation

```bash
pip install fastapi-utilities
```

## License

This project is licensed under the terms of the MIT license.
