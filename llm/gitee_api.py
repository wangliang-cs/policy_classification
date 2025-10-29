from openai import OpenAI
import config

API_TOKEN = config.get_config("gitee_api_key")

ds_client = OpenAI(
    base_url="https://ai.gitee.com/v1",
    api_key=API_TOKEN,
)


def get_ds_content(prompt, temperature=0.7, role_system="You are a helpful assistant"):  # not stream
    response = ds_client.chat.completions.create(
        model="DeepSeek-V3",
        stream=False,
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": role_system
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    content = response.choices[0].message.content
    return content


qw_client = OpenAI(
    base_url="https://ai.gitee.com/v1",
    api_key=API_TOKEN,
    default_headers={"X-Failover-Enabled": "true"},
)


def get_qw_content(prompt, temperature=0.7, role_system="You are a helpful assistant"):
    response = qw_client.chat.completions.create(
        model="Qwen3-32B",
        stream=False,
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": role_system
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    content = response.choices[0].message.content
    return content
