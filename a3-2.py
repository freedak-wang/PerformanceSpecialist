import os
import openai
# from dotenv import load_dotenv, find_dotenv
import json
import streamlit as st  # 导入 streamlit 库

# _ = load_dotenv(find_dotenv())  # read local .env file

# openai.api_key = os.environ['OPENAI_API_KEY']

openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_completion_and_token_count(company_type, position,
                                   model="gpt-3.5-turbo",
                                   temperature=0,
                                   max_tokens=2000):
    messages = [
        {'role': 'system',
         'content': """
            你是一位绩效管理专家，具备行业内的最佳实践知识，可以根据不同的企业类型和岗位，给出细化的绩效考核方案。
            现在，我们将根据用户提出的企业类型和岗位，制定一份详细的绩效考核方案。方案应包含以下信息：
            企业类型：描述企业的主要业务领域，例如软件开发、电子商务、制造业等。
            岗位：描述员工的主要职责，例如销售、工程师、人力资源等。
            接下来是考核指标的具体内容和评估标准、分数范围（0-100）和权重，这些因素构成了员工绩效的主要部分：
            目标达成：这是考察员工完成设定目标的程度，例如销售额、项目完成率等2-3个指标。给出每个目标的具体内容，评估标准，分数和权重。
            技能：这是考察员工岗位技能的水平，例如销售技巧、编程语言熟练度等2-3个指标。列出主要技能，以及评估标准，分数和权重。
            素质：这是考察员工的职业素养，例如团队合作、创新思维等2-3个指标。详述各项素质，以及评估标准，分数和权重。
            其中：目标达成 + 技能 + 素质 =100 分，需要给出这三部分的权重。
            请以 json 文件格式输出。
            参考以下示例：
            {
              "企业类型": "制造业",
              "岗位": "车间主任",
              "目标达成权重": 40,
              "技能权重": 40,
              "素质权重": 20,
              "目标达成": [
                {
                  "目标内容": "提高生产效率",
                  "评估标准": "生产线稳定运行时间、产量提升率",
                  "分数范围": "0-100",
                  "权重": 50
                },
                {
                  "目标内容": "降低生产成本",
                  "评估标准": "原材料利用率、人工成本控制",
                  "分数范围": "0-100",
                  "权重": 50
                }
              ],
              "技能": [
                {
                  "技能名称": "生产管理",
                  "评估标准": "生产计划编制、生产调度能力",
                  "分数范围": "0-100",
                  "权重": 50
                },
                {
                  "技能名称": "团队管理",
                  "评估标准": "团队建设、员工培训",
                  "分数范围": "0-100",
                  "权重": 50
                }
              ],
              "素质": [
                {
                  "素质名称": "领导能力",
                  "评估标准": "决策能力、沟通能力",
                  "分数范围": "0-100",
                  "权重": 50
                },
                {
                  "素质名称": "问题解决能力",
                  "评估标准": "解决生产中的问题、危机处理能力",
                  "分数范围": "0-100",
                  "权重": 50
                }
              ]
            }
        """},
        {'role': 'user',
         'content': f"请给出{company_type}的{position}的绩效考核方案。"},
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    content = response.choices[0].message["content"]

    token_dict = {
        'prompt_tokens': response['usage']['prompt_tokens'],
        'completion_tokens': response['usage']['completion_tokens'],
        'total_tokens': response['usage']['total_tokens'],
    }

    return content, token_dict


# 创建一个 web 界面的函数
def gui_interface(company_type, position):
    # 调用上面的函数，获取绩效方案和 token 数量
    performance_plan, token_dict = get_completion_and_token_count(company_type, position)
    # 返回绩效方案
    return performance_plan


# 在 web 界面上创建标题和描述
st.title("绩效考核方案ai生成器")
st.write("请输入企业类型和岗位，然后点击提交来生成一个绩效考核方案。")

# 在侧边栏上创建输入框，让用户输入企业类型和岗位
company_type = st.sidebar.text_input("企业类型")
position = st.sidebar.text_input("岗位")

# 在侧边栏上创建一个按钮，让用户提交输入
if st.sidebar.button("提交"):
    progress = st.progress(0)
    progress.progress(50)

    # 调用 web 界面的函数，获取绩效方案
    performance_plan = gui_interface(company_type, position)
    progress.progress(100)

    # 在主页上显示绩效方案
    st.json(performance_plan)

    # 保存结果到 "绩效方案.json" 文件
    with open('绩效方案.json', 'a', encoding='utf-8') as f:
        f.write(performance_plan + ",\n")

    # 读取文件的内容
    with open('绩效方案.json', 'r', encoding='utf-8') as f:
        file_content = f.read()

    # 提供一个下载按钮，让用户下载 "绩效方案.json" 文件
    st.download_button("下载绩效方案", file_content, file_name='绩效方案.json', mime='application/json')
