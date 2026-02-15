# hwmon

A lightweight terminal-based hardware monitor and fan control utility for Linux.


**Note:**  
This project currently works only on linux laptops.  

---

## Screenshot

![hwmon screenshot](screenshot/2.png)

---

## Features

- CPU and Memory usage monitor
- fan rpm monitor
- temp monitor for other like nvme 
- voltage and power used and remaining battery life
- can write custom fan-temp curves 
- TUI made with Textual

---

## Requirements

- Linux
- Python 3.10+
- Root access (required for fan control)
- `hwmon` support in the kernel

---

## Installation

```bash
git clone https://github.com/shalonjovan/hwmon.git
cd hwmon
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x run.sh
