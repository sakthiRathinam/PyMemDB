## PyMemDB - A Simple In-Memory Key-Value Store

PyMemDB is a lightweight, in-memory key-value store written in Python. Designed as a simple implementation of a database, it stores data in memory and uses the **RESP protocol** (similar to Redis) for communication with clients.

### Key Features

- **12 Supported Commands**: PyMemDB supports 12 essential commands, including common operations like `GET`, `SET`, `INCR`, and list operations such as `LPUSH` and `RPUSH`. These commands provide the functionality needed for basic key-value storage and list management.
  
- **I/O Multiplexing**: Leveraging asynchronous programming with `asyncio`, PyMemDB uses efficient I/O multiplexing, allowing it to handle multiple client connections concurrently, achieving improved performance on operations.

- **Append Only File (AOF) Persistence**: PyMemDB includes an optional AOF persistence mode. When enabled, it logs each write operation to a file in real-time, providing basic durability by allowing data to be restored if the server restarts. However, AOF must be explicitly enabled.

### Limitations

While PyMemDB provides in-memory data storage, it does **not offer full persistence**. Without AOF enabled, data exists only in memory and will be lost when the program terminates.

### Use Cases

PyMemDB can be useful for:
- Development and testing of key-value storage solutions
- Learning and experimentation with RESP-based communication and basic in-memory storage mechanics

For more details on starting the server, see the section on [Starting the PyMemDB Server](#starting-the-pymemdb-server).


## Installation

To install PyMemDB, you need to have Poetry installed on your system. Poetry is a dependency management and packaging tool for Python.

If you don't have Poetry installed, you can follow the installation instructions provided in the [Poetry documentation](https://python-poetry.org/docs/#installation).

Once you have Poetry installed, navigate to the directory where you have the `pyproject.toml` file for PyMemDB. Run the following commands to install the dependencies:

```shell
pip install poetry
poetry shell
```

This will create a virtual environment and install all the required dependencies for PyMemDB.

## Usage

PyMemDB provides several commands that you can use. Here are the available commands:

- `run-cli`: Run the PyMemDB command-line interface.
- `run-server`: Run the PyMemDB server.
- `run-async-server`: Run the PyMemDB asynchronous server.
- `run-server-with-debugger`: Run the PyMemDB server with a debugger attached.
- `run-async-server-with-debugger`: Run the PyMemDB asynchronous server with a debugger attached.
- `run-cli-with-debugger`: Run the PyMemDB command-line interface with a debugger attached.
- `run-test-services`: Run the test services using Docker Compose.
- `run-all-tests`: Run all the tests for PyMemDB.
- `pytest-debug`: Run the tests with debugging enabled.
- `run-server-with-profiler`: Run the PyMemDB asynchronous server with a profiler enabled.
- `run-lint`: Run the linter to check the code for style and syntax errors.
- `run-formatter`: Run the code formatter to format the code according to the project's style guide.

To execute these commands, use the following format: `poe run <command>`.

## Available Commands

1. **`ping`**  
   **Usage**: `ping`  
   Sends a ping to the server to check if it is responsive. The server responds with "PONG."

2. **`echo`**  
   **Usage**: `echo <message>`  
   Returns the provided message back to the client. Useful for debugging or testing connectivity.

3. **`get`**  
   **Usage**: `get <key>`  
   Retrieves the value associated with the specified key from the key-value store. Returns `nil` if the key does not exist.

4. **`set`**  
   **Usage**: `set <key> <value>`  
   Stores the specified value under the given key in the key-value store. If the key already exists, its value is updated.

5. **`exists`**  
   **Usage**: `exists <key>`  
   Checks if a specific key exists in the store. Returns `1` if the key exists and `0` otherwise.

6. **`del`**  
   **Usage**: `del <key>`  
   Deletes the key-value pair associated with the specified key from the store. Returns the number of keys removed.

7. **`incr`**  
   **Usage**: `incr <key>`  
   Increments the integer value of the specified key by 1. If the key does not exist, it is initialized to 0 before incrementing. Returns the new value.

8. **`decr`**  
   **Usage**: `decr <key>`  
   Decrements the integer value of the specified key by 1. If the key does not exist, it is initialized to 0 before decrementing. Returns the new value.

9. **`rpush`**  
   **Usage**: `rpush <key> <value>`  
   Pushes the specified value to the right end of a list associated with the given key. If the key does not exist, a new list is created.

10. **`lpush`**  
    **Usage**: `lpush <key> <value>`  
    Pushes the specified value to the left end of a list associated with the given key. If the key does not exist, a new list is created.

11. **`lrange`**  
    **Usage**: `lrange <key> <start> <stop>`  
    Retrieves a range of values from the list associated with the specified key, starting from `start` to `stop`. Returns an empty list if the key does not exist or is not a list.



## Starting the PyMemDB Server

To start the PyMemDB server, you can use the following command-line arguments to configure it based on your needs:

```bash
poe run-async-server [--port PORT] [--host HOST] [--appendonly BOOL] [--startexpiryloop BOOL] [--restoredb BOOL] [--aofpath PATH]
```



## Contributing

Contributions are welcome! If you have ideas for new features, optimizations, or improvements, feel free to submit a pull request or open an issue on GitHub.

## License

PyMemDB is open-source software licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Get Started

Explore the code and try out PyMemDB by visiting the [GitHub Repository](https://github.com/sakthiRathinam/PyMemDB).

---

Thank you for using PyMemDB! Your support and feedback are invaluable to making this project better. If you find it helpful or have suggestions, don’t hesitate to connect.

