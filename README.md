<p align="center">
    <em>🎨⚡️🔥 Reusable Utilities for FastAPI</em>
</p>
<p align="center">
<a href="https://github.com/priyanshu-panwar/fastapi-utilities/actions/workflows/build.yaml" > 
 <img src="https://github.com/priyanshu-panwar/fastapi-utilities/actions/workflows/build.yaml/badge.svg"/> 
 </a>
<a href="https://codecov.io/gh/priyanshu-panwar/fastapi-utilities" > 
 <img src="https://codecov.io/gh/priyanshu-panwar/fastapi-utilities/graph/badge.svg?token=8ACG93WM6I"/> 
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

---

## Requirements

This package is intended for use with any recent version of FastAPI and Python 3.7+.

## Installation

```bash
pip install fastapi-utilities
```

## License

This project is licensed under the terms of the MIT license.
