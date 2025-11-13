import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

platform_list = ["Android", "iOS", "pub_dev", "kmp", "rn_directory"]
policy_type_list = ["favorable_policy", "unfavorable_policy"]

technology_category_list = [
    "编译器与语言工具链", "操作系统与平台相关技术", "硬件抽象层", "系统级构建与部署", "架构模式实现",
    "构建与部署（通用）", "开发效率/IDE插件", "代码质量与规范", "依赖与包管理", "单元测试与UI测试",
    "调试与诊断", "日志与监控", "崩溃监控与异常处理", "教程与文档", "社区与工具集", "文档与格式处理",
    "内容管理", "分析与统计", "设备间通信", "实时通信", "机器学习框架", "计算机视觉", "AR/VR", "区块链集成",
    "游戏引擎与框架", "游戏组件", "定位与地图", "支付集成", "推送与广告服务", "日期与时间处理", "图表",
    "事件总线", "数据结构与算法", "函数式工具", "响应式与异步编程", "依赖注入（DI）", "HTTP/HTTPS网络库",
    "数据存储", "数据解析", "数据安全与加密解密", "认证与授权", "基础控件", "布局框架", "动画与视觉效果",
    "主题与样式", "文本与字体处理", "图像处理", "视频处理", "音频处理", "相机与传感器",
    '不明确', '云原生后端即服务(BaaS)', '代码生成与脚手架', '内容管理系统(CMS)', '医院信息系统', '命令行与工具集',
    '命令行与终端工具', '图形处理与渲染', '媒体内容管理', '工具集', '应用分发平台', '应用间通信', '操作系统',
    '数据分析与统计', '数据同步', '数据验证', '数据验证与通知', '文件处理与系统接口', '文件系统监控', '物联网',
    '状态管理扩展', '电商集成', '编程语言桥接', '编译器与运行时', '编译器前端', '编译器技术',
    '编译器插件与中间表示（IR）模板', '网络与安全', '设备与传感器', '配置中心', '音视频处理']
technology_category_dictionary = {item: [item] for item in technology_category_list}

business_category_list = [
    "操作系统与平台", "编程语言与编译器", "移动应用生态", "开源操作系统生态建设", "开源生态与社区运营",
    "云原生与DevOps服务", "CI/CD平台与云存储", "API管理与密码工具", "身份认证与渗透测试", "数据隐私合规",
    "操作系统与智能终端基础软件", "AI/ML解决方案", "AI视觉技术", "AI聊天机器人与客服", "AI辅助医疗",
    "IoT应用与低功耗通信", "数据分析与个性化", "跨平台开发", "移动应用UI/UX设计", "移动应用性能与变现",
    "企业级SaaS", "企业数字化转型", "企业协作与CRM", "办公软件", "移动支付与转账", "数字银行", "信贷与风控",
    "健康管理与医疗支付", "视频与有声内容", "数字出版与内容推荐", "emoji品牌授权", "垂直领域电商",
    "共享出行与网约车", "即时配送与货运", "本地生活服务", "会员制零售", "可穿戴与智能设备", "慢性病管理与预防",
    "职业与编程教育", "K-12教育服务", "在线教育平台", "教育类游戏", "社交媒体平台", "赛事组织", "个人服务",
    "广告变现与受众分析", "程序化与场景广告", "C2C/B2B电商", "游戏",
    "身份认证与密码工具", "办公软件开发", "车载操作系统与智能座舱", "开源生态建设", "操作系统研发",
    "音频处理与移动应用", "电商系统", "游戏引擎与开发工具", "办公场所软件", "操作系统与系统安装",
    "区块链与Web3基础设施", 'B2C/B2B电商', 'Flutter开发工具', 'USB设备管理工具', '不明确', '代码质量与开发工具',
    '企業協作與CRM', '企業級SaaS', '個人服務', '办公应用', '办公软件开发工具', '区块链基础设施',
    '区块链底层协议与去中心化基础设施', '区块链底层协议研发', '实时音视频通信', '应用性能与变现', '操作系统开源治理',
    '数据处理与个性化', '数据库ORM与数据访问层', '数据库设备管理', '本地生活与到店服务', '本地生活信息平台',
    '本地生活服务SaaS', '游戏启动器与游戏工具', '游戏开发工具与中间件', '游戏开发工具与引擎', '游戏成就与数据身份服务',
    '编程教育工具', '编程语言', '编程语言与开发工具', '编程语言与开发者工具', '编程语言与开源库', '编程语言工具链',
    '编程语言设计与实现', '软件开发工具', '音乐与音频工具']
