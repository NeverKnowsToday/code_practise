import re

# def is_markdown(text):
#     # 简单的正则表达式判断是否包含 Markdown 特征
#     markdown_pattern = r'(\*\*|\*|__|_|`|#|\-|>|!|\[.*\]\(.*\))'
#     return bool(re.search(markdown_pattern, text))

# def convert_markdown_to_text(text):
#     # 去除 Markdown 格式，保留纯文本
#     text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # 去掉粗体
#     text = re.sub(r'\*(.*?)\*', r'\1', text)      # 去掉斜体
#     text = re.sub(r'__(.*?)__', r'\1', text)     # 去掉下划线
#     text = re.sub(r'_(.*?)_', r'\1', text)        # 去掉下划线
#     text = re.sub(r'`(.*?)`', r'\1', text)        # 去掉代码
#     text = re.sub(r'#+\s*', '', text)             # 去掉标题
#     text = re.sub(r'\n+', '\n', text)             # 去掉多余换行
#     return text.strip()

def remove_sql_format(text):
    # 去掉 SQL 代码块
    return re.sub(r'```sql\n(.*?)\n```', r'\1', text, flags=re.DOTALL).strip()

# 输入字符串
input_string = """```sql
CREATE TABLE Classification_and_grading_results2 (
   字段名 VARCHAR(255),
   分类 VARCHAR(255),
   分级 VARCHAR(255),
   字段名释义 VARCHAR(255),
   数据安全保护措施建议 VARCHAR(255)
);
...
```"""

# # 判断并转换
# if is_markdown(input_string):
#     output = convert_markdown_to_text(input_string)
# else:
#     output = input_string

# print(output)

if '```sql' in input_string:
    # 如果包含 SQL 格式，去掉 SQL 格式
    output = remove_sql_format(input_string)
    print("1",output)
else:
    # 如果没有 SQL 格式，直接返回原文本
    output =  input_string.strip()
    print("2",output)
