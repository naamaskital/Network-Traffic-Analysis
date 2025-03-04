# **Network Traffic Analysis and Application Classification**

## 📌 **Project Overview**
This project focuses on analyzing network traffic to identify application usage patterns, even when traffic is encrypted or anonymized.  
We extract key traffic features from PCAP files, visualize network behaviors, and build machine learning models to classify traffic flows by application type.

---

## 📂 **Project Structure**
The project is organized into the following directories:

```
project/
│── README.md               # This documentation file
│── final_report.pdf        # The final project report
│
├── src/                    # Source code for processing traffic data
│   ├── question_3/         # Scripts for analyzing application-level traffic patterns
│   │   ├── ques_3.py       # Main script for processing PCAPs and generating visualizations
│   │   ├── recordings/     # Directory for storing PCAP recordings (not included in GitHub)
│   │
│   ├── question_4/         # Scripts for machine learning classification of network traffic
│   │   ├── ques_4.py       # Main script for training and evaluating ML models
│   │   ├── combined_dataset.csv  # Preprocessed dataset for direct ML training
│
├── res/                    # Directory for storing results (graphs, processed CSV files)
│   ├── inter_arrival_times.png
│   ├── packet_size_distribution.png
│   ├── tcp_flag_distribution.png
│   ├── tls_packets_per_app.png
│   ├── traffic_analysis.csv
│   ||| and more png
```

---

## 📥 **Downloading the Required Files**
Before running the scripts, you need to download the following files:

### 1️⃣ **Download PCAP Recordings**
The PCAP recordings are available at the following link:  
- [Download PCAP Recordings Link(compressed)]
- https://drive.usercontent.google.com/download?id=14X829KINkmqASNlD0QL5SC-1FJPSJMLY&export=download&authuser=0

After downloading,extract the ZIP, place the files directly inside the `recordings/` directory (not in a subfolder).
The directory structure should look like this:
```
src/                   
│   ├── question_3/
│   │   ├── ques_3.py      
│   │   ├── recordings/     
```

If the `recordings/` directory doesn't exist, create it.

### 2️⃣ **Download the Prepared Dataset**
The dataset is available at the following link:  
- [Download Dataset (compressed)]
- https://drive.google.com/file/d/1vIyOnlJZkmR7iuWMG6v-1ei2M9xNkl-p/view?usp=drive_link

After downloading, extract the ZIP file into the following directory(name it combined_dataset):
```
├── question_4/         # Scripts for machine learning classification of network traffic
│   │   ├── ques_4.py       # Main script for training and evaluating ML models
│   │   ├── combined_dataset.csv  # Preprocessed dataset for direct ML training
```
---

### 🔧 **Additional Steps After Downloading:**
1. **PCAP Recordings**: Ensure that the files are placed directly inside the `recordings/` directory (not in any subfolders).
2. **Dataset**: Extract the ZIP file into the `src/question_4/` directory.

---
---

## 🔧 **Setup Instructions**
### **1️⃣ Prerequisites**
Ensure you have the following installed:

#### **For Windows:**
- Python 3.x (Install from [python.org](https://www.python.org/downloads/))
- Wireshark (Optional, for packet capture analysis)
- Npcap (Required for Scapy to work with Windows - download from [Npcap](https://nmap.org/npcap/))

#### **For Linux (Ubuntu/Debian-based distributions):**
- Python 3.x (Install via package manager: `sudo apt update && sudo apt install python3 python3-pip -y`)
- `tcpdump` (For live packet capturing): `sudo apt install tcpdump`
- `tshark` (For analyzing PCAP files): `sudo apt install tshark`

---

### **2️⃣ Install Required Python Libraries**
Run the following command to install necessary dependencies:
```bash
pip install -r requirements.txt
```
If `requirements.txt` is not provided, manually install:
```bash
pip install scapy pandas matplotlib seaborn
```

On **Linux**, you may need to run:
```bash
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)
```
to allow `Scapy` to capture packets properly.

---

## ▶ **Running the Project**
### **📌 Running Question 3 (Traffic Analysis & Visualization)**

#### **1️⃣ Ensure PCAP files are available**
- If you don’t have the PCAP files, **download them from [Google Drive / Your Cloud Link Here]**
- Place them in the correct directory:
  ```
  project/src/question_3/recordings/ (Ensure this directory contains the PCAP files before running the script)
  ```

#### **2️⃣ Execute the script**

##### **On Windows:**
```powershell
cd project/src/question_3
python ques_3.py
```

##### **On Linux/Mac:**
```bash
cd project/src/question_3
python3 ques_3.py
```
📌 **Expected Output:**
- Generates traffic analysis graphs inside the `project/res/` directory.
- Saves a processed CSV file (`traffic_analysis.csv`) with extracted features.

---

### **📌 Running Question 4 (Machine Learning Model for Traffic Classification)**

⚠ The dataset is compressed due to file size constraints.  
📥 Before running `ques_4.py`, extract `combined_dataset.zip` in `src/question_4/`

**No need to process PCAP files!**  
💡 **To make testing easier, we provide the dataset directly.** Instead of converting PCAP files to CSV, simply run the model on the preprocessed dataset:  

##### **1️⃣ Run the classification model**
##### **On Windows:**
```powershell
cd project/src/question_4
python ques_4.py
```
##### **On Linux/Mac:**
```bash
cd project/src/question_4
python3 ques_4.py
```
📌 **Expected Output:**
- The script trains and evaluates a machine learning model for traffic classification.
- The results will be displayed in the terminal.

---

## ⚠ **Troubleshooting**
❌ **Issue:** `FileNotFoundError: No such file or directory: 'recordings/chrome_capture.pcapng'`  
✔ **Fix:** Download the required PCAP files and place them inside `project/src/question_3/recordings/`  

❌ **Issue:** `ModuleNotFoundError: No module named 'scapy'`  
✔ **Fix:** Run `pip install scapy` to install missing dependencies.  

❌ **Issue:** `Analysis completed, but no graphs are generated`  
✔ **Fix:** Ensure `res/` directory exists and check if PCAPs contain valid network traffic.  

---

## 📢 **Additional Notes**
- **Why aren’t PCAP files included?**  
  - Due to GitHub’s size limitations, large `.pcap` files are **not uploaded**. Users must manually download them.
- **Why does the code use relative paths?**  
  - To ensure compatibility across different environments, all file paths are relative.
- **Why are some preprocessing scripts missing?**  
  - The preprocessing steps were completed in advance, and the final dataset is provided for direct model training.
- **How can I contribute or modify the project?**  
  - Fork the repository, make changes, and submit a pull request!

📌 **If you encounter any issues, feel free to open a GitHub issue or contact us!** 🚀

