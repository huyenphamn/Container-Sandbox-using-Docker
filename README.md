# Container-Sandbox-using-Docker
## Abstract
The goal of this project is to implement a security Sandbox using Docker containers to restrict the behaviour of given malicious code. My main focus for this project is on the Linux operating system. The Sandbox containers provide a controlled execution environment by adding a file system permission, restricting CPU and memory power for resource management, and restricting process spamming and exhausting resources.

## Features

- **Sandboxing:** Uses Docker to create a secure container that runs Bash scripts in isolation.
- **Security Restrictions:** Configurable seccomp profile to restrict system calls and prevent dangerous operations.
- **Resource Limiting:** Sets CPU, memory, and process limits to prevent resource exhaustion attacks.
- **Upload and Predefined Test Cases:** You can upload your own Bash scripts or select from predefined test scripts.
- **Timeout:** Each script is given a maximum execution time to avoid infinite loops and resource hogging.

## Technologies Used

- **Docker**: For containerization and sandboxing.
- **Flask**: For building the web interface and backend API.
- **HTML, CSS**: For the frontend user interface.
- **Seccomp**: For defining allowed and denied system calls in the container.
- **Bash**: For scripting and container execution.

## Security Considerations

- **Seccomp Profile:** Seccomp (Secure Computing Mode) is a Linux kernel feature that allows you to filter and restrict the system calls a process can make. In this project, we use a custom seccomp profile to limit the syscalls available to the container running the script, reducing the risk of malicious actions and ensuring that only safe operations can be performed. For example, system calls like file access outside specific directories are blocked, and potentially dangerous syscalls like `ptrace` are disabled.

- **Resource Limit:** Memory, CPU, and process limits are set to prevent DoS attacks and resource exhaustion.

- **Resource Limit:** Each script is limited to 15 seconds of execution time to avoid infinite loops or excessive computation.

## Why do we use a container?

Containers offer an easy way to isolate the processes, limiting their running environment, adding a new restriction layer, and within the tightly controlled sandboxed environment, sandbox containers will provide an ideal space to test for malicious code without causing harm to the machine. 

## Installation instruction

1. Clone the repository
2. Set up the environment
    - Make sure to have Docker installed and running in your machine. Visit the [Docker Starter Page](https://www.docker.com/get-started/) for installation intruction.
    - Make sure to have Python3 and pip installed. Please check out [Geeksforgeeks]{https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/} and [Python Packaging User Guide]{https://packaging.python.org/en/latest/tutorials/installing-packages/} for installation. 
    - Make sure to install [Flask]{https://flask.palletsprojects.com/en/stable/installation/}

## Usage

1. You can choose to upload your own test files, should be in .sh format
2. You can also choose to use one of the predefined test case
3. There should be a replica to show how the terminal would look like running in the sandbox container. 

