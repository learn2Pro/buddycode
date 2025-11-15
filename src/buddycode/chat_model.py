import os
from langchain_openai import ChatOpenAI

def init_chat_model():
    """
    Initialize the ChatOpenAI model for Doubao (豆包).

    Environment variables (optional):
    - ARK_API_KEY: ByteDance ARK API key (defaults to hardcoded value for local dev)
    - ARK_BASE_URL: API base URL (defaults to Beijing endpoint)
    - ARK_MODEL: Model endpoint ID (defaults to ep-20251010103732-rchjc)
    """
    # Get configuration from environment or use defaults
    api_key = os.getenv("ARK_API_KEY")
    base_url = os.getenv("ARK_BASE_URL")
    model = os.getenv("ARK_MODEL")

    return ChatOpenAI(
        model=model,
        base_url=base_url,
        api_key=api_key,
        temperature=0,
        max_tokens=8 * 1024,
        extra_body={
            "thinking": {
                "type": "disabled"  # 如果需要推理，这里可以设置为 "auto"
            }
        }
    )


if __name__ == "__main__":
    chat_model = init_chat_model()
    for chunk in chat_model.stream("你好"):
        print(chunk.content, end="", flush=True)
    print()  # New line at the end
