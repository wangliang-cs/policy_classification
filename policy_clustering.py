from llm.llm_embed import EmbedPolicy

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
    for policy_name in standard_policy_embed_dir:
        # 寻找距离最近的policy，返回其policy_name
        pass


def policy_assignment_monthly(input_policy_list: list, standard_policy_list: list) -> list:
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
        std_policy_name = xxx
        std_policy_text = xxx
        std_policy_emb = ep_model.embed_text(std_policy_text)
        standard_policy_embed_dir[std_policy_name] = std_policy_emb

    ret_list = []
    for input_policy in input_policy_list:
        input_policy_text = xxx
        std_policy_name = _assign_single_policy(input_policy_text, standard_policy_embed_dir)
        ret_list.append(std_policy_name)

    return ret_list
