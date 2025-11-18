# PDF 转化Markdow 工具方案调研情况



[toc]



## Textin

https://docs.textin.com/xparse/parse-quickstart

支持API，需要手动post请求

解析的最大页数: 1000

### 计费方式

<img src="C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20251118172651189.png" alt="image-20251118172651189" style="zoom:25%;" />



输入：配置参数和PDF(支持本地文件或者url)[配置参数说明](https://docs.textin.com/xparse/parse-quickstart)

输出: 一个解析后的`json`响应, 里面可以获取`markdown源码`，`图片url/base64编码`, `表格元素`，`文档目录树`

### 图片元素

https://docs.textin.com/xparse/parse-getimage

对于图片处理有两种返回方式

- 传入option: `image_output_type` 为 `base64str`, 会直接返回图片编码字符串
- 传入option: `image_output_type`为`default`, 会返回图片`url`, 服务方会为解析出来的`url`保存30天 

### 表格元素

https://docs.textin.com/xparse/parse-gettable

要求：设置配置`table_flavor` 为 md 或 html

可以保存为excel 或者 json、md

### 并发请求

https://docs.textin.com/xparse/parse-max-workers

最大`2QPS`, 如果需要提升需要[咨询](https://www.textin.com/contact?type=28)



## Zamzar API

### 计费方式

<img src="C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20251117132917704.png" alt="image-20251117132917704" style="zoom:50%;" />

细节

![image-20251117133125044](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20251117133125044.png)

使用方法：

 - python 使用密钥调用API服务

API文档： https://developers.zamzar.com/docs



### 安装Python SDK

https://github.com/zamzar/zamzar-python

```
pip install --upgrade zamzar
```

### 使用

采用: `提交任务-轮询状态-下载结果 `的异步模型

转换文件代码

```python
client.convert(pdf_path, 
            target_format='md', 
            source_format='pdf', 
            options={                
                "ocr": "true"
            }).store('./').delete_all_files()
```

#### 输入

文件地址，可以是`url`

#### 输出

会将结果存储指定本地文件夹或者zamzar网站远程服务器



### 不足

- 文档不全(找不到关于转化配置`options`的描述)

- 定价不便宜
- 转化结果较差(似乎没法提取图片表格，仅文字)



## mistral-ocr(开源社区工具, 对PDF还原度较高)

找到开源项目: https://github.com/nicekate/mistral-ocr

**对pdf的还原度很高**

### 功能特点

- 使用 [Mistral AI](https://admin.mistral.ai/organization/api-keys) 的 OCR 能力处理 PDF 文件
- 自动提取文本内容并保留原始布局
- 提取并保存 PDF 中的图像
- 生成包含完整内容的 Markdown 文件
- 支持中文等多种语言



### Mistral AI OCR定价

<img src="E:\Book\实用API\PDFToMd\image-20251118203652345.png" alt="image-20251118203652345" style="zoom:50%;" />

### 使用

首先安装依赖

```
pip install mistralai flask
```



需要获取`mistral-ocr`密钥，运行工具

```
python pdf_ocr.py your_document.pdf -o custom_output_folder
```

#### 输入

pdf 路径， 保存的目标路径

#### 输出

`images`文件夹 `md`文件

 

## MinerU API

可以自己部署，可以使用官网在线 API

**需要申请才能用**

https://mineru.net/apiManage/docs

**由于不支持SDK, 只能手动异步轮询结果**

需要上传后从回调接口获取含图片和md 的压缩包(异步)

- 支持图片完整保存
- 支持批量上传
- 获取的是压缩包

### limits

- 单个文件大小不能超过 200MB,文件页数不超出 600 页
- 每个账号每天享有 2000 页最高优先级解析额度，超过 2000 页的部分优先级降低
- 因网络限制，github、aws 等国外 URL 会请求超时
- 该接口不支持文件直接上传
- header头中需要包含 Authorization 字段，格式为 Bearer + 空格 + Token

- 异步请求需要轮询
- 需要手动下载zip并解压



### 使用

采用: `提交任务-轮询状态-下载结果 `的异步模型

[详细参数说明见文档](https://mineru.net/apiManage/docs)

#### 首先提交任务

```python
import requests

token = "官网申请的api token"
url = "https://mineru.net/api/v4/extract/task"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
data = {
    "url": "https://cdn-mineru.openxlab.org.cn/demo/example.pdf",
    "model_version": "vlm"
}

res = requests.post(url,headers=header,json=data)
print(res.status_code)
print(res.json())
print(res.json()["data"])
```



#### 轮询状态

```python
import requests

token = "官网申请的api token"
url = f"https://mineru.net/api/v4/extract/task/{task_id}"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

res = requests.get(url, headers=header)
print(res.status_code)
print(res.json())
print(res.json()["data"])
```

### 获取结果

轮询时，如果任务完成会在轮询接口下给出`zip`下载链接

```
{
  "code": 0,
  "data": {
    "task_id": "47726b6e-46ca-4bb9-******",
    "state": "done",
    "full_zip_url": "https://cdn-mineru.openxlab.org.cn/pdf/018e53ad-d4f1-475d-b380-36bf24db9914.zip",
    "err_msg": ""
  },
  "msg": "ok",
  "trace_id": "c876cd60b202f2396de1f9e39a1b0172"
}
```

#### 输入

请求参数, pdf path

#### 输出

轮询后得到`zip`下载链接



## Marker

https://documentation.datalab.to/api-reference/marker

**好像暂时没法登录来进行API测试**



### 支持本地部署

```
pip install -U marker-pdf==1.3.5
```

```python
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
converter = PdfConverter(
    artifact_dict=create_model_dict(),
)
rendered = converter("/path/to/bench_pdf.pdf")
# save to disk
with open("marker-output.md", "w", encoding="utf-8") as myfile:
    myfile.write(rendered.markdown)
```



### 使用

使用方式和MinerU 有相似性

采用: `提交任务-轮询状态-下载结果 `的异步模型



```python
import requests

url = "https://www.datalab.to/api/v1/marker"

form_data = {
    'file': ('test.pdf', open('~/pdfs/test.pdf', 'rb'), 'application/pdf'),
    "force_ocr": (None, False),
    "paginate": (None, False),
    'output_format': (None, 'markdown'),
    "use_llm": (None, False),
    "strip_existing_ocr": (None, False),
    "disable_image_extraction": (None, False)
}

headers = {"X-Api-Key": "YOUR_API_KEY"}

response = requests.post(url, files=form_data, headers=headers)
data = response.json()
```

轮询

```python
import time

max_polls = 300
check_url = data["request_check_url"]

for i in range(max_polls):
    time.sleep(2)
    response = requests.get(check_url, headers=headers) # Don't forget to send the auth headers
    data = response.json()

    if data["status"] == "complete":
        break
```

### 输入

请求对象

### 输出

轮询结果的参数会包含完整的markdown列表, 图片直接返回Base64编码

```json
{
    "output_format": "markdown",
    "markdown": "...",
    "status": "complete",
    "success": True,
    "images": {...},
    "metadata": {...},
    "error": "",
    "page_count": 5
}
```



### 本地部署

• 操作流程：

1. 安装Python环境及PyTorch；

2. 执行命令：`pip install marker-pdf`；

3. 转换命令：`marker_single input.pdf output_dir --langs Chinese`；

4. 检查输出MD文件的阅读顺序和表格完整性。

- 优势：

   • 比传统工具快4倍，支持GPU加速；

   • 自动去除页眉/页脚，还原LaTeX公式。



## Docling(本地)

IBM 的 Docling 可以解析文档，并将其导出为 Markdown 或 JSON 格式，以用于 LLM 和 RAG 用例。

Docling 是开源的，并采用 MIT 许可证。

```
pip install -U docling==2.20.0
```

```python
import html
from docling.document_converter import DocumentConverter
converter = DocumentConverter()
result = converter.convert("/path/to/bench_pdf.pdf")
docling_text = result.document.export_to_markdown()
# unescape HTML entities
docling_text = html.unescape(docling_text)
# save to disk
with open("docling-output.md", "w", encoding="utf-8") as myfile:
    myfile.write(docling_text)
```



## Doc2x

https://noedgeai.github.io/pdfdeal-docs

### 定价

![image-20251118235217951](E:\Book\实用API\PDFToMd\image-20251118235217951.png)

### 使用

可以使用`SDK`, 或者命令行，首先使用python安装相关内容

```
pip install --upgrade pdfdeal
```

通过命令行可以生成文档

```
doc2x './ReAct.pdf' -k "api_key" -o './tmp/doc2x/' --unzip
```



#### 输入

PDF路径

#### 输出

会将`images` + `md`结果生成到指定文件夹

<img src="E:\Book\实用API\PDFToMd\image-20251119000355978.png" alt="image-20251119000355978" style="zoom:33%;" />

### 不足

对PDF格式的支持可能比较少，或者是工具本身的BUG, 在生成含复杂元素的期刊会出现解析错误的情况

可能是不支持扫描版PDF。



## Lightpdf

文档地址: https://lightpdf.cn/convert-api-doc

### 定价

<img src="E:\Book\实用API\PDFToMd\image-20251119000729618.png" alt="image-20251119000729618" style="zoom:33%;" />

异步执行任务

### 使用

自定义请求

```python
client = light.lightPDF(api_key=config.light_api_key)
client.convert(open('./ReAct.pdf', 'rb'), 'md').store('./light/ReAct.md')
```

### 输入

[配置参数](https://lightpdf.cn/convert-api-doc#)

### 输入

一个OSS链接需要自行下载到本地

### 不足

不支持扫描版PDF, 图像信息会被丢失,只能获取文字和表格信息



## PyMuPDF(本地)

• 特点：只能提取文本, 速度快，但无法解析表格和图片

```python
import fitz
doc = fitz.open("input.pdf")
text = [page.get_text() for page in doc]
```

还有一个LLM版本的

```
pip install -U pymupdf4llm==0.0.17
```

```python
import pymupdf4llm
import pathlib
md_text = pymupdf4llm.to_markdown("/path/to/bench_pdf.pdf")
# save to disk
pathlib.Path("output-pymudpdf4llm.md").write_bytes(md_text.encode())
```



## Pandoc

不支持PDF直接转markdown



## mathpix

**api.mathpix.com/v3/pdf** 接口支持PDF转MD, 是异步方案，没有SDK，仅API

The maximum PDF file size supported is 1 GB.

<img src="E:\Book\实用API\PDFToMd\image-20251119013143806.png" alt="image-20251119013143806" style="zoom:33%;" />

### 使用

[配置文档](https://docs.mathpix.com/#request-parameters-for-uploading-pdfs)

支持发送请求，数据流传输/轮询 的异步方案

请求发送

```python
#!/usr/bin/env python
import requests
import json

r = requests.post("https://api.mathpix.com/v3/pdf",
    json={
        "url": "https://cdn.mathpix.com/examples/cs229-notes1.pdf",
        "conversion_formats": {
            "docx": True,
            "tex.zip": True
        }
    },
    headers={
        "app_id": "APP_ID",
        "app_key": "APP_KEY",
        "Content-type": "application/json"
    }
)
print(json.dumps(r.json(), indent=4, sort_keys=True))

```



轮询状态

```
# Replace {pdf_id} with your pdf_id
curl --location --request GET 'https://api.mathpix.com/v3/converter/{pdf_id}' \
--header 'app_key: APP_KEY' \
--header 'app_id: APP_ID'
```

支持stream数据流接口

```
GET api.mathpix.com/v3/pdf/{pdf_id}/stream
```

| Field            | Type   | Description                                                  |
| ---------------- | ------ | ------------------------------------------------------------ |
| text             | string | Mathpix Markdown output                                      |
| page_idx         | number | page index from selected page range, starting at 1 and going all the way to `pdf_selected_len` |
| pdf_selected_len | number | total number of pages inside selected page range             |

### 输入

配置

```
curl --location --request POST 'https://api.mathpix.com/v3/pdf' \
--header 'app_id: APP_ID' \
--header 'app_key: APP_KEY' \
--form 'file=@"cs229-notes5.pdf"' \
--form 'options_json="{\"conversion_formats\": {\"docx\": true, \"tex.zip\": true}, \"math_inline_delimiters\": [\"$\", \"$\"], \"rm_spaces\": true}"'

```

会得到一个包含'pdf_id'的响应

### 输出

当轮询获得的状态为complete， 就可以再次发请求获取内容

支持多种格式返回

```python
import requests

pdf_id = "PDF_ID"
headers = {
  "app_key": "APP_KEY",
  "app_id": "APP_ID"
}

# get mmd response
url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".mmd"
response = requests.get(url, headers=headers)
with open(pdf_id + ".mmd", "w") as f:
    f.write(response.text)

# get docx response
url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".docx"
response = requests.get(url, headers=headers)
with open(pdf_id + ".docx", "wb") as f:
    f.write(response.content)

# get LaTeX zip file
url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".tex"
response = requests.get(url, headers=headers)
with open(pdf_id + ".tex.zip", "wb") as f:
    f.write(response.content)

# get HTML file
url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".html"
response = requests.get(url, headers=headers)
with open(pdf_id + ".html", "wb") as f:
    f.write(response.content)

# get lines data
url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".lines.json"
response = requests.get(url, headers=headers)
with open(pdf_id + ".lines.json", "wb") as f:
    f.write(response.content)

# get lines mmd json
url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".lines.mmd.json"
response = requests.get(url, headers=headers)
with open(pdf_id + ".lines.mmd.json", "wb") as f:
    f.write(response.content)

# get pptx response
url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".pptx"
response = requests.get(url, headers=headers)
with open(pdf_id + ".pptx", "wb") as f:
    f.write(response.content)

# get MMD zip file
url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".mmd.zip"
response = requests.get(url, headers=headers)
with open(pdf_id + ".mmd.zip", "wb") as f:
    f.write(response.content)

# get MD zip file
url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".md.zip"
response = requests.get(url, headers=headers)
with open(pdf_id + ".md.zip", "wb") as f:
    f.write(response.content)

# get HTML zip file
url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".html.zip"
response = requests.get(url, headers=headers)
with open(pdf_id + ".html.zip", "wb") as f:
    f.write(response.content)

```





## Unstructured.io

- 特点：功能强大, 对于数据清洗和数据分片嵌入	提供企业化解决方案。
  - 返回的是数据流， 需要**自己根据返回的数据元素进行组装出结果**

- API: 按page 收费，三种plan
  - <img src="C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20251117230136675.png" alt="image-20251117230136675" style="zoom:25%;" />



### SDK 对文档进行按元素拆解获取结果(sync)

[Python SDK](https://docs.unstructured.io/api-reference/partition/sdk-python)

可以自定义输出的内容(`json`, `md`)

通过对PDF进行分片切割，会返回分析之后的`text`、`image` `table`元素，本地按照元素进行按顺序组装

下面是ChatGPT生成的示例：

```python
import os
import base64
import io
from PIL import Image

import unstructured_client
from unstructured_client.models import operations, shared
from unstructured.staging.base import elements_from_dicts

def partition_pdf(pdf_path: str, api_key: str):
    client = unstructured_client.UnstructuredClient(api_key_auth=api_key)

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    req = operations.PartitionRequest(
        partition_parameters=shared.PartitionParameters(
            files=shared.Files(
                content=pdf_bytes,
                file_name=os.path.basename(pdf_path),
            ),
            # 使用 hi_res 策略更容易识别图片 /布局
            strategy=shared.Strategy.HI_RES,
            # 提取图片和表格块
            extract_image_block_types=["Image", "Table"],
            # 如果 PDF 很大，可以按页拆分请求 (可选)
            split_pdf_page=True,
            split_pdf_allow_failed=True,
            split_pdf_concurrency_level=10,
        )
    )

    res = client.general.partition(request=req)
    # res.elements 是一个 dict 对象列表 (每个元素是一个结构化块)
    element_dicts = res.elements or []

    # 转成 Unstructured Element 对象 (可选)
    elements = elements_from_dicts(element_dicts)
    return elements


```



```python
def element_to_markdown(el, image_dir):
    """把单个元素转换成 Markdown 片段 (string)，图片写文件，并返回 md 行。"""
    md = ""
    etype = el.type
    text = getattr(el, "text", "") or ""

    # 标题 (Title)
    if etype == "Title":
        level = el.metadata.to_dict().get("heading_level", 1) or 1
        md += "#" * level + " " + text + "\n\n"

    # 段落 /叙述文本
    elif etype in ("NarrativeText", "Paragraph"):
        md += text + "\n\n"

    # 列表项
    elif etype == "ListItem":
        md += f"- {text}\n"

    # 表格
    elif etype == "Table":
        # 这里简单处理为 code block，也可以做 Markdown 表格
        md += "\n```\n" + text + "\n```\n\n"

    # 图片
    elif etype == "Image":
        meta = el.metadata.to_dict()
        b64 = meta.get("image_base64")
        if b64:
            img_data = base64.b64decode(b64)
            filename = f"{el.element_id}.png"
            path = os.path.join(image_dir, filename)
            # 确保目录存在
            os.makedirs(image_dir, exist_ok=True)
            # 写图片
            img = Image.open(io.BytesIO(img_data))
            img.save(path)
            # Markdown 引用
            alt = meta.get("filename", "")
            md += f"![{alt}]({path})\n\n"

    else:
        # 默认 fallback
        md += text + "\n\n"

    return md

def elements_to_markdown(elements, md_path="output.md", image_dir="images"):
    md_lines = []
    for el in elements:
        md_piece = element_to_markdown(el, image_dir)
        md_lines.append(md_piece)

    with open(md_path, "w", encoding="utf-8") as f:
        f.writelines(md_lines)

    print(f"Markdown 已写入：{md_path}")
    print(f"图片文件保存在：{image_dir}")

```



### 支持自定义工作流

[工作流 SDK](https://docs.unstructured.io/api-reference/workflows/list-workflows)

**特点** : 自定义`Pipeline`, 企业级**ETL**解决方案   

- ✔ 1. **自定义工作流（Custom Workflows）执行**

- ✔ 2. **一键 Embedding（/process /embed）管线**

- ✔ 3. **自托管服务器 / unstructured-ingest / pipeline API 调用**
支持的工作流节点

- `Source` ：source节点，指定了文档源(可以是`File`, `三方数据源(比如企业数据库)`)
- `Destination`:  target节点，指定了文档输出源(可以是各种三方服务, 也可以是`企业数据库, 向量数据库`)
- `Partitioner` :  对文档进行语义分割，元素拆解
- `Enrichment`: 增强文档内容，如将文档的`image` 来进行生成描述
- `Chunker`: 对上一个节点的结果进行分块，支持按`title` `page` `character` `similarity`
- `Embed`:  一般跟在Chunker 后面， 对结果进行向量嵌入可以无缝衔接项链数据库源进行输出

![image-20251117225900016](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20251117225900016.png)



## Markitdown(需要本地部署)

https://github.com/microsoft/markitdown

需要本地部署，可以打包成MCP或者Docker工具

### 打包成MCP

[如何使用MarkItDown MCP将文档转换为Markdown？](https://www.wbolt.com/markitdown-mcp.html)





## notegpt(Web Server Only)

https://notegpt.io/pdf-to-markdown-converter

网页版工具，不提供API



## pdf2md(Web Server Only)

https://pdf2md.site/#features

网页版工具，不提供API



## FlashAI(Application Only)

https://conv.flashai.com.cn/#

本地应用程序，不提供API





