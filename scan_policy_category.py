import json
import os

if __name__ == "__main__":
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "policy_classification_data", "policy_std"))
    policy_set = set()
    for name in os.listdir(base_dir):
        if "input.json" not in name:
            continue
        input_file_path = f"{base_dir}/{name}"
        with open(input_file_path, "r", encoding="utf-8") as fd:
            print(input_file_path)
            for line in fd:
                line = line.strip()
                # print(line)
                rec = json.loads(line)
                if "policy_category" in rec:
                    policy_set.add(rec["policy_category"])

    for p in policy_set:
        print(p)
