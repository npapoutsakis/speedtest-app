
# SpeedTest – Throughput Measurement with Unix Sockets

This project implements a custom SpeedTest application in C, using TCP Unix sockets to measure downlink throughput between a client and a server. The system also includes data visualization and analysis tools in Python for comparing measurements against both active (SpeedTest, iperf) and passive (Wi-Fi sniffer) throughput estimates.

---

### Table of Contents
- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Compilation](#compilation)
- [Running the Server](#running-the-server)
- [Running the Client](#running-the-client)
- [Visualizer & Data Analysis](#visualizer--data-analysis)
- [Evaluation Scenarios](#evaluation-scenarios)
- [File Descriptions](#file-descriptions)
- [References](#references)

---

### Project Overview

- **Goal:** Measure and analyze TCP downlink throughput between a client and server over Wi-Fi, in various scenarios, using your own SpeedTest implementation.
- **Architecture:** Client-Server written in C using Unix Sockets.
- **Features:**  
    - Aggregated and interval-based throughput measurement  
    - 2-second interval reporting for timeseries analysis  
    - Long-running server for repeated experiments  
    - Python visualizer for plotting and comparing results
---
### Compilation

Run the following command in the project root to build both server and client:

```sh
make
```

This will produce the `server` and `client` executables.

### Running the Server

Start the server:

```sh
./server
```

- The server **always runs**, serving one client at a time.
- It prints throughput (Mbps) every 2 seconds and the aggregate throughput after 30 seconds.

### Running the Client

On another terminal or host:

```sh
./client <server_ip>
```

- The client connects to the server and sends data for **30 seconds**.
- Throughput (Mbps) is printed every 2 seconds and at the end of the test.
---
### Visualizer & Data Analysis

The `visualizer.py` script generates plots and statistics from measurement CSVs.

- Requires: Python 3, `numpy`, `pandas`, `matplotlib`
- Usage example:

```sh
python3 visualizer.py
```

- The script will:
    - Plot throughput time series for each scenario
    - Compare SpeedTest with iperf
    - Analyze Wi-Fi Doctor/sniffer metrics


### Evaluation Scenarios

Scenarios are tested for:
- 2.4 GHz & 5 GHz Wi-Fi, both close and far from AP, and with movement.
- Data is collected for each scenario in dedicated CSV files.

### File Descriptions

- `server.c`: Implements the TCP server for SpeedTest. Prints interval and aggregate throughput.
- `client.c`: Implements the TCP client. Connects to the server, sends data for 30s, prints interval/aggregate throughput.
- `Makefile`: Automates compilation of client/server.
- `visualizer.py`: Plots throughput, compares with iperf/sniffer data, saves statistics.
- `metrics/`: Contains all result CSVs (SpeedTest, iperf, sniffer).
- `plots/`, `statistics/`: Output folders for generated visualizations/statistics.
---
### References

- [iperf tool](https://iperf.fr/)
- [Beej’s Guide to Network Programming](https://beej.us/guide/bgnet/pdf/bgnet_usl_c_1.pdf)
- [Wireless Throughput Calculations and Limitations](https://documentation.meraki.com/MR/Wi-Fi_Basics_and_Best_Practices/Wireless_Throughput_Calculations_and_Limitations)
- [TutorialsPoint: Unix Sockets Quick Guides](https://www.tutorialspoint.com/unix_sockets/socket_quick_guide.htm)