from llm.llm_embed import EmbedPolicy
import numpy as np
import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed


def _json_safe(obj):
    import numpy as np
    if isinstance(obj, dict):
        return {_json_safe(k): _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_safe(x) for x in obj]
    if isinstance(obj, tuple):
        return tuple(_json_safe(x) for x in obj)
    if isinstance(obj, set):
        return [_json_safe(x) for x in obj]
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return _json_safe(obj.tolist())
    return obj


def assign_single_policy(policy_text: str, standard_policy_embed_dir, ep_model):
    """
    policy_text为待标准化的政策文本

    standard_policy_embed_dir为标准化的政策对应的嵌入向量字典，形如：
    {
        "标准化政策名称": float(768),
        "标准化政策名称": float(768),
        ...
    }
    """
    if policy_text in standard_policy_embed_dir:
        print(f"!!!!!! direct return: {policy_text}")
        return policy_text, 0
    p_emb = ep_model.embed_text(policy_text)
    # 使用欧式距离（L2范数）寻找最近的标准化政策
    min_dist = float('inf')
    best_name = None
    dists_list = []
    for policy_name, std_emb in standard_policy_embed_dir.items():
        dist = np.linalg.norm(np.array(p_emb) - np.array(std_emb))
        dists_list.append((policy_name, dist))
        if dist < min_dist:
            min_dist = dist
            best_name = policy_name
    # 根据距离分布判断是否疑似都不匹配
    if len(dists_list) == 0:
        no_match = 1
    else:
        all_dists = np.array([d for _, d in dists_list])
        sorted_dists = np.sort(all_dists)
        second_min = sorted_dists[1] if len(sorted_dists) > 1 else sorted_dists[0]
        std = all_dists.std()
        median = float(np.median(all_dists))
        distinct_top = (second_min - min_dist) / (std + 1e-8)
        relative_to_median = min_dist / (median + 1e-8)
        if (distinct_top < 0.7) and (relative_to_median > 0.3):
            no_match = 1
        else:
            no_match = 0
    # 可根据 no_match 进一步处理（当前仅计算）
    print(f"!!!!!! normal return ({no_match}): {policy_text}: {best_name} : {distinct_top} : {relative_to_median}")
    return best_name, no_match


def policy_standardize_monthly(input_policy_list: list, standard_policy_list: list, ep_model):
    """
    输入待标准化的政策列表input_policy_list，形如：
    [
        {"政策名称": "政策内容"},
        {"政策名称": "政策内容"},
        ...
    ]

    输入标准化的政策列表standard_policy_list，形如：
    [
        {"标准化政策名称": "标准化政策内容"},
        {"标准化政策名称": "标准化政策内容"},
        ...
    ]

    返回长度等于len(input_policy_list)的str类型列表，包含与输入政策列表对应的标准化政策名称，形如：
    ["标准化政策名称", "标准化政策名称", ..., "标准化政策名称"]
    """
    standard_policy_embed_dir = {}
    for std_policy_name in standard_policy_list:
        # std_policy_name = list(std_policy.keys())[0]
        # std_policy_text = list(std_policy.values())[0]
        # std_policy_text = f"{std_policy_name} {std_policy_text}"
        std_policy_emb = ep_model.embed_text(std_policy_name)
        standard_policy_embed_dir[std_policy_name] = std_policy_emb

    ret_list = []
    no_match_list = []
    for input_policy in input_policy_list:
        input_policy_name = list(input_policy.keys())[0]
        input_policy_text = list(input_policy.values())[0]
        input_policy_text = f"{input_policy_name} {input_policy_text}"
        std_policy_name, no_match = assign_single_policy(input_policy_text, standard_policy_embed_dir, ep_model)
        ret_list.append(std_policy_name)
        no_match_list.append(no_match)

    return ret_list, no_match_list


# 线程工作函数：每个线程内部创建独立 EmbedPolicy 实例并处理一个批次
def _process_month_chunk(months):
    # 每进程仅初始化一次模型
    local_ep = EmbedPolicy()
    for month_str in months:
        input_policy_list = []
        input_policy_records = []
        with open(f"../policy_classification_data/policy_std/{month_str}_input.json", "r", encoding="utf-8") as fd:
            for line in fd:
                line = line.strip()
                if line:
                    input_policy = json.loads(line)
                    input_policy_records.append(input_policy)
                    # input_policy_list.append({input_policy['event']: input_policy['policy_content']['政策内容和影响']})
                    input_policy_list.append({input_policy['event']: ""})
        standard_policy_list = []
        standard_policy_type = {}
        with open(f"../policy_classification_data/policy_std/{month_str}_events.json", "r", encoding="utf-8") as fd:
            data = json.load(fd)
            for type in ["政府政策", "平台举措", "其它事件"]:
                if len(data[type]) == 0:
                    continue
                for item in data[type]:
                    standard_policy_list.append(item)
                    standard_policy_type[item] = type
        ret_list, no_match_list = policy_standardize_monthly(input_policy_list, standard_policy_list, local_ep)
        print(month_str)
        # print(ret_list)
        with open(f"../policy_classification_data/policy_std/{month_str}_output.json", "w", encoding="utf-8") as fd:
            for idx, std_policy_name in enumerate(ret_list):
                input_policy_records[idx]['std_event'] = std_policy_name
                input_policy_records[idx]['std_event_type'] = standard_policy_type[std_policy_name]
                input_policy_records[idx]['no_match'] = no_match_list[idx]
                if no_match_list[idx] > 0:
                    print(input_policy_records[idx])
                fd.write(json.dumps(_json_safe(input_policy_records[idx]), ensure_ascii=False) + "\n")


if __name__ == "__main__":
    # 枚举 ../policy_classification_data/policy_std/ 目录下所有出现过的年_月字符串
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "policy_classification_data", "policy_std"))
    month_set = set()
    for name in os.listdir(base_dir):
        # 从文件或目录名中提取形如 YYYY_MM 的片段
        m = name.split("_")[0]
        if m:
            month_str = m
            output_path = os.path.join(base_dir, f"{month_str}_output.json")
            input_path = os.path.join(base_dir, f"{month_str}_input.json")
            events_path = os.path.join(base_dir, f"{month_str}_events.json")
            if not os.path.exists(output_path) and os.path.exists(input_path) and os.path.exists(events_path):
                month_set.add(month_str)
    month_list = sorted(month_set)
    print(month_list)
    # 按批次并行：20进程，每进程处理一段月份，且进程内仅初始化一次模型
    max_workers = 20
    n = len(month_list)
    if n > 0:
        chunk_size = max(1, (n + max_workers - 1) // max_workers)
        chunks = [month_list[i:i + chunk_size] for i in range(0, n, chunk_size)]
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(_process_month_chunk, chunk) for chunk in chunks]
            for _ in as_completed(futures):
                pass
    print(f"All done. {len(month_list)} months processed.")
