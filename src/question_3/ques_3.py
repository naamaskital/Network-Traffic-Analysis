import os
from scapy.all import rdpcap
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scapy.layers.inet import IP, TCP

base_dir = os.path.dirname(os.path.abspath(__file__))

# נתיבים חדשים שמתאימים למבנה התיקיות שלך
recordings_dir = os.path.join(base_dir, "recordings")
res_dir = os.path.join(base_dir, "..","..", "res")

os.makedirs(res_dir, exist_ok=True)


# Dictionary of PCAP files for different applications
pcap_files = {
    "Chrome": os.path.join(recordings_dir, "chrome_capture.pcapng"),
    "Edge": os.path.join(recordings_dir, "edge_capture.pcapng"),
    "Spotify": os.path.join(recordings_dir, "spotify_capture.pcapng"),
    "YouTube": os.path.join(recordings_dir, "youtube_capture.pcapng"),
    "Zoom": os.path.join(recordings_dir, "zoom_capture.pcapng")
}


# Function to extract traffic features from a PCAP file
def extract_traffic_scapy(file_path, app_name, limit=1000000):
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} not found. Skipping {app_name}.")
        return []

    try:
        packets = rdpcap(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}. Skipping {app_name}.")
        return []

    data = []
    for i, pkt in enumerate(packets):
        try:
            if IP in pkt and TCP in pkt:
                data.append([
                    pkt.time,  # Timestamp
                    len(pkt),  # Packet size
                    pkt[IP].src,  # Source IP
                    pkt[IP].dst,  # Destination IP
                    pkt[TCP].sport,  # Source port
                    pkt[TCP].dport,  # Destination port
                    pkt[TCP].flags,  # TCP flags
                    app_name
                ])
            if len(data) >= limit:  # Limit the number of packets processed
                break
        except Exception as e:
            print(f"Error processing packet {i} in {app_name}: {e}")

    return data


# Process all files and collect data
traffic_data = []
for app, file in pcap_files.items():
    traffic_data.extend(extract_traffic_scapy(file, app))

# Create a DataFrame
df = pd.DataFrame(traffic_data,
                  columns=["Timestamp", "Packet_Size", "Src_IP", "Dst_IP", "Src_Port", "Dst_Port", "TCP_Flags", "App"])

if df.empty:
    print("No valid packets were extracted. Exiting.")
    exit()

# 1. Bar plot - Comparing total traffic volume per application
plt.figure(figsize=(10, 6))
sns.barplot(x=df.groupby("App")["Packet_Size"].mean().index, y=df.groupby("App")["Packet_Size"].mean().values)
plt.xlabel("Application")
plt.ylabel("Average Packet Size (Bytes)")
plt.title("Average Packet Size by Application")
plt.savefig(os.path.join(res_dir, "total_traffic_volume.png"))  # ✔ שמירת הגרף
plt.close()

# 2. Box plot - Comparing packet sizes per application
plt.figure(figsize=(10, 6))
sns.boxplot(x="App", y="Packet_Size", data=df)
plt.xlabel("Application")
plt.ylabel("Packet Size (Bytes)")
plt.title("Packet Size Distribution by Application")
plt.savefig(os.path.join(res_dir, "packet_size_distribution.png"))  # ✔ שמירת הגרף
plt.close()

# 3. Line plot - Comparing inter-arrival times of packets
plt.figure(figsize=(10, 6))
for app in df["App"].unique():
    subset = df[df["App"] == app].sort_values("Timestamp")
    inter_arrival_times = subset["Timestamp"].diff().dropna()
    plt.plot(inter_arrival_times, label=app)
plt.xlabel("Packet Index")
plt.ylabel("Inter-arrival Time (seconds)")
plt.title("Comparison of Inter-arrival Times by Application")
plt.legend()
plt.savefig(os.path.join(res_dir, "inter_arrival_times.png"))  # ✔ שמירת הגרף
plt.close()

# 4. Bar plot - Number of TLS packets per application
tls_ports = [443, 993, 465, 587, 8443]
df_tls = df[df["Dst_Port"].isin(tls_ports)]
if not df_tls.empty:
    tls_packet_counts = df_tls["App"].value_counts()
    plt.figure(figsize=(10, 6))
    plt.bar(tls_packet_counts.index, tls_packet_counts.values)
    plt.xlabel("Application")
    plt.ylabel("Number of TLS Packets")
    plt.title("Number of TLS Packets per Application")
    plt.xticks(rotation=45)  # סיבוב התוויות למניעת חפיפה
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    os.makedirs(res_dir, exist_ok=True)
    plt.savefig(os.path.join(res_dir, "tls_packets_per_app.png"), bbox_inches="tight")
    plt.close()
else:
    print("No TLS packets found in the dataset.")

# 5. Strip plot - Comparing the number of unique source ports per application
plt.figure(figsize=(10, 6))
sns.stripplot(x=df.groupby("App")["Src_Port"].nunique().index, y=df.groupby("App")["Src_Port"].nunique().values)
plt.xlabel("Application")
plt.ylabel("Number of Unique Source Ports")
plt.title("Number of Unique Source Ports by Application")
plt.savefig(os.path.join(res_dir, "unique_source_ports.png"))  # ✔ שמירת הגרף
plt.close()

# 6. Bar plot - TCP flag distribution per application
plt.figure(figsize=(12, 6))
df_tcp_flags = df.groupby("App")["TCP_Flags"].value_counts().unstack().fillna(0)
df_tcp_flags.plot(kind="bar", figsize=(12, 6))
plt.xlabel("Application")
plt.ylabel("Number of TCP Packets")
plt.title("TCP Flag Distribution per Application")
plt.legend(title="TCP Flags", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig(os.path.join(res_dir, "tcp_flag_distribution.png"))  # ✔ שמירת הגרף
plt.close()

# 7. Bar plot - Number of unique source IPs per application
plt.figure(figsize=(10, 6))
sns.barplot(x=df.groupby("App")["Src_IP"].nunique().index, y=df.groupby("App")["Src_IP"].nunique().values)
plt.xlabel("Application")
plt.ylabel("Number of Unique Source IPs")
plt.title("Number of Unique Source IPs by Application")
plt.savefig(os.path.join(res_dir, "unique_source_ips.png"))  # ✔ שמירת הגרף
plt.close()

# Save results to a CSV file
csv_path = os.path.join(res_dir, "traffic_analysis.csv")
df.to_csv(csv_path, index=False)
print(f"Analysis completed. Results saved to {csv_path}")
