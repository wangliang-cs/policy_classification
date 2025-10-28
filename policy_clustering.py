from llm.llm_embed import EmbedPolicy
import numpy as np

ep_model = EmbedPolicy()


def _assign_single_policy(policy_text: str, standard_policy_embed_dir) -> str:
    """
    policy_text为待标准化的政策文本

    standard_policy_embed_dir为标准化的政策对应的嵌入向量字典，形如：
    {
        "标准化政策名称": float(768),
        "标准化政策名称": float(768),
        ...
    }
    """
    p_emb = ep_model.embed_text(policy_text)
    # 使用欧式距离（L2范数）寻找最近的标准化政策
    min_dist = float('inf')
    best_name = None
    for policy_name, std_emb in standard_policy_embed_dir.items():
        dist = np.linalg.norm(np.array(p_emb) - np.array(std_emb))
        if dist < min_dist:
            min_dist = dist
            best_name = policy_name
    return best_name


def policy_standardize_monthly(input_policy_list: list, standard_policy_list: list) -> list:
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
    for std_policy in standard_policy_list:
        std_policy_name = list(std_policy.keys())[0]
        std_policy_text = list(std_policy.values())[0]
        std_policy_text = f"{std_policy_name} {std_policy_text}"
        std_policy_emb = ep_model.embed_text(std_policy_text)
        standard_policy_embed_dir[std_policy_name] = std_policy_emb

    ret_list = []
    for input_policy in input_policy_list:
        input_policy_name = list(input_policy.keys())[0]
        input_policy_text = list(input_policy.values())[0]
        input_policy_text = f"{input_policy_name} {input_policy_text}"
        std_policy_name = _assign_single_policy(input_policy_text, standard_policy_embed_dir)
        ret_list.append(std_policy_name)

    return ret_list

if __name__ == "__main__":
    input_policy_list = [
        {"欧盟GPS/Galileo开放信号政策": "欧盟宣布民用Galileo信号免费并鼓励多星座接收，提升民用定位精度；osmdroid后续版本增加对GnssStatus.Callback等多星座接口的封装，使离线定位更准确。"},
        {"欧盟GDPR生效": "开发者需对地图数据收集做合规审计，部分企业因担心聚合插件可能缓存用户坐标而弃用第三方扩展，Issues中出现银行与医疗客户移除该库的反馈"},
        {"中国工信部 164 号文 IPv6 改造": "要求新上架 App 必须支持 IPv6-Only 网络。YTKNetwork 2.6.0 默认启用 NSURLSession 的 IPv6 解析，并给出“IPv6 失败-降级-IPv4”示例配置，帮助开发者快速过检。"},
        {"Google UMP + GDPR 合规框架": "Google要求2021Q2起所有欧洲流量必须使用IAB TCF 2.0合规的UMP表单；AdColony SDK 4.6迅速内置Google UMP适配器并开源TCF String解析，帮助开发者一次集成即可同时满足AdColony+AdMob的GDPR合规，提高SDK采用率。"},
        {"欧盟GDPR对开源项目合规成本提升": "GDPR要求开源库若收集IP、邮箱需披露数据流向；DKChainableAnimationKit Demo内置Firebase埋点统计崩溃，被欧洲开发者质疑合规，主导者最终移除统计代码并发布无追踪版本，增加维护负担。"},
        {"工信部《推动5G+工业互联网512工程通知》": "明确鼓励5G+工业互联网场景采用国产实时通信中间件。腾讯云随后将TIMSDK的5G QoS接口、工厂局域网穿透模块开源，获得江苏、广东多家工业SaaS订单。"},
        {"工信部要求 App 备案并规范权限调用": "备案制推动国内 App 瘦身、减少三方 SDK；ZoomImage 零网络权限、零依赖，契合合规诉求，成为对安全敏感厂商的首选。"},
        {"宽带中国战略及IPv6升级": "工信部要求新建智能终端默认支持IPv6，node-android在0.4.0版本立即加入IPv6-UDP打洞，使其在政府智慧路灯、抄表项目中中标。"},
        
    ]
    standard_policy_list = [
        {"欧盟GDPR政策": "GDPR要求开源库若收集IP、邮箱、位置等需披露数据流向"},
        {"Galileo开放信号": "Galileo开放民用卫星信号"},
        {"工信部《推动5G+工业互联网512工程通知》": "5G+工业互联网512工程通知要求5G基站支持10000个并发用户。"},
        {"工信部 164 号文 IPv6 改造": "要求新上架 App 必须支持 IPv6 网络"},
        {"工信部要求 App 备案并规范权限调用": "要求移动APP必须备案"}
    ]
    ret_list = policy_standardize_monthly(input_policy_list, standard_policy_list)
    print(ret_list)