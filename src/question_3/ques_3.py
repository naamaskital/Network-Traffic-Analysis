import os
from scapy.all import rdpcap
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scapy.layers.inet import IP, TCP, UDP

base_dir = os.path.dirname(os.path.abspath(__file__))

# Directories
recordings_dir = os.path.join(base_dir, "recordings")
res_dir = os.path.join(base_dir, "..", "..", "res")
os.makedirs(res_dir, exist_ok=True)

if not os.path.exists(recordings_dir):
    print(f"Warning: The directory '{recordings_dir}' does not exist. Creating it now...")
    os.makedirs(recordings_dir)

# Find all PCAP/PCAPNG files in the recordings directory
pcap_files = {
    os.path.splitext(file)[0]: os.path.join(recordings_dir, file)
    for file in os.listdir(recordings_dir)
    if file.endswith(".pcap") or file.endswith(".pcapng")
}

if not pcap_files:
    print("No PCAP files found in the recordings directory. Exiting.")
    exit()


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
            if IP in pkt and (TCP in pkt or UDP in pkt):
                proto = "TCP" if TCP in pkt else "UDP"
                sport = pkt[TCP].sport if TCP in pkt else pkt[UDP].sport
                dport = pkt[TCP].dport if TCP in pkt else pkt[UDP].dport
                tcp_flags = pkt[TCP].flags if TCP in pkt else None

                data.append([
                    pkt.time,  # חותמת זמן
                    len(pkt),  # גודל חבילה
                    pkt[IP].src,  # כתובת מקור
                    pkt[IP].dst,  # כתובת יעד
                    sport,  # פורט מקור
                    dport,  # פורט יעד
                    proto,
                    tcp_flags,
                    app_name
                ])
            if len(data) >= limit:
                break
        except Exception as e:
            print(f"Error processing packet {i} in {app_name}: {e}")

    return data


# Process all files and collect data
traffic_data = []
for app, file in pcap_files.items():
    traffic_data.extend(extract_traffic_scapy(file, app))

# Create a DataFrame
# יצירת DataFrame כולל TCP_Flags
df = pd.DataFrame(traffic_data,
                  columns=["Timestamp", "Packet_Size", "Src_IP", "Dst_IP", "Src_Port", "Dst_Port", "Protocol", "TCP_Flags", "App"])

if df.empty:
    print("No valid packets were extracted. Exiting.")
    exit()

# 1. Bar plot - Comparing total traffic volume per application
plt.figure(figsize=(10, 6))
sns.barplot(x=df.groupby("App")["Packet_Size"].mean().index, y=df.groupby("App")["Packet_Size"].mean().values)
plt.xlabel("Application")
plt.ylabel("Average Packet Size (Bytes)")
plt.title("Average Packet Size by Application")
plt.savefig(os.path.join(res_dir, "avg_packet_size.png"))
plt.close()

# 2. Box plot - Comparing packet sizes per application
plt.figure(figsize=(10, 6))
sns.boxplot(x="App", y="Packet_Size", data=df)
plt.xlabel("Application")
plt.ylabel("Packet Size (Bytes)")
plt.title("Packet Size Distribution by Application")
plt.savefig(os.path.join(res_dir, "packet_size_distribution.png"))
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
plt.savefig(os.path.join(res_dir, "inter_arrival_times.png"))
plt.close()


# 5. Bar plot - Number of unique source IPs per application
plt.figure(figsize=(10, 6))
sns.barplot(x=df.groupby("App")["Src_IP"].nunique().index, y=df.groupby("App")["Src_IP"].nunique().values)
plt.xlabel("Application")
plt.ylabel("Number of Unique Source IPs")
plt.title("Number of Unique Source IPs by Application")
plt.savefig(os.path.join(res_dir, "unique_source_ips.png"))
plt.close()

# 6. Bar plot - TCP flag distribution per application
plt.figure(figsize=(12, 6))
df_tcp_flags = df.groupby("App")["TCP_Flags"].value_counts().unstack().fillna(0)
df_tcp_flags.plot(kind="bar", figsize=(12, 6))
plt.xlabel("Application")
plt.ylabel("Number of TCP Packets")
plt.title("TCP Flag Distribution per Application")
plt.legend(title="TCP Flags", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig(os.path.join(res_dir, "tcp_flag_distribution.png"))
plt.close()

# 7. Bar plot - Number of unique source ports per application
plt.figure(figsize=(10, 6))
sns.barplot(x=df.groupby("App")["Src_Port"].nunique().index, y=df.groupby("App")["Src_Port"].nunique().values)
plt.xlabel("Application")
plt.ylabel("Number of Unique Source Ports")
plt.title("Number of Unique Source Ports by Application")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig(os.path.join(res_dir, "unique_source_ports.png"), bbox_inches="tight")
plt.close()


# Save results to a CSV file
csv_path = os.path.join(res_dir, "traffic_analysis.csv")
df.to_csv(csv_path, index=False)
print(f"Analysis completed. Results saved to {csv_path}")
