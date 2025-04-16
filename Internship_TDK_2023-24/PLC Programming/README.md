# 🌐 PLC Web Interface using Snap7 & Flask

This project is a lightweight web application that enables real-time monitoring of **Siemens S7-1500 PLC** data through a browser, accessible across a **local network**. It was developed as part of my internship experience to assist in seamless plant-level monitoring.

## 🛠️ Overview

- The **Snap7 Python library** is used to establish communication with the Siemens S7-1500 PLC and read specific memory addresses (inputs, outputs, data blocks, etc.).
- I built a **Flask-based web interface** to expose those readings in a user-friendly format accessible from any device on the same network (PC, mobile, tablet).

## ⚙️ Technologies Used

| Component         | Description                                  |
|------------------|----------------------------------------------|
| Siemens S7-1500   | PLC used for industrial control              |
| Snap7 (Python)    | Communication library to interact with PLC   |
| Flask             | Lightweight Python web framework             |
| HTML/CSS (Jinja2) | Frontend templating and styling              |

---

## 🧩 How It Works

1. **Snap7** connects to the PLC using its IP address and port.
2. Specific data blocks or addresses are read at regular intervals.
3. These values are passed to the Flask backend.
4. The web page is served over the local network with real-time values.

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.x
- Snap7: `pip install python-snap7`
- Flask: `pip install Flask`

### 📁 Project Structure

