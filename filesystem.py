# filesystem.py
import json
import os

STORAGE_FILE = "storage.json"
DISK_SIZE = 100

class FileSystem:
    def __init__(self):
        self.load_storage()

    def load_storage(self):
        if os.path.exists(STORAGE_FILE):
            with open(STORAGE_FILE, "r") as f:
                self.storage = json.load(f)
                if "file_data" not in self.storage:
                    self.storage["file_data"] = {}
                if "files" not in self.storage:
                    self.storage["files"] = {}
                if "free_space" not in self.storage:
                    self.storage["free_space"] = list(range(DISK_SIZE))
        else:
            self.storage = {"files": {}, "free_space": list(range(DISK_SIZE)), "file_data": {}, "disk_queue": [], "scheduling_method": "FCFS"}
            self.save_storage()

    def save_storage(self):
        with open(STORAGE_FILE, "w") as f:
            json.dump(self.storage, f, indent=4)

    def create_file(self, filename, size, method):
        if filename in self.storage["files"]:
            return "Error: File already exists."
        if len(self.storage["free_space"]) < size:
            return "Error: Not enough space."

        allocated_blocks = self.storage["free_space"][:size]
        self.storage["files"][filename] = {"size": size, "method": method, "blocks": allocated_blocks}
        self.storage["file_data"][filename] = ""
        self.storage["free_space"] = self.storage["free_space"][size:]
        self.save_storage()
        return f"File '{filename}' created successfully."

    def delete_file(self, filename):
        if filename not in self.storage["files"]:
            return "Error: File not found."
        allocated_blocks = self.storage["files"][filename]["blocks"]
        self.storage["free_space"].extend(allocated_blocks)
        del self.storage["files"][filename]
        del self.storage["file_data"][filename]
        self.save_storage()
        return f"File '{filename}' deleted successfully."

    def write_to_file(self, filename, content):
        if filename not in self.storage["files"]:
            return "Error: File not found."
        self.storage["file_data"][filename] = content
        self.save_storage()
        return f"Content written to '{filename}'."

    def read_file(self, filename):
        return self.storage["file_data"].get(filename, "Error: File not found.")

    def list_files(self, sort_by="name"):
        files = list(self.storage["files"].keys())
        if sort_by == "name":
            return sorted(files)
        elif sort_by == "size":
            return sorted(files, key=lambda x: self.storage["files"][x]["size"])
        return files

    def set_scheduling_method(self, method):
        self.storage["scheduling_method"] = method
        self.save_storage()

    def get_free_space_visual(self):
        return ["#" if i not in self.storage["free_space"] else "." for i in range(DISK_SIZE)]

    def schedule_disk_requests(self):
        method = self.storage["scheduling_method"]
        if method == "FCFS":
            return self.fcfs_schedule()
        elif method == "SSTF":
            return self.sstf_schedule()
        elif method == "SCAN":
            return self.scan_schedule()
        return []

    def fcfs_schedule(self):
        return sorted(self.storage["disk_queue"])

    def sstf_schedule(self):
        queue = self.storage["disk_queue"]
        head = 0
        queue.sort(key=lambda x: abs(x - head))
        return queue

    def scan_schedule(self):
        queue = sorted(self.storage["disk_queue"])
        head = 0
        left = [x for x in queue if x < head]
        right = [x for x in queue if x >= head]
        return left[::-1] + right
