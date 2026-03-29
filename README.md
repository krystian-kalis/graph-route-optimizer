# Shortest Path & Network Analysis GUI (Dijkstra's Algorithm)

## Overview
This repository contains a standalone desktop application developed in Python that performs communication network analysis. The core of the application models physical locations and routes as graph structures, utilizing **Dijkstra's Algorithm** to solve the shortest path problem. Originally designed with a "Museum Tour Routing" use case, the project demonstrates the practical application of graph theory packaged into a user-friendly Graphical User Interface (GUI).

## Key Features
* **Algorithmic Core:** Efficient implementation of Dijkstra's algorithm to calculate the optimal (shortest/fastest) path between multiple nodes in a communication network.
* **Graph Data Structures:** Mathematical modeling of locations as nodes and connections as weighted edges (representing distance or time).
* **Interactive GUI:** A fully functional Graphical User Interface that allows users to easily input parameters, select start/end points, and visualize the calculated routes without interacting with the raw code.
* **Standalone Executable (.exe):** The entire Python environment, dependencies, and application logic are compiled and packaged into a single `.exe` file. This allows non-technical users to run the application natively on Windows without needing to install Python.

## Repository Structure
* **`code.py`**: The main Python source code. It contains the graph structure definitions, the implementation of Dijkstra's algorithm, and the code for the graphical user interface.
* **`report.pdf`**: Detailed technical documentation and project report. It covers the mathematical foundations, time complexity analysis, and a showcase of the application's capabilities.
* **`app.exe`**: The compiled, standalone executable file that allows you to run the application directly. Due to its size, it is not hosted in the main file tree. You can download it by navigating to the Releases section on the right side of the GitHub repository page and downloading the latest version (v1.0).

## Authors
Krystian Kaliś, Maria Eberhardt
