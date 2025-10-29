import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

from llm.llm_embed import EmbedPolicy
# import llm.gitee_api as gitee
import llm.kimi_api as kimi
from policy_clustering import assign_single_policy as asp

policy_types = ["政府政策", "系统平台举措与规定", "其它事件"]

platform_action_map = {
    "工具链与开发环境": "系统平台举措与规定",
    "系统功能与API迭代": "系统平台举措与规定",
    "开发者资源支持": "系统平台举措与规定",
    "应用审核与发布限制": "系统平台举措与规定",
    "关键功能和服务控制": "系统平台举措与规定",
    "官方收录和背书支持三方库/框架": "系统平台举措与规定",
    "开发者协议与分成机制": "系统平台举措与规定",
    "安全与隐私技术": "系统平台举措与规定"
}

policy_event_map = {
    "数据隐私与权限管理": "外部政策与环境",
    "技术标准与认证": "外部政策与环境",
    "行业联盟与供应链生态共建": "外部政策与环境",
    "司法诉讼与仲裁": "外部政策与环境",
    "硬件厂商合作": "外部政策与环境",
    "法律和行政政策合规": "外部政策与环境",
    "资本运作": "外部政策与环境",
    "开源协议与合规": "外部政策与环境"
}


def _ask_for_type(event_name, ori_output_name, policy_category):
    prompt3 = f'''
    你是一个移动操作系统开源软件供应链政策和发展战略研究方面的专家。请将这条政策或者事件的类型归类为“政府政策”、“系统平台举措与规定”、“其它事件”之一。注意：
    1. "政府政策"指由国家或地方政府所颁发的政策、法规、标准等；
    2. "系统平台举措与规定"是包括Google、Apple、华为、社交媒体平台等知名大型厂商所发布或采取的规定或技术标准、要求等；
    3. "其它事件"包括由非上述2类发起方所主导提出的其它类型的事件和自发形成的新共识等；
    4. 返回只能是上述3个类型对应的字符串之一，严格以字符串形式返回，不要给出任何其它内容。

    需要分类的事件是：{event_name}
    '''

    prompt2 = f'''
        你是一个移动操作系统开源软件供应链政策和发展战略研究方面的专家。请将这条政策或者事件的类型归类为“政府政策”、“其它事件”之一。注意：
        1. "政府政策"指由国家或地方政府所颁发的政策、法规、标准等；
        2. "其它事件"包括由非政府发起的其它类型的事件和自发形成的新共识等；
        3. 返回只能是上述2个类型对应的字符串之一，严格以字符串形式返回，不要给出任何其它内容。

        需要分类的事件是：{event_name}
        '''
    if policy_category:
        if policy_category in platform_action_map:
            return "系统平台举措与规定"
        elif policy_category in policy_event_map:
            prompt = prompt2
        else:
            prompt = prompt3
    else:
        prompt = prompt3

    ptype = None
    for _ in range(3):
        ptype = kimi.KimiClient().chat(prompt)
        if ptype and ptype in policy_types:
            print(f"                                                  message: kimi OK: {ptype} : {ori_output_name}")
            return ptype
    print(f"                                                  warning: kimi none: {ptype} : {ori_output_name}")
    return None


def _rematch_en(no_match_rec_list, ep_model, month_str):
    best_match_dict = {}
    best_type_dict = {}
    ret_event_dict = {"政府政策": [], "平台举措": [], "其它事件": []}
    ori_rematch_list = []
    rematch_emb = {}
    for no_match in no_match_rec_list:
        ori_rematch_list.append({"name": no_match["event"], "content": no_match["event_en"],
                                 "policy_category": no_match.get("policy_category", None)})

    rematch_list = ori_rematch_list

    while len(rematch_list) > 0:
        no_match_name = rematch_list[0]["name"]
        no_match_content = rematch_list[0]["content"]
        policy_category = rematch_list[0]["policy_category"]
        if no_match_name not in rematch_emb:
            rematch_emb[no_match_name] = ep_model.embed_text(no_match_content)
            policy_type = _ask_for_type(no_match_name, month_str, policy_category)
            if policy_type:
                ret_event_dict[policy_type].append(no_match_name)
                best_type_dict[no_match_name] = policy_type
            else:
                best_type_dict[no_match_name] = "其它事件"
                ret_event_dict["其它事件"].append(no_match_name)

            try_rematch_list = []
            for event in rematch_list:
                event_name = event["name"]
                event_content = event["content"]
                best_name, no_match = asp(event_content, rematch_emb, ep_model)
                if no_match > 0:
                    try_rematch_list.append(event)
                else:
                    if event_name not in best_match_dict:
                        best_match_dict[event_name] = best_name
            rematch_list = try_rematch_list
        else:
            rematch_list = rematch_list[1:]

    ret_best_match_list = []
    for rec in no_match_rec_list:
        rec["std_event"] = best_match_dict[rec["event"]]
        rec["std_event_type"] = best_type_dict[rec["std_event"]]
        ret_best_match_list.append(rec)
    return ret_best_match_list, ret_event_dict


def _solve_monthly_en(input_path, output_path, event_path, ep_model):
    en_rec_list = []
    with open(input_path, 'r') as fd:
        for line in fd:
            rec = json.loads(line.strip())
            en_rec_list.append(rec)
    output_rect_list, event_map = _rematch_en(en_rec_list, ep_model, input_path.split("/")[-1])

    with open(output_path, 'w') as fd:
        for line in output_rect_list:
            fd.write(json.dumps(line, ensure_ascii=False) + '\n')

    with open(event_path, 'w') as fd:
        fd.write(json.dumps(event_map, ensure_ascii=False, indent=4))


def _process_month_chunk(months, base_dir, output_dir):
    local_ep = EmbedPolicy()
    for month_str in months:
        input_path = os.path.join(base_dir, f"{month_str}_input_translated.json")
        output_path = os.path.join(output_dir, f"{month_str}_output.json")
        event_path = os.path.join(output_dir, f"{month_str}_events.json")
        if not os.path.exists(input_path):
            print(f"{month_str} continued.")
            continue
        _solve_monthly_en(input_path, output_path, event_path, local_ep)
        print(f"{month_str} done.")


if __name__ == "__main__":
    output_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "policy_classification_data", "policy_std_en"))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "policy_classification_data", "policy_std"))
    month_set = set()
    for name in os.listdir(base_dir):
        # 从文件或目录名中提取形如 YYYY_MM 的片段
        m = name.split("_")[0]
        if m:
            month_str = m
            output_rect_file = f"{output_dir}/{month_str}_output.json"
            if not os.path.exists(output_rect_file):
                month_set.add(month_str)
    month_list = sorted(month_set)
    month_list = ["2014-12"]
    print(month_list)
    print(len(month_list))
    # 并行处理：将 month_list 切分为 20 个批次，每个批次一个进程，进程内只初始化一次 EmbedPolicy
    max_workers = 40
    n = len(month_list)
    if n > 0:
        chunk_size = max(1, (n + max_workers - 1) // max_workers)
        chunks = [month_list[i:i + chunk_size] for i in range(0, n, chunk_size)]
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(_process_month_chunk, chunk, base_dir, output_dir) for chunk in chunks]
            for _ in as_completed(futures):
                pass
    print(f"All done. {len(month_list)} months processed.")
