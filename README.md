# Python小工具

## 安装项目依赖包

1. 基础环境：Python3.12+

2. 安装UV
```shell
pip install uv
set UV_INDEX=https://mirrors.aliyun.com/pypi/simple
```

3. 安装Python依赖包
```shell
uv sync --python 3.12 --all-extras
```

4. 切换到本地环境(.venv)，请安装whl包
```shell
cd .venv/Scripts
activate
```

## 模型加载

1. 在项目根目录下新建`.env`文件，并添加以下内容
```text
API_KEY=your_api_key
BASE_URL=model_base_url
```

2. 加载模型  
如果需要调用模型，请直接添加以下代码（注意需要加载项目根目录到环境的path中），不需要额外的配置。
```python
import os
from dotenv import load_dotenv, find_dotenv

loaded = load_dotenv(find_dotenv(), override=True)
# 从环境变量中获取 OpenAI API Key 或者直接赋值
API_KEY = os.getenv("API_KEY")

# 如果您使用的是官方 API，就直接用 https://api.siliconflow.cn/v1 就行。
BASE_URL = "https://api.siliconflow.cn/v1"
```