business_category_dictionary = {item: [item] for item in business_category_list}

external_policy_category_list = [
    "法律和行政政策合规", "数据隐私与权限管理", "技术标准与认证", "开源协议与合规",
    "硬件厂商合作", "行业联盟与供应链生态共建", "资本运作", "司法诉讼与仲裁"]
external_policy_category_dictionary = {
    "行业规范与合规要求": ["法律和行政政策合规", "数据隐私与权限管理", "技术标准与认证", "开源协议与合规"],
    "合作与竞争伙伴关系/行业生态构建": ["硬件厂商合作", "行业联盟与供应链生态共建", "资本运作", "司法诉讼与仲裁"],
    # 其它
    "外部和自身需求和技术发展更迭演化": ["其它影响因素"]
}

platform_measure_category_list = [
    "开发者协议与分成机制", "开发者资源支持", "应用审核与发布限制", "关键功能和服务控制",
    "系统功能与API迭代", "官方收录和背书支持三方库/框架", "安全与隐私技术", "工具链与开发环境"]
platform_measure_category_dictionary = {
    "平台相关政策与商业规则制定": [
        "开发者协议与分成机制", "开发者资源支持", "应用审核与发布限制", "关键功能和服务控制"
    ],
    "技术架构与系统维护更新": [
        "系统功能与API迭代", "官方收录和背书支持三方库/框架", "安全与隐私技术", "工具链与开发环境"
    ],
    # 其它
    "适应性举措": ["适应性举措与规定"]
}

fundamental_driver_category_list = [
    "内部降本", "开源引流", "直接变现", "抢占生态位", "对抗垄断/官方", "建立事实标准",
    "生态锁定", "个人技术名片", "组织技术背书", "教学与知识沉淀", "法规与政策合规",
    "许可证策略优化", "合规与许可一体化"]

fundamental_driver_category_dictionary = {
    "商业驱动": ["内部降本", "开源引流", "直接变现"],
    "生态与竞争驱动": ["抢占生态位", "对抗垄断/官方", "建立事实标准", "生态锁定"],
    "个人与组织品牌驱动": ["个人技术名片", "组织技术背书", "教学与知识沉淀"],
    "合规与许可驱动": ["法规与政策合规", "许可证策略优化", "合规与许可一体化"],
    # 其它
    "自身发展驱动": ["自身发展驱动力"]
}

method_category_list = [
    "填补原生空白", "适配新技术", "性能优化", "架构演进", "简化API/链式调用", "提升开发体验", "功能增强与一致性"]
method_category_dictionary = {
    "技术革新动力": ["填补原生空白", "适配新技术", "性能优化", "架构演进"],
    "用户体验提升动力": ["简化API/链式调用", "提升开发体验", "功能增强与一致性"],
    # 其它
    "技术和服务调整动力": ["适应新的技术和服务需求"]
}


# 解析原始政策数据
def parse_policy_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        policy_data = json.load(f)

    parsed_data = []

    for item in policy_data:
        if "policy_category" not in item:
            continue

        policy_category = item["policy_category"]

        external_policy_category = []
        for category in policy_category:
            if category in external_policy_category_list:
                external_policy_category.append(category)
        if not external_policy_category:
            external_policy_category = ["其它影响因素"]

        platform_measure_category = []
        for category in policy_category:
            if category in platform_measure_category_list:
                platform_measure_category.append(category)
        if not platform_measure_category:
            platform_measure_category = ["适应性举措与规定"]

        parsed_data.append({
            "repo": item.get("repo", ""),
            "external_policy_category": external_policy_category,
            "platform_measure_category": platform_measure_category
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=2)


# 解析原始驱动力数据
def parse_driver_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        driver_data = json.load(f)

    parsed_data = []

    for item in driver_data:
        if "minors" not in item:
            continue

        driver_category = item["minors"]

        fundamental_driver_category = []
        for category in driver_category:
            if category in fundamental_driver_category_list:
                fundamental_driver_category.append(category)
        if not fundamental_driver_category:
            fundamental_driver_category = ["自身发展驱动力"]

        method_category = []
        for category in driver_category:
            if category in method_category_list:
                method_category.append(category)
        if not method_category:
            method_category = ["适应新的技术和服务需求"]

        new_item = {
            "repo": item.get("repo", ""),
            "fundamental_driver_category": fundamental_driver_category,
            "method_category": method_category
        }
        parsed_data.append(new_item)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=2)


# 构建热力图
# y:字号缩小，x:字号缩小
def generate_heatmap(heatmap_data, output_file, Y_name, X_name, Y_category_list, X_category_list, y=0, x=0):
    heatmap_matrix = np.zeros((len(Y_category_list), len(X_category_list)))
    for i, Y_category in enumerate(Y_category_list):
        for j, X_category in enumerate(X_category_list):
            heatmap_matrix[i, j] = heatmap_data[Y_category][X_category]

    heatmap_matrix = np.round(heatmap_matrix).astype(int)

    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']

    # 对X轴、Y轴的类别列表做调整
    adjustment = {
        "提升开发体验": "提升开发/使用体验"
    }
    X_labels = [adjustment.get(item, item) for item in X_category_list]
    Y_labels = [adjustment.get(item, item) for item in Y_category_list]

    plt.figure(figsize=(12, 10))
    sns.heatmap(data=heatmap_matrix,
                annot=True,  # 在格子中显示数值
                fmt='d',  # 整数格式
                cmap='YlOrRd',  # 颜色映射
                xticklabels=X_labels,
                yticklabels=Y_labels,
                # 设置数字大小和粗细
                annot_kws={"size": 16 - max(x, y), "weight": "bold"},
                cbar_kws={"shrink": 0.8})

    # fontsize控制大小，rotation控制旋转角度
    plt.xticks(fontsize=16 - x, rotation=90)
    plt.yticks(fontsize=16 - y, rotation=0, va='center')

    plt.xlabel(X_name, fontsize=20)
    plt.ylabel(Y_name, fontsize=20)

    plt.tight_layout()

    # 保存矢量图
    plt.savefig(output_file, format='svg', bbox_inches='tight')
    plt.savefig(output_file.replace('.svg', '.png'), format='png', bbox_inches='tight', dpi=300)

    plt.close()


# 基于单文件生成小类热力图数据
def create_minor_heatmap_data_by_single_file(input_file, Y_field, X_field, Y_category_list, X_category_list):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 热力图数据
    result = {Y_category: {X_category: 0 for X_category in X_category_list} for Y_category in Y_category_list}

    # 遍历数据中的每个项目
    for item in data:
        # 判断是否为列表，如果是数值，转为列表
        if isinstance(item[Y_field], list):
            Y_category_for_project = item[Y_field]
        else:
            Y_category_for_project = [item[Y_field]]

        if isinstance(item[X_field], list):
            X_category_for_project = item[X_field]
        else:
            X_category_for_project = [item[X_field]]

        for y in Y_category_for_project:
            for x in X_category_for_project:
                if y != '不明确' and x != '不明确':
                    result[y][x] += 1

    return result


def create_major_heatmap_data(minor_heatmap_data, Y_category_dictionary, X_category_dictionary):
    result = {}
    for y in Y_category_dictionary.keys():
        result[y] = {}
        for x in X_category_dictionary.keys():
            result[y][x] = 0

    # 基于原字典构建小类到大类的映射关系
    Y_map = {}
    for major, minors in Y_category_dictionary.items():
        for minor in minors:
            Y_map[minor] = major

    X_map = {}
    for major, minors in X_category_dictionary.items():
        for minor in minors:
            X_map[minor] = major

    for y_minor, y_data in minor_heatmap_data.items():
        y_major = Y_map[y_minor]

        for x_minor, count in y_data.items():
            x_major = X_map[x_minor]

            # 累加计数
            result[y_major][x_major] += count

    return result


def create_minor_heatmap_data_by_double_files(Y_input_file, X_input_file, Y_field, X_field, Y_category_list,
                                              X_category_list):
    with open(Y_input_file, 'r', encoding='utf-8') as f:
        Y_data = json.load(f)
    with open(X_input_file, 'r', encoding='utf-8') as f:
        X_data = json.load(f)

    # 初始化结果（字典的字典）
    result = {Y_category: {X_category: 0 for X_category in X_category_list} for Y_category in Y_category_list}

    X_dictionary = {i["repo"]: i for i in X_data}
    for item in Y_data:
        repo = item["repo"]
        if repo in X_dictionary:
            corresponding_item = X_dictionary[repo]

            Y_field_for_project = item[Y_field]
            X_field_for_project = corresponding_item[X_field]

            if isinstance(Y_field_for_project, list):
                Y_category_for_project = Y_field_for_project
            else:
                Y_category_for_project = [Y_field_for_project]

            if isinstance(X_field_for_project, list):
                X_category_for_project = X_field_for_project
            else:
                X_category_for_project = [X_field_for_project]

            for y in Y_category_for_project:
                for x in X_category_for_project:
                    if y != '不明确' and x != '不明确':
                        result[y][x] += 1

    # 特殊处理
    if "许可证策略优化" in result and "其它影响因素" in result["许可证策略优化"]:
        result["许可证策略优化"]["开源协议与合规"] += result["许可证策略优化"]["其它影响因素"]
        result["许可证策略优化"]["其它影响因素"] = 0

    if "开源协议与合规" in result and "许可证策略优化" in result["开源协议与合规"]:
        result["开源协议与合规"]["许可证策略优化"] += result["其它影响因素"]["许可证策略优化"]
        result["其它影响因素"]["许可证策略优化"] = 0

    return result


# 对驱动力文件执行预处理
def preprocess_driver_data(input_file, output_file):
    output_data = []

    # 读取json文件
    with open(input_file, 'r', encoding='utf-8') as f:
        for number, line in enumerate(f, 1):
            line = line.strip()
            # 跳过空行
            if not line:
                continue
            try:
                item = json.loads(line)
                output_data.append(item)
            except json.JSONDecodeError as e:
                print(f"第{number}行解析错误: {e}")
                print(f"错误行: {line}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)


# 对政策文件执行预处理
def preprocess_policy_data(input_file, favorable_policy_file, unfavorable_policy_file):
    # 用于存储(repo, event)->item的映射
    dictionary = {}

    # 读取所有行
    # 按(repo, event)去重，仅保留最后一个
    with open(input_file, 'r', encoding='utf-8') as f:
        for number, line in enumerate(f, 1):
            line = line.strip()
            # 跳过空行
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"第{number}行解析错误：{e}")
                continue

            repo = item.get('repo')
            event = item.get('event')
            policy_type = item.get('policy_type')

            # 检查是否缺少必要字段
            if not repo:
                print(f"第{number}行缺少repo字段，跳过")
                continue
            if not event:
                print(f"第{number}行缺少event字段，跳过")
                continue

            policy_category = item.get('policy_category')
            if not policy_category:
                print(f"第{number}行（{repo}）缺少policy_category，跳过")
                continue

            # 使用(repo, event)作为键，保留最后一个
            key = (repo, event)
            dictionary[key] = {
                'repo': repo,
                'policy_type': policy_type,
                'policy_category': policy_category
            }

    # 按repo合并，收集policy_category
    repo_to_policy_category = {"favorable": {}, "unfavorable": {}}

    for item in dictionary.values():
        repo = item['repo']
        policy_type = item['policy_type']
        policy_category = item['policy_category']
        if policy_type == '有利政策':
            if repo not in repo_to_policy_category["favorable"]:
                repo_to_policy_category["favorable"][repo] = set()
            repo_to_policy_category["favorable"][repo].add(policy_category)
        elif policy_type == '不利政策':
            if repo not in repo_to_policy_category["unfavorable"]:
                repo_to_policy_category["unfavorable"][repo] = set()
            repo_to_policy_category["unfavorable"][repo].add(policy_category)

    # 构建输出列表
    favorable_policy_data = []
    for repo, policy_category in repo_to_policy_category["favorable"].items():
        favorable_policy_data.append({
            "repo": repo,
            "policy_category": sorted(list(policy_category))
        })

    unfavorable_policy_data = []
    for repo, policy_category in repo_to_policy_category["unfavorable"].items():
        unfavorable_policy_data.append({
            "repo": repo,
            "policy_category": sorted(list(policy_category))
        })

    with open(favorable_policy_file, 'w', encoding='utf-8') as f:
        json.dump(favorable_policy_data, f, ensure_ascii=False, indent=2)

    with open(unfavorable_policy_file, 'w', encoding='utf-8') as f:
        json.dump(unfavorable_policy_data, f, ensure_ascii=False, indent=2)


def merge_files(input_files, output_file):
    all_data = []
    for file in input_files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            all_data.extend(data)
    # 基于repo去重
    repo_to_project = {}
    for project in all_data:
        if isinstance(project, dict) and 'repo' in project:
            repo_to_project[project['repo']] = project
    all_data = list(repo_to_project.values())
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)


for platform in ["pub_dev", "kmp", "rn_directory"]:
    input_file = f"./heatmap_data/{platform}_driver_classify.json"
    output_file = f'./heatmap_data/{platform}_driver.json'
    preprocess_driver_data(input_file, output_file)

for platform in platform_list:
    input_file = f"./heatmap_data/{platform}_policy_classify.json"
    favorable_policy_file = f'./heatmap_data/{platform}_favorable_policy.json'
    unfavorable_policy_file = f'./heatmap_data/{platform}_unfavorable_policy.json'
    preprocess_policy_data(input_file=input_file,
                           favorable_policy_file=favorable_policy_file,
                           unfavorable_policy_file=unfavorable_policy_file)

for platform in platform_list:
    # 驱动力的输入文件和输出文件（经解析）
    driver_input = f'./heatmap_data/{platform}_driver.json'
    driver_output = f'./heatmap_data/{platform}_driver_parse.json'
    parse_driver_data(driver_input, driver_output)
    for policy_type in policy_type_list:
        # 政策的输入文件和输出文件（经解析）
        policy_input = f'./heatmap_data/{platform}_{policy_type}.json'
        policy_output = f'./heatmap_data/{platform}_{policy_type}_parse.json'
        parse_policy_data(policy_input, policy_output)

fundamental_driver_category_list.append("自身发展驱动力")
method_category_list.append("适应新的技术和服务需求")
external_policy_category_list.append("其它影响因素")
platform_measure_category_list.append("适应性举措与规定")

