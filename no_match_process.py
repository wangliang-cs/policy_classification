import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

from llm.llm_embed import EmbedPolicy
# import llm.gitee_api as gitee
import llm.kimi_api as kimi
from policy_clustering import assign_single_policy as asp

policy_types = ["政府政策", "平台举措", "其它事件"]


def _extract_english(input_text: str):
    import re
    english_pattern = re.compile(r'[a-zA-Z]{3,}')
    matches = english_pattern.findall(input_text)
    if len(matches) >= 2:
        # print(f"{input_text} ->> {' '.join(matches)}")
        return ' '.join(matches)
    # print(f"{input_text} -xx {input_text}")
    return input_text
    

def _ask_for_type(event_name, ori_output_name):
    prompt = f'''
    你是一个移动操作系统开源软件供应链政策和发展战略研究方面的专家。请将这条政策或者事件的类型归类为“政府政策”、“平台举措”、“其它事件”之一。注意：
    1. 政府政策指由国家或地方政府所颁发的政策、法规、标准等；
    2. 平台举措是包括Google、Apple、华为、社交媒体平台等知名大型厂商所发布或采取的规定或技术标准、要求等；
    3. 其它事件包括由非上述2类发起方所主导提出的其它类型的事件和自发形成的新共识等；
    4. 返回只能是上述三个类型对应的字符串之一，严格以字符串形式返回，不要给出任何其它内容。
    
    需要分类的事件是：{event_name}
    '''
    ptype = None
    for _ in range(3):
        ptype = kimi.KimiClient().chat(prompt)
        if ptype and ptype in policy_types:
            print(f"                                                  message: kimi OK: {ptype} : {ori_output_name}")
            return ptype
    print(f"                                                  warning: kimi none: {ptype} : {ori_output_name}")
    return None


def _rematch(no_match_rec_list, ep_model, ori_output_name):
    best_match_dict = {}
    best_type_dict = {}
    ret_event_dict = {"政府政策": [], "平台举措": [], "其它事件": []}
    ori_rematch_list = []
    rematch_emb = {}
    for no_match in no_match_rec_list:
        no_match_event = f'{no_match["event"]}'
        ori_rematch_list.append(no_match_event)

    rematch_list = ori_rematch_list

    while len(rematch_list) > 0:
        no_match_event = rematch_list[0]
        no_match_event = _extract_english(no_match_event)
        if no_match_event not in rematch_emb:
            if no_match_event == "Google开放RecyclerView扩展政策":
                print("++++++++++++++++++++++++++++++++++++")
                print(no_match_event)
                print("++++++++++++++++++++++++++++++++++++")
            # en_name = _extract_english(no_match_event)
            rematch_emb[no_match_event] = ep_model.embed_text(no_match_event)
            policy_type = _ask_for_type(rematch_list[0], ori_output_name)
            if policy_type:
                ret_event_dict[policy_type].append(no_match_event)
                best_type_dict[no_match_event] = policy_type
            else:
                best_type_dict[no_match_event] = "其它事件"
                ret_event_dict["其它事件"].append(no_match_event)

            try_rematch_list = []
            for event in rematch_list:
                best_name, no_match = asp(_extract_english(event), rematch_emb, ep_model)
                if no_match > 0:
                    if event == "Google开放RecyclerView扩展政策":
                        print('-----------------------------------')
                        print(event)
                        print('-----------------------------------')
                    try_rematch_list.append(event)
                else:
                    if event not in best_match_dict:
                        best_match_dict[event] = best_name
                if event == "Google开放RecyclerView扩展政策":
                    print("============================================")
                    print(event)
                    print(best_name)
                    print(no_match)
                    print("============================================")
            rematch_list = try_rematch_list
            # print(rematch_list)
        else:
            rematch_list = rematch_list[1:]

    ret_best_match_list = []
    for rec in no_match_rec_list:
        rec["std_event"] = best_match_dict[rec["event"]]
        rec["std_event_type"] = best_type_dict[rec["std_event"]]
        ret_best_match_list.append(rec)
    return ret_best_match_list, ret_event_dict


def _solve_monthly_no_match(ori_output_name, ori_events_name, input_dir, output_dir, ep_model):
    ori_output_file = f"{input_dir}/{ori_output_name}"
    no_match_rec_list = []
    output_rect_list = []
    with open(ori_output_file, 'r') as fd:
        for line in fd:
            rec = json.loads(line.strip())
            no_match_rec_list.append(rec)
            # if 'no_match' not in rec or rec['no_match'] > 0:
            #     no_match_rec_list.append(rec)
            # else:
            #     output_rect_list.append(rec)
    best_match_list, ret_event_dict = _rematch(no_match_rec_list, ep_model, ori_output_name)
    for new_match in best_match_list:
        output_rect_list.append(new_match)

    ori_events_file = f"{input_dir}/{ori_events_name}"
    if os.path.exists(ori_events_file):
        with open(ori_events_file, 'r') as fd:
            event_map = json.load(fd)
    else:
        event_map = {"政府政策": [], "平台举措": [], "其它事件": []}

    for ptype in policy_types:
        if ptype not in event_map:
            event_map[ptype] = []
        event_map[ptype].extend(ret_event_dict[ptype])

    output_rect_file = f"{output_dir}/{ori_output_name}"
    with open(output_rect_file, 'w') as fd:
        for line in output_rect_list:
            fd.write(json.dumps(line, ensure_ascii=False) + '\n')

    output_event_file = f"{output_dir}/{ori_events_name}"
    with open(output_event_file, 'w') as fd:
        fd.write(json.dumps(event_map, ensure_ascii=False, indent=4))


def _process_month_chunk(months, base_dir, output_dir):
    local_ep = EmbedPolicy()
    for month_str in months:
        output_path = os.path.join(base_dir, f"{month_str}_output.json")
        input_path = os.path.join(base_dir, f"{month_str}_input.json")
        if not os.path.exists(output_path) and not os.path.exists(input_path):
            print(f"{month_str} continued.")
            continue
        output_name = f"{month_str}_output.json"
        if not os.path.exists(output_path):
            output_name = f"{month_str}_input.json"
        # event_name = f"{month_str}_events.json"
        event_name = f"{month_str}_events_disabled.json"
        _solve_monthly_no_match(output_name, event_name, base_dir, output_dir, local_ep)
        print(f"{month_str} done.")


if __name__ == "__main__":
    output_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "policy_classification_data", "policy_std_rematch"))
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
    # month_list = ["2014-12"]
    print(month_list)
    # 并行处理：将 month_list 切分为 20 个批次，每个批次一个进程，进程内只初始化一次 EmbedPolicy
    max_workers = 20
    n = len(month_list)
    if n > 0:
        chunk_size = max(1, (n + max_workers - 1) // max_workers)
        chunks = [month_list[i:i + chunk_size] for i in range(0, n, chunk_size)]
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(_process_month_chunk, chunk, base_dir, output_dir) for chunk in chunks]
            for _ in as_completed(futures):
                pass
    print(f"All done. {len(month_list)} months processed.")
