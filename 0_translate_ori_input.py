import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

import llm.kimi_api


def _do_translation(input_path, output_path, kimi):
    trans_buf = {}
    with open(input_path, "r", encoding="utf-8") as fd:
        with open(output_path, "w", encoding="utf-8") as fw:
            for line in fd:
                rec = json.loads(line.strip())
                event = rec["event"]

                prompt = (f"Please translate \"{event}\" into no more than 100 English words. Do not search the web. "
                          f"Only respond with the translated text and nothing else.")
                if event not in trans_buf:
                    trans_txt = kimi.chat(prompt)
                    trans_buf[event] = trans_txt
                    print(f"               {event}: {trans_txt}")

                rec['event_en'] = trans_buf[event]

                fw.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _process_month_chunk(months, base_dir):
    kimi = llm.kimi_api.KimiClient()
    for month_str in months:
        output_path = os.path.join(base_dir, f"{month_str}_input_translated.json")
        input_path = os.path.join(base_dir, f"{month_str}_input.json")
        if not os.path.exists(input_path):
            print(f"{month_str} continued.")
            continue
        _do_translation(input_path, output_path, kimi)
        print(f"{month_str} done.")


def _need_redo(base_dir, month_str):
    count_input = 0
    if not os.path.exists(f"{base_dir}/{month_str}_input.json"):
        return False
    with open(f"{base_dir}/{month_str}_input.json", "r", encoding="utf-8") as fd:
        for line in fd:
            count_input += 1

    count_trans = 0
    if not os.path.exists(f"{base_dir}/{month_str}_input_translated.json"):
        return True
    with open(f"{base_dir}/{month_str}_input_translated.json", "r", encoding="utf-8") as fd:
        for line in fd:
            count_trans += 1

    if count_trans != count_input:
        return True
    return False


if __name__ == "__main__":
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "policy_classification_data", "policy_std"))
    month_set = set()
    for name in os.listdir(base_dir):
        # 从文件或目录名中提取形如 YYYY_MM 的片段
        m = name.split("_")[0]
        if m:
            month_str = m
            if _need_redo(base_dir, month_str):
                month_set.add(month_str)
    month_list = sorted(month_set)
    print(month_list)
    print(len(month_list))
    # 并行处理：将 month_list 切分为 20 个批次，每个批次一个进程，进程内只初始化一次 EmbedPolicy
    max_workers = 40
    n = len(month_list)
    if n > 0:
        chunk_size = max(1, (n + max_workers - 1) // max_workers)
        chunks = [month_list[i:i + chunk_size] for i in range(0, n, chunk_size)]
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(_process_month_chunk, chunk, base_dir) for chunk in chunks]
            for _ in as_completed(futures):
                pass
    print(f"All done. {len(month_list)} months processed.")
