import json
import os
import glob
import matplotlib.pyplot as plt


# 合并所有年-月_output.json文件
def merge_output_files(source_folder, target_folder):
    # 查找所有_output.json文件
    pattern = os.path.join(source_folder, "*_output.json")
    input_files = glob.glob(pattern)

    # 合并所有内容
    output_items = []
    for file_path in input_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    item = json.loads(line)
                    output_items.append(item)

    # 保存合并结果
    output_file = os.path.join(target_folder, "all_output.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in output_items:
            line = json.dumps(item, ensure_ascii=False)
            f.write(line + '\n')

    return output_items


# 统计每种事件的数量
def count_events(all_items, bar_chart):
    # 创建字典
    # 相同的std_event只保留最后一个std_event_type
    std_event_to_std_event_type = {}
    for item in all_items:
        std_event = item['std_event']
        std_event_type = item['std_event_type']
        if std_event:
            std_event_to_std_event_type[std_event] = std_event_type

    # 统计数量
    # total_count = len(std_event_to_std_event_type)
    government_policy_count = sum(1 for value in std_event_to_std_event_type.values() if value == "政府政策")
    platform_action_count = sum(1 for value in std_event_to_std_event_type.values() if value == "平台举措")
    others_count = sum(1 for value in std_event_to_std_event_type.values() if value == "其它事件")

    counts = [government_policy_count, platform_action_count, others_count]
    labels = ['政府政策', '平台举措', '其它事件']

    # 创建条形图
    plt.figure(figsize=(6, 6))
    colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
        '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
        '#F8C471', '#82E0AA', '#F1948A', '#85C1E9', '#D7BDE2',
        '#F9E79F', '#A9DFBF', '#F5B7B1', '#AED6F1', '#E8DAEF'
    ]
    colors = [colors[i % len(colors)] for i in range(len(labels))]
    plt.bar(labels, counts, width=0.3, color=colors)

    plt.ylabel('数量', fontsize=14)
    plt.xlabel('事件类别', fontsize=14)

    # 保存到指定路径
    plt.savefig(bar_chart, dpi=300, bbox_inches='tight')
    plt.close()

    return std_event_to_std_event_type


# 统计各类政府政策的数量
def count_government_policy_events(all_items, bar_chart):
    # 筛选std_event_type为"政府政策"的记录
    government_policy_items = [item for item in all_items if item.get('std_event_type') == "政府政策"]

    # 创建字典
    # 相同的std_event只保留最后一个policy_category
    std_event_to_policy_category = {}
    for item in government_policy_items:
        std_event = item['std_event']
        policy_category = item.get('policy_category', '其它影响因素')
        if std_event and policy_category:
            std_event_to_policy_category[std_event] = policy_category

    external_policy_category_list = [
        "法律和行政政策合规", "数据隐私与权限管理", "技术标准与认证", "开源协议与合规",
        "硬件厂商合作", "行业联盟与供应链生态共建", "资本运作", "司法诉讼与仲裁"]

    external_policy_category_to_number = {category: 0 for category in external_policy_category_list}
    external_policy_category_to_number["其它影响因素"] = 0
    for value in std_event_to_policy_category.values():
        if value in external_policy_category_list:
            external_policy_category_to_number[value] += 1
        else:
            external_policy_category_to_number["其它影响因素"] += 1

    # 根据数量画条形图
    counts = list(external_policy_category_to_number.values())
    labels = list(external_policy_category_to_number.keys())

    # 创建条形图
    plt.figure(figsize=(8, 6))
    colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
        '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
        '#F8C471', '#82E0AA', '#F1948A', '#85C1E9', '#D7BDE2',
        '#F9E79F', '#A9DFBF', '#F5B7B1', '#AED6F1', '#E8DAEF'
    ]
    colors = [colors[i % len(colors)] for i in range(len(labels))]

    labels = labels[::-1]
    counts = counts[::-1]

    plt.barh(labels, counts, color=colors)

    plt.xlabel('数量')
    plt.ylabel('外部政策与环境（详细类别）')

    # 保存到指定路径
    plt.savefig(bar_chart, dpi=300, bbox_inches='tight')
    plt.close()

    return external_policy_category_to_number


if __name__ == "__main__":
    source_folder = './figure_data/output'
    target_folder = './figure_data'

    all_items = merge_output_files(source_folder, target_folder)

    events_bar_chart = './figure_result/events.png'
    government_policy_events_bar_chart = './figure_result/government_policy_events.png'
    # 支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    # 防止负号变成方块
    plt.rcParams['axes.unicode_minus'] = False

    std_event_to_std_event_type = count_events(all_items, events_bar_chart)
    external_policy_category_to_number = count_government_policy_events(all_items, government_policy_events_bar_chart)
