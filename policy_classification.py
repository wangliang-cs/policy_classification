from openai import OpenAI
import json
from tqdm import tqdm
import concurrent.futures
import threading
import config

# 创建客户端（在主线程创建，共享给所有线程）
qw_client = OpenAI(
    base_url="https://ai.gitee.com/v1",
    api_key="LV41QCCDGLTQLUUUBAM8KXZKCQOS4ZTUTQDGH461",
    default_headers={"X-Failover-Enabled": "true"},
)

# 全局 prompt 和 categories

prompt_1 = (
    "你是专业的事件类别分析助手。请按以下要求执行：\n"
    "1. 根据所提供的事件具体信息，将其分类为候选事件和政策类别列表中的一个类别，不得出现其他内容\n"
    "2. 必须返回一个str类型的分类结果，不要任何额外文本、解释、换行或空格，也不要包含括号内的内容。\n"
    "示例正确返回格式：'开发者协议与分成机制'\n")

categories_name = config.get_config("categories_name")

categories = config.get_config("categories")


def analyze_repository(prompt):
    """调用 Qwen 模型进行分析"""
    try:
        response = qw_client.chat.completions.create(
            model="Qwen3-32B",
            stream=False,
            temperature=0.7,
            messages=[
                # {"role": "system", "content": prompt_1},
                {"role": "user", "content": prompt}
            ],
        )
        content = response.choices[0].message.content.strip()
        return content
    except Exception as e:
        print(f"API 调用出错: {e}")
        return None


def classify_policy(item):
    """分类单个政策事件"""
    event = item["event"]
    policy_content = item["policy_content"]
    prompt = f"{prompt_1}候选事件和政策类别列表：{categories}，事件具体信息：{event} -- {policy_content}"
    response = analyze_repository(prompt)
    for _ in range(3):
        if response and isinstance(response, str):
            if response in categories_name:
                item["policy_category"] = response
                break
        response = analyze_repository(prompt)
    return item


def main(data_path, output_path):
    # 读取数据
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    policy_data_list = []
    for item in data:
        repo = item.get("repo", "")
        policy = item.get("policy", {})  # 修复变量引用问题
        for policy_type in ["有利政策", "不利政策"]:
            if policy_type in policy and isinstance(policy[policy_type], dict) and len(policy[policy_type]) > 0:
                for event in policy[policy_type]:
                    policy_data_list.append({
                        "repo": repo,
                        "policy_type": policy_type,
                        "event": event,
                        "policy_content": policy[policy_type][event]
                    })
    print(f"共 {len(policy_data_list)} 条政策数据：{data_path}")

    # 创建文件写入锁
    file_lock = threading.Lock()

    # 定义单个项目的处理函数
    def process_item(item):
        item = classify_policy(item)
        with file_lock:
            with open(output_path, 'a', encoding='utf-8') as fw:
                fw.write(json.dumps(item, ensure_ascii=False) + '\n')
                fw.flush()
        return item

    # 使用线程池并发处理
    max_workers = 200
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 使用tqdm显示进度
        list(tqdm(executor.map(process_item, policy_data_list), total=len(policy_data_list)))


if __name__ == "__main__":
    # 提供默认参数，但保留原有的循环处理逻辑
    # for eco in ["Android", "iOS"]:
    for eco in ["iOS"]:
        data_path = f"../policy_classification_data/{eco}.json"
        output_path = f"../policy_classification_data/{eco}_output.json"
        main(data_path, output_path)
