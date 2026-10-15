# 导入操作系统接口模块，主要用于读取环境变量（类似于 Java 的 System.getenv）
import os

# 导入路径处理模块，用于跨平台地拼接和获取文件绝对路径（比 Java 的 File 更现代、更好用）
from pathlib import Path

# 从 dotenv 库导入加载函数，用于读取 .env 文件中的环境变量
from dotenv import load_dotenv

# 从 LangChain 的 DeepSeek 集成包中导入聊天模型类（类似于 Spring 中注入一个特定的 Bean）
from langchain_deepseek import ChatDeepSeek


def main():
    # 1. 获取当前脚本所在目录，并拼接出 .env 文件的绝对路径
    # __file__ 是 Python 内置变量，代表当前脚本的文件名（类似于 Java 获取当前 Class 的路径）
    # .resolve() 获取绝对路径，.parent 获取父目录
    env_path = Path(__file__).resolve().parent / ".env"

    # 2. 加载 .env 文件中的配置到系统环境变量中
    # 这样后面的 os.getenv 才能读到里面的 API Key
    load_dotenv(env_path)

    # 3. 安全检查：如果环境变量中没有 DEEPSEEK_API_KEY，则直接抛出异常终止程序
    # 这是一种“快速失败（Fail-Fast）”的策略，避免后面调用接口时报错
    if not os.getenv("DEEPSEEK_API_KEY"):
        raise RuntimeError("请在项目 .env 中配置 DEEPSEEK_API_KEY")

    # 4. 初始化 DeepSeek 聊天模型实例（核心配置）
    model = ChatDeepSeek(
        # 模型名称：优先从环境变量 DEEPSEEK_MODEL 读取，如果没有则默认使用 "deepseek-flash"
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),

        # temperature=0 表示“确定性输出”，让模型尽量不随机发挥，适合做严谨的分析（范围通常是 0~1）
        temperature=0,

        # max_tokens=128 限制模型最多输出 128 个 token（防止模型废话太多或消耗过多额度）
        max_tokens=128,

        # timeout=30 请求超时时间设置为 30 秒（网络不好时 30 秒没响应就报错）
        timeout=30,

        # max_retries=0 失败后不重试（测试连通性时，失败就是失败，不浪费时间重试）
        max_retries=0,

        # extra_body 用于传递 DeepSeek API 特有的参数
        # 这里 {"thinking": {"type": "disabled"}} 表示关闭模型的“思考过程”（类似关闭思维链），直接输出结果，加快响应速度
        extra_body={"thinking": {"type": "disabled"}},
    )

    # 5. 向模型发送一条测试消息（invoke 是同步调用，类似 Java 的 RestTemplate.postForObject）
    response = model.invoke("请用一句中文说明你已收到连接测试。")

    # 6. 打印模型返回的内容
    # response 是一个 AIMessage 对象，.content 属性里才是真正的文本回复
    print(response.content)


# 7. Python 的入口判断（类似于 Java 的 public static void main(String[] args)）
# 只有当直接运行这个文件时，才会执行 main() 函数；如果被其他文件 import，则不会执行
if __name__ == "__main__":
    main()