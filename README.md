# Fetch SRE Take-Home Assignment:

## Project Overview&#x20;

I developed this Python-based solution as a replacement for the provided Go code. The program reads a YAML configuration file that lists endpoints to monitor. For each endpoint, it performs periodic health checks and logs availability statistics based on the domain name. The checks validate both the HTTP status (must be 200–299) and the response time (must be under 500ms). These checks are executed repeatedly every 15 seconds in an infinite loop. The code structure was designed to be minimal, testable, and easy to maintain.

---

## Installation Guide

To ensure this project runs smoothly, you must install Python  on your system. Below are steps for both Windows and macOS.

### For Windows

1. Visit https://www.python.org/downloads/
2. Download the latest version for Windows
3. Run the installer
4. Check the box that says 'Add Python to PATH'
5. Complete the installation
6. Open Command Prompt and verify:

```bash
python --version
```

### For macOS

1. Install Homebrew if not already installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. Install Python using Homebrew:
```bash
brew install python3
```
3. Verify installation:
```bash
python3 --version
```


### 1. Clone the repository




```bash
git clone https://github.com/saitejaindukuri/FETCH_SRE_EXCERCISE.git
cd FETCH_SRE_EXCERCISE
```

### 2. Set up Python Environment

```bash
python -m venv fetch-env
source fetch-env/bin/activate
```

### 3. Install Required Packages

```bash
pip install pyyaml requests
```

### 4. Run the Program

```bash
python main.py sample.yaml
```

---



## Code Improvements and Implementation Details

1. **Rewriting in Python instead of Go**  
The original submission was in Go. I rewrote the entire logic in Python so I could better understand and control every aspect of the solution.

2. **Accurate handling of request bodies**  
In the Go code, the full endpoint object was incorrectly marshaled and passed as the request body. In Python, I send only the relevant body content using the `data` parameter in `requests.post()`.

3. **Header injection support**  
The Go implementation used `req.Header.Set()` but didn’t validate presence of headers. In Python, I safely pass headers if available using the `.get("headers")` method.

4. **Proper domain extraction with port handling**  
In Go, domain extraction was done using `strings.Split()` which could mistakenly include ports. I used Python's `urlparse(url).hostname` and added `.split(":")[0]` to fully eliminate ports from domain tracking.

5. **Tracking availability cumulatively**  
The Go code updated stats but didn’t report them. In Python, I created a stats dictionary (`stats[domain]["total"]` and `"success"`) to continuously record performance per domain across check cycles.

6. **Check cycle interval control**  
Although the Go code included a sleep, it lacked clear structure. I placed the entire loop inside a `while True` block with `time.sleep(15)` to ensure checks happen every 15 seconds consistently.

7. **Graceful error handling**  
Python exceptions are captured using try-except. This ensures that the application doesn't crash and continues monitoring other endpoints if one fails.

8. **Availability condition logic**  
Availability is checked using:
```python
is_available = (200 <= status < 300) and (duration_ms <= 500)
```
Only responses that return success status codes and respond within 500 milliseconds are considered available.


9.**Output** 

<img width="1078" alt="image" src="https://github.com/user-attachments/assets/9b04e2fe-bd17-4d94-97d2-ca1a60ce75b2" />


---





##  What I Ensured

- Tracks **availability by domain only**
- Ignores port numbers with proper parsing
- Cumulative tracking works and updates per cycle
- No name field or unnecessary complexity used
- Supports **GET and POST** only (prints warning if method unsupported)
- Follows all time/status-based availability checks.
