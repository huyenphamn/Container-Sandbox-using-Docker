# Container-Sandbox-using-Docker
## Abstract
The goal of this project is to implement a security Sandbox using Docker containers to restrict the behaviour of given malicious code. My main focus for this project is on the Linux operating system. The Sandbox containers provide a controlled execution environment by adding a file system permission, restricting CPU and memory power for resource management, and restricting process spamming and exhausting resources.

## Sandbox
A sandbox is a security mechanism that isolates running processes, usually to mitigate the damage caused by malware from spreading. Under highly controlled environments, sandboxing offers ease to kill malicious code. 
Essentially, sandboxing means running malicious code with limited privileges and restricted rules, mitigating the risk if the code behaves unexpectedly and potentially causes harm to the host machine. 

## Sandbox Container
Containers offer an easy way to isolate the processes, limiting their running environment, adding a new restriction layer, and within the tightly controlled sandboxed environment, sandbox containers will provide an ideal space to test for malicious code without causing harm to the machine. 

Even when sandboxed environments have some vulnerabilities, the containers will keep the process completely separate from the system’s processes and only cause harm within the container.

I use Docker for this project as it supports security solutions, namely seccomp. A virtual machine would also be a good solution to isolate the process and machines, but I believe that, with the scope of the simple implementation for this project can be used for faster performance. Docker also introduces the COW (copy-on-write) principle, which we touched on recently, which makes malicious code not able to interfere with other processes.

What the sandbox is doing is essentially limiting the syscalls that the process can access. For example, this will prevent the cases that involve computer worms, a malware that can clone itself without the user’s awareness. There is still open research on the accurate sandbox policy for a program. However, for this project, I have not considered complicated processes and only used the default “read”, “write”, “exit”, and “sigreturn”.

There are also cases when other syscalls are necessary, however, it should be noted that the default ones are not likely to cause harm to the machine. For example, clone() can potentially allow a fork bomb (see the section below for a detailed explanation), which might crash the system. 

## Seccomp
Seccomp (secured computing mode) is a kernel feature that control syscall a process can make. It is a core part of Linux security feature. Seccomp profiles can be pass in to a container and use to add a level of security to the container. 

As stated in the Kubernetes documentation, seccomp is used to sandbox the privileges of the process. It will allow me to restrict the syscalls of the process; the only syscalls that are allowed now are the seccomp default: read, write, sigreturn, and exit. 
My seccomp rules should be applicable to both 32-bit and 64-bit x86, and also a hybrid one.

This ensures that the malicious code cannot call any other syscall than the ones mentioned.
This is important because for some of the test cases (listed below), the process that is trying to invoke any other syscall will be terminated. 

### Seccomp - from kernel view
By using the seccomp profile, it is basically saying that for everytime the kernel invoke the syscalls, check the rules in the seccomp first. When Docker run with a seccomp profile, it will make a syscall seccomp() to the kernel, telling it to apply these new policies for future syscalls. This will create something similar to a filter, and the kernel will attach that filter to the process, every syscall makes by the process have to go through that filter first. 

For example, a process that has fork(), Docker makes a seccomp() syscall, creating a syscall filter for that process. When the process call fork(), the kernel see that this process has a filter on, and proceed to check the rules of the filter. In this case, since only “read”, “write”, “exit”, “sigreturn” is allowed, fork() violates the rule of seccomp. The syscall then blocked, and the process will be terminated. 

"mmap()", is needed for memory allocation. mmap() can be abused when attackers can map the read-only region of memory to the writable one and use it to execute malicious code. However, "mmap()" itself should not cause a huge security problem, as they would need "mprotect()" to make the code executable. Similar case with "execve", "brk", "fstat".

Right now, open is only allowed if the process is running inside the container, and is not allowed for critical directiories (/home, /etc, /tmp). The /etc directory contains essential system configuration files for the operating system and software applications. The /home directory stores user-specific data, including personal files, application data, and configurations.  The /tmp directory is used for storing temporary files created by applications and the system, which might contain sensitive data, such as passwords, API keys, or session information.

## Sandboxing Method
I created a sandbox container to limit the resources so the CPU will not be exhausted. The Docker container will be created for the process, and automatically terminate itself after the process finishes. 

Within the container, the file permissions will be set to read-only to make sure malware is not able to overwrite other existing files. I set the control group's limit for both the CPU and the memory to isolate the resource usage, stopping the process from exhausting the machine. The pid limit is set to 100 to prevent cases like the fork bomb in the test below. I also set a timer for processes that were taking too much time, like the infinite loop test case; the process should be killed after 15 seconds, avoiding using the CPU power unnecessarily. 

The test and it's performance before timeout is documented in the timeout_log.txt

## Tests

### Fork bomb
Forkbomb is a Denial of Service attack where the process keeps forking itself indefinitely, which will eventually crash the system, and by setting the upper bound for the pid, the process will not be able to fork itself too many times. Since it only using CPU power inside Docker, it does not affect the normal activities. 

### Infinite Loop
A simple infinite loop that should burn the CPU and stop the other processes, but with the use of a sandbox container, the normal activities from my machine remain the same, while it is burning the one in Docker. We can also see that the CPU usage is limited to below 50%.

### File spam
This process is attempting to create 10000 spam files, which should not work as the container should be setting the files to be read-only to prevent overwrite, and limit the memory usage, which 10000 might be out of bounds. As always, everything will happen in the container and will not  be affecting the machine itself. 

### Memory exhaustion
This test is mainly to see if the control group of resources is working properly by starting the memory thread and allocating 512 MB to every thread, which would exceed the limit of 265 MB. It will immediately “sigkill” the process since the memory usage exceeds. 
