import requests
import base64
import re
import os

# Sources for V2Ray configs (Public channels, other repos, etc.)
SOURCES = [
    "https://raw.githubusercontent.com/iboxz/free-v2ray-collector/main/main/mix.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/IranianCypherpunks/sub/main/sub",
    "https://raw.githubusercontent.com/vfarid/v2ray-share/main/all.txt"
]

PROTOCOLS = ["vmess", "vless", "ss", "trojan", "reality"]

def fetch_configs():
    all_configs = []
    for url in SOURCES:
        try:
            print(f"Fetching from {url}...")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                content = response.text
                # Check if content is base64 encoded
                try:
                    decoded = base64.b64decode(content).decode('utf-8')
                    all_configs.extend(decoded.splitlines())
                except:
                    all_configs.extend(content.splitlines())
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
    return list(set(all_configs)) # Remove duplicates

def categorize_configs(configs):
    categorized = {proto: [] for proto in PROTOCOLS}
    categorized["mix"] = []
    
    for config in configs:
        config = config.strip()
        if not config: continue
        
        categorized["mix"].append(config)
        
        for proto in PROTOCOLS:
            if config.startswith(f"{proto}://"):
                categorized[proto].append(config)
                break
    return categorized

def save_configs(categorized):
    os.makedirs("configs", exist_ok=True)
    for proto, items in categorized.items():
        file_path = f"configs/{proto}.txt"
        with open(file_path, "w") as f:
            f.write("\n".join(items))
        
        # Also save base64 version for subscription links
        with open(f"configs/{proto}_sub.txt", "w") as f:
            b64_content = base64.b64encode("\n".join(items).encode('utf-8')).decode('utf-8')
            f.write(b64_content)
    print("Configs saved successfully.")

if __name__ == "__main__":
    configs = fetch_configs()
    print(f"Total unique configs found: {len(configs)}")
    categorized = categorize_configs(configs)
    save_configs(categorized)
