import json
import os

from tqdm import tqdm

import llm.kimi_api as kimi
from concurrent.futures import ThreadPoolExecutor, as_completed

# policy_topics = ["用户权益和隐私保护", "产业生态培育", "技术攻关和创新推动", "技术基础设施建设", "安全保障",
#                  "国际合作与标准制定", "人才培养"]

policy_topics = ["技术自主可控与国产化", "软件审核规定", "安全技术要求", "产业生态建设", "开源生态发展", "数据治理与战略"
                                                                                                         "市场竞争与反垄断",
                 "个人信息与隐私保护规定", "数据出境安全评估", "人才培养", "国际合作与标准制定", "应用推广与示范"]


def _assign_topic(std_event_name):
    prompt = (
        f'你是一个移动操作系统开源软件政策和战略专家，请将政策"{std_event_name}"分类为以下主题中的一个：{list(policy_topics)}。'
        f'注意尽量选择上述主题中的一个，返回类型对应主题相关字符串，不要开展分析或返回任何其它内容。')
    for _ in range(3):
        ptype = kimi.KimiClient().chat(prompt)
        if ptype and ptype in list(policy_topics):
            return ptype
        # elif ptype:
        #     print(f"                  message: kimi new topic: {ptype} : {std_event_name}")
        #     return ptype
    return None


def execute_gov_policy_topic():
    known_events = set()
    output_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "policy_classification_data", "policy_topics"))
    os.makedirs(output_dir, exist_ok=True)

    output_file = f"{output_dir}/policy_topics.json"

    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as fd:
            for line in fd:
                event = json.loads(line)
                known_events.add(event["std_event"])

    events_set = set()
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "policy_classification_data", "policy_std_en"))
    for name in os.listdir(base_dir):
        if "events.json" in name:
            with open(f"{base_dir}/{name}", "r", encoding="utf-8") as fd:
                events = json.load(fd)
                for event in events["政府政策"]:
                    if event not in known_events:
                        events_set.add(event)
    print(f"待处理数量: {len(events_set)}")

    with open(output_file, "a", encoding="utf-8") as fw:
        # 使用100线程并行为事件分配主题，写入仍串行以保证文件安全
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(_assign_topic, event): event for event in events_set if
                       event not in known_events}
            for future in as_completed(futures):
                event = futures[future]
                try:
                    topic = future.result()
                except Exception:
                    topic = None
                rec = {"std_event": event, "topic": topic}
                fw.write(json.dumps(rec, ensure_ascii=False) + "\n")
                known_events.add(event)


def append_policy_topic():
    topics_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "policy_classification_data", "policy_topics"))
    topics_file = f"{topics_dir}/policy_topics.json"

    topics_dict = {}
    with open(topics_file, "r", encoding="utf-8") as fd:
        for line in fd:
            event = json.loads(line)
            topics_dict[event["std_event"]] = event["topic"]

    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "policy_classification_data", "policy_std_en"))
    for name in tqdm(os.listdir(base_dir)):
        if "output.json" in name:
            policy_event_list = []
            with open(f"{base_dir}/{name}", "r", encoding="utf-8") as fd:
                for line in fd:
                    event = json.loads(line)
                    if event.get("std_event_type", "") == "政府政策":
                        if event["std_event"] in topics_dict:
                            event["std_policy_topic"] = topics_dict.get(event["std_event"])
                    policy_event_list.append(event)
            with open(f"{base_dir}/{name}", "w", encoding="utf-8") as fd:
                for evt in policy_event_list:
                    fd.write(json.dumps(evt, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    execute_gov_policy_topic()
    append_policy_topic()
