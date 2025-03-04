# **Network Traffic Analysis and Application Classification**

## 📌 **Project Overview**
This project focuses on analyzing network traffic to identify application usage patterns, even when traffic is encrypted or anonymized.  
We extract key traffic features from PCAP files, visualize network behaviors, and build machine learning models to classify traffic flows by application type.

---

## 📂 **Project Structure**
The project is organized into the following directories:

```
Network-Traffic-Analysis-main/
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
│   │   ├── combined_dataset.csv  # Preprocessed dataset for direct ML training (not included in GitHub)
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

### 1️⃣ **Download Recordings**
The PCAPNG recordings are available at the following link:  
- [Download PCAPNG Recordings Link(compressed)]
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
### 🔑 **Adding Keys for Traffic Decryption in Wireshark**

To analyze encrypted traffic (e.g., HTTPS), you will need to configure Wireshark to use the appropriate TLS keys:

1. Open **Wireshark** and navigate to `Edit` > `Preferences`.
2. In the **Protocols** section, find  **TLS**.
3. Add the **path to the private key** 
   - The keys can be found in the `recordings/` directory, where the capture files are stored. For example:
     ```
     /path/to/Network-Traffic-Analysis-main/src/question_3/recordings/sslkeys_all.log
     ```
4. Save the settings and restart Wireshark to decrypt the traffic.


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
pip install pandas~=2.2.0 matplotlib~=3.10.0 seaborn~=0.13.2 scapy~=2.6.1 scikit-learn~=1.4.1.post1
```



