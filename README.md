# 🗃️ File System Simulator

This project is a file system simulator implemented in Python. It simulates core functionalities of an operating system's file management and disk scheduling, with a graphical interface for user interaction.

## 🚀 Features

- Create, delete, read, and write files
- Three storage allocation methods:
  - Contiguous
  - Linked
  - Indexed
- File listing with sorting options (by name or size)
- Disk scheduling algorithms:
  - FCFS (First-Come-First-Serve)
  - SSTF (Shortest Seek Time First)
  - SCAN
- Visualization of disk block usage
- JSON-based persistent storage

## 🧩 Components

- `filesystem.py` – Backend logic for file management, allocation strategies, and disk scheduling.
- `gui.py` – GUI interface (compiled `.pyc` in this repo).
- `storage.json` – Simulated disk storage saved in JSON format.
- `filesystem.cpython-311.pyc` – Compiled version of the backend module.
- `gui.cpython-311.pyc` – Compiled version of the GUI module.

## 📦 File Operations

- **Create file:** Allocate disk blocks using the selected method.
- **Delete file:** Free allocated blocks and remove metadata.
- **Read/Write file:** Manage file content via JSON.
- **List files:** Display stored files, optionally sorted by size or name.

## 📊 Disk Scheduling

You can simulate disk access scheduling via different algorithms:
- **FCFS:** Processes requests in order of arrival.
- **SSTF:** Picks the request with the shortest seek time.
- **SCAN:** Moves the disk arm in one direction, servicing all requests, then reverses.

## 🖥️ How to Run

1. Ensure Python 3.11 is installed.
2. Run the `gui.py` script (you may need to recompile or restore it from source).
3. Use the interface to manage files and observe block usage.


## 📜 License

This project is open-source and available under the MIT License.