base_info_files = []
driver_files = []
favorable_policy_files = []
unfavorable_policy_files = []
# 拼接文件
for platform in platform_list:
    if platform != "iOS":
        base_info_files.append(f'./heatmap_data/{platform}_base_info.json')
    driver_files.append(f'./heatmap_data/{platform}_driver_parse.json')
    favorable_policy_files.append(f'./heatmap_data/{platform}_favorable_policy_parse.json')
    unfavorable_policy_files.append(f'./heatmap_data/{platform}_unfavorable_policy_parse.json')

base_info_file = f'./heatmap_data/base_info.json'
driver_file = f'./heatmap_data/driver.json'

# 基础数据
merge_files(base_info_files, base_info_file)
# 驱动力
merge_files(driver_files, driver_file)
# 有利政策
merge_files(favorable_policy_files, './heatmap_data/favorable_policy.json')
# 不利政策
merge_files(unfavorable_policy_files, './heatmap_data/unfavorable_policy.json')

bf_minor_heatmap_data = create_minor_heatmap_data_by_double_files(
    Y_input_file=base_info_file,
    X_input_file=driver_file,
    Y_field="business_domain_class",
    X_field="fundamental_driver_category",
    Y_category_list=business_category_list,
    X_category_list=fundamental_driver_category_list
)
generate_heatmap(
    heatmap_data=bf_minor_heatmap_data,
    output_file=f"./result/heatmap_result/业务-驱动_小类.svg",
    Y_name="主导者业务领域",
    X_name="本源驱动力",
    Y_category_list=business_category_list,
    X_category_list=fundamental_driver_category_list,
    y=10
)

bf_major_heatmap_data = create_major_heatmap_data(
    minor_heatmap_data=bf_minor_heatmap_data,
    Y_category_dictionary=business_category_dictionary,
    X_category_dictionary=fundamental_driver_category_dictionary
)
generate_heatmap(
    heatmap_data=bf_major_heatmap_data,
    output_file=f"./result/heatmap_result/业务-驱动_大类.svg",
    Y_name="主导者业务领域",
    X_name="本源驱动力",
    Y_category_list=business_category_dictionary.keys(),
    X_category_list=fundamental_driver_category_dictionary.keys(),
    y=10
)

mt_minor_heatmap_data = create_minor_heatmap_data_by_double_files(
    Y_input_file=driver_file,
    X_input_file=base_info_file,
    Y_field="method_category",
    X_field="tech_domain_class",
    Y_category_list=method_category_list,
    X_category_list=technology_category_list
)
generate_heatmap(
    heatmap_data=mt_minor_heatmap_data,
    output_file=f"./result/heatmap_result/途径-技术_小类.svg",
    Y_name="技术和功能研发动力",
    X_name="三方库/框架技术领域",
    Y_category_list=method_category_list,
    X_category_list=technology_category_list,
    x=10
)
mt_major_heatmap_data = create_major_heatmap_data(
    minor_heatmap_data=mt_minor_heatmap_data,
    Y_category_dictionary=method_category_dictionary,
    X_category_dictionary=technology_category_dictionary
)
generate_heatmap(
    heatmap_data=mt_major_heatmap_data,
    output_file=f"./result/heatmap_result/途径-技术_大类.svg",
    Y_name="技术和功能研发动力",
    X_name="三方库/框架技术领域",
    Y_category_list=method_category_dictionary.keys(),
    X_category_list=technology_category_dictionary.keys(),
    x=10
)

bt_minor_heatmap_data = create_minor_heatmap_data_by_single_file(
    input_file=base_info_file,
    Y_field="business_domain_class",
    X_field="tech_domain_class",
    Y_category_list=business_category_list,
    X_category_list=technology_category_list
)
generate_heatmap(
    heatmap_data=bt_minor_heatmap_data,
    output_file=f"./result/heatmap_result/业务-技术.svg",
    Y_name="主导者业务领域",
    X_name="三方库/框架技术领域",
    Y_category_list=business_category_list,
    X_category_list=technology_category_list,
    y=10,
    x=10
)

fm_minor_heatmap_data = create_minor_heatmap_data_by_single_file(
    input_file=driver_file,
    Y_field="fundamental_driver_category",
    X_field="method_category",
    Y_category_list=fundamental_driver_category_list,
    X_category_list=method_category_list
)
generate_heatmap(
    heatmap_data=fm_minor_heatmap_data,
    output_file=f"./result/heatmap_result/驱动-途径_小类.svg",
    Y_name="本源驱动力",
    X_name="技术和功能研发动力",
    Y_category_list=fundamental_driver_category_list,
    X_category_list=method_category_list
)
fm_major_heatmap_data = create_major_heatmap_data(
    minor_heatmap_data=fm_minor_heatmap_data,
    Y_category_dictionary=fundamental_driver_category_dictionary,
    X_category_dictionary=method_category_dictionary
)
generate_heatmap(
    heatmap_data=fm_major_heatmap_data,
    output_file=f"./result/heatmap_result/驱动-途径_大类.svg",
    Y_name="本源驱动力",
    X_name="技术和功能研发动力",
    Y_category_list=fundamental_driver_category_dictionary.keys(),
    X_category_list=method_category_dictionary.keys()
)

for policy_type in policy_type_list:
    policy_file = f'./heatmap_data/{policy_type}.json'
    policy_type_word = '有利政策' if policy_type == 'favorable_policy' else '不利政策'
    ep_minor_heatmap_data = create_minor_heatmap_data_by_single_file(
        input_file=policy_file,
        Y_field="external_policy_category",
        X_field="platform_measure_category",
        Y_category_list=external_policy_category_list,
        X_category_list=platform_measure_category_list
    )
    generate_heatmap(
        heatmap_data=ep_minor_heatmap_data,
        output_file=f"./result/heatmap_result/政策-平台_{policy_type_word}-小类.svg",
        Y_name="外部政策与环境",
        X_name="系统平台举措与规定",
        Y_category_list=external_policy_category_list,
        X_category_list=platform_measure_category_list
    )

    ep_major_heatmap_data = create_major_heatmap_data(
        minor_heatmap_data=ep_minor_heatmap_data,
        Y_category_dictionary=external_policy_category_dictionary,
        X_category_dictionary=platform_measure_category_dictionary
    )
    generate_heatmap(
        heatmap_data=ep_major_heatmap_data,
        output_file=f"./result/heatmap_result/政策-平台_{policy_type_word}-大类.svg",
        Y_name="外部政策与环境",
        X_name="系统平台举措与规定",
        Y_category_list=external_policy_category_dictionary.keys(),
        X_category_list=platform_measure_category_dictionary.keys()
    )

    ef_minor_heatmap_data = create_minor_heatmap_data_by_double_files(
        Y_input_file=policy_file,
        X_input_file=driver_file,
        Y_field="external_policy_category",
        X_field="fundamental_driver_category",
        Y_category_list=external_policy_category_list,
        X_category_list=fundamental_driver_category_list
    )

    generate_heatmap(
        heatmap_data=ef_minor_heatmap_data,
        output_file=f"./result/heatmap_result/政策-驱动_{policy_type_word}-小类.svg",
        Y_name="外部政策与环境",
        X_name="本源驱动力",
        Y_category_list=external_policy_category_list,
        X_category_list=fundamental_driver_category_list
    )

    ef_major_heatmap_data = create_major_heatmap_data(
        minor_heatmap_data=ef_minor_heatmap_data,
        Y_category_dictionary=external_policy_category_dictionary,
        X_category_dictionary=fundamental_driver_category_dictionary
    )

    generate_heatmap(
        heatmap_data=ef_major_heatmap_data,
        output_file=f"./result/heatmap_result/政策-驱动_{policy_type_word}-大类.svg",
        Y_name="外部政策与环境",
        X_name="本源驱动力",
        Y_category_list=external_policy_category_dictionary.keys(),
        X_category_list=fundamental_driver_category_dictionary.keys()
    )

    pf_minor_heatmap_data = create_minor_heatmap_data_by_double_files(
        Y_input_file=policy_file,
        X_input_file=driver_file,
        Y_field="platform_measure_category",
        X_field="fundamental_driver_category",
        Y_category_list=platform_measure_category_list,
        X_category_list=fundamental_driver_category_list
    )

    generate_heatmap(
        heatmap_data=pf_minor_heatmap_data,
        output_file=f"./result/heatmap_result/平台-驱动_{policy_type_word}-小类.svg",
        Y_name="系统平台举措与规定",
        X_name="本源驱动力",
        Y_category_list=platform_measure_category_list,
        X_category_list=fundamental_driver_category_list
    )

    pf_major_heatmap_data = create_major_heatmap_data(
        minor_heatmap_data=pf_minor_heatmap_data,
        Y_category_dictionary=platform_measure_category_dictionary,
        X_category_dictionary=fundamental_driver_category_dictionary
    )

    generate_heatmap(
        heatmap_data=pf_major_heatmap_data,
        output_file=f"./result/heatmap_result/平台-驱动_{policy_type_word}-大类.svg",
        Y_name="系统平台举措与规定",
        X_name="本源驱动力",
        Y_category_list=platform_measure_category_dictionary.keys(),
        X_category_list=fundamental_driver_category_dictionary.keys()
    )

    em_minor_heatmap_data = create_minor_heatmap_data_by_double_files(
        Y_input_file=policy_file,
        X_input_file=driver_file,
        Y_field="external_policy_category",
        X_field="method_category",
        Y_category_list=external_policy_category_list,
        X_category_list=method_category_list
    )

    generate_heatmap(
        heatmap_data=em_minor_heatmap_data,
        output_file=f"./result/heatmap_result/政策-途径_{policy_type_word}-小类.svg",
        Y_name="外部政策与环境",
        X_name="技术和功能研发动力",
        Y_category_list=external_policy_category_list,
        X_category_list=method_category_list
    )

    em_major_heatmap_data = create_major_heatmap_data(
        minor_heatmap_data=em_minor_heatmap_data,
        Y_category_dictionary=external_policy_category_dictionary,
        X_category_dictionary=method_category_dictionary
    )

    generate_heatmap(
        heatmap_data=em_major_heatmap_data,
        output_file=f"./result/heatmap_result/政策-途径_{policy_type_word}-大类.svg",
        Y_name="外部政策与环境",
        X_name="技术和功能研发动力",
        Y_category_list=external_policy_category_dictionary.keys(),
        X_category_list=method_category_dictionary.keys()
    )

    pm_minor_heatmap_data = create_minor_heatmap_data_by_double_files(
        Y_input_file=policy_file,
        X_input_file=driver_file,
        Y_field="platform_measure_category",
        X_field="method_category",
        Y_category_list=platform_measure_category_list,
        X_category_list=method_category_list
    )

    generate_heatmap(
        heatmap_data=pm_minor_heatmap_data,
        output_file=f"./result/heatmap_result/平台-途径_{policy_type_word}-小类.svg",
        Y_name="系统平台举措与规定",
        X_name="技术和功能研发动力",
        Y_category_list=platform_measure_category_list,
        X_category_list=method_category_list
    )

    pm_major_heatmap_data = create_major_heatmap_data(
        minor_heatmap_data=pm_minor_heatmap_data,
        Y_category_dictionary=platform_measure_category_dictionary,
        X_category_dictionary=method_category_dictionary
    )

    generate_heatmap(
        heatmap_data=pm_major_heatmap_data,
        output_file=f"./result/heatmap_result/平台-途径_{policy_type_word}-大类.svg",
        Y_name="系统平台举措与规定",
        X_name="技术和功能研发动力",
        Y_category_list=platform_measure_category_dictionary.keys(),
        X_category_list=method_category_dictionary.keys()
    )
