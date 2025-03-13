# Python Core - A simple base software without trying to overengineer or predict problems that aren't happening yet.

## Project structure
![image](https://github.com/user-attachments/assets/3bff301b-f65f-4a2b-89f5-8cebccec351e)

This is your main.py:

![image](https://github.com/user-attachments/assets/4cf6d473-60af-4d67-9ac9-e3c5a106c095)


## Benefits:
- Uses UV.
- Has a front-end using PyWebView.
- Uses Uvicorn in the backend.
- Communicate between front-end and back-end using websockets.
- Have a default logger that is accessible globally.
- Can save logs to the database.
- Have a default database (SQLite) that doesn't require any manual installation.
- Follow SOLID principles, like the Single-Responsibility Principle and the Open-Closed Principle. One example is that users never have to touch anything in the "Core" folder, they don't need to touch old code, they only extend it.

## Some known downsides for now are:
- I'm not typing every single thing that exists in the project. And the reason is simple: I think it makes the code extremely ugly, hard to read, and is useless in 90% of the cases that I've used it so far, especially since I'm not looking for super high performance, so I'm just typing whenever I feel like it's a good use.
- Doesn't have automatic tests yet.
- Logging, due to the fact of being handled mainly by a static class, may act weird when trying to run on multi-threaded code, which shouldn't be a huge issue since this project should run mainly asynchronous code and creating new threads manually should be limited to extremely rare cases of IO stuff.
- SQLite stores all its data in a file, so I'm not sure what are the limitations for now. I've used it in multiplayer games before and it handled it well, so I imagine as long as we keep an eye on how it's going, we can act if needed. And due to how the code was made, using a different database should be almost effortless.
- I haven't made some IP configuration configurable, so I'll still have to touch the backend folder once more, but it should be fairly simple.

## How to run

Install UV on your machine first: https://docs.astral.sh/uv/getting-started/installation/

Honestly, if you already have Python, the simplest way is just doing:
```bash
pip install uv
```

After that, you can run it with:
```bash
uv run main.py
```

And boom, there you are. No overcomplicating things.

