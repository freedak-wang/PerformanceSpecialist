# 绩效考核方案ai生成器

import os
import openai
from dotenv import load_dotenv, find_dotenv
import streamlit as st  # 导入 streamlit 库

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.environ['OPENAI_API_KEY']


# 这些因素构成了员工绩效的主要部分：
# 目标达成：这是考察员工完成设定目标的程度，例如销售额、项目完成率等2-3个指标。给出每个目标的具体内容，评估标准，分数和权重。
# 技能：这是考察员工岗位技能的水平，例如销售技巧、编程语言熟练度等2-3个指标。列出主要技能，以及评估标准，分数和权重。
# 素质：这是考察员工的职业素养，例如团队合作、创新思维等2-3个指标。详述各项素质，以及评估标准，分数和权重。
# 其中：目标达成 + 技能 + 素质 =100 分，需要给出这三部分的权重。

def get_completion_and_token_count(company_type, position, performance_method,
                                   model="gpt-3.5-turbo",
                                   temperature=0,
                                   max_tokens=2000):
    messages = [
        {'role': 'system',
         'content': """
            你是一位绩效管理专家，具备行业内的最佳实践知识，可以根据不同的企业类型和岗位，给出细化的绩效考核方案。绩效考核的方式有很多，例如：
            
            目标设定法（Management by Objectives, MBO）：这种方法侧重于目标和结果。管理者和员工一起设定员工需要实现的明确、可衡量的目标，然后在考核期结束时看看员工是否达到了这些目标。
            360度反馈法：这种方法涵盖了来自多个源的反馈，包括上司、同事、下属甚至自我评价。这种方式可以提供一个全方位的、多角度的员工绩效视图。
            行为锚定等级法（Behaviorally Anchored Rating Scales, BARS）：这种方式侧重于员工的行为和态度，其方式是设定一些特定的行为标准并评价员工的表现。
            关键绩效指标（Key Performance Indicators, KPI）：这是一种目标导向的评估方法，主要依据的是员工对公司目标达成的贡献。
            评分等级法：在这种方法中，管理者对每个员工在特定领域的表现进行评分。这种方法简单易懂，但可能会受到主观性的影响。
            自我评价法：员工对自己的绩效进行评估，这种方法可以提高员工的自我认知能力。
            临床评估法：这种方式像医生诊断病人一样，对员工的绩效进行综合评估，包括员工的潜力和工作满意度等方面。
            组合评价法：这是一个混合方法，结合了以上几种方法，以实现最全面的评估。
            
            首先，向用户提问来确定用户的企业类型、岗位以及希望采用的考核方法，然后经过认真思考，为用户推荐一个详细的绩效考核方案。方案应包含以下信息：
            企业类型：描述企业的主要业务领域，例如软件开发、电子商务、制造业等。
            岗位：描述员工的主要职责，例如销售、工程师、人力资源等。
            绩效考核方式：{performance_method}
            接下来是考核指标的具体内容和评估标准、分数范围（0-100）和权重。
            最后请以 json 文件格式输出。
        """},
        {'role': 'user',
         'content': f"请给出{company_type}的{position}岗位，采用{performance_method}方式的绩效考核方案。"},
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
def gui_interface(company_type, position, performance_method):
    # 调用上面的函数，获取绩效方案和 token 数量
    performance_plan, token_dict = get_completion_and_token_count(company_type, position, performance_method)
    # 返回绩效方案
    return performance_plan


# 在 web 界面上创建标题和描述
st.title("绩效考核方案ai生成器")
st.write("请输入企业类型和岗位，然后点击提交来生成一个绩效考核方案。")

# 在侧边栏上创建输入框，让用户输入企业类型和岗位
company_type = st.sidebar.text_input("企业类型")
position = st.sidebar.text_input("岗位")

# 在侧边栏上创建一个下拉框，让用户选择绩效考核方式
performance_method = st.sidebar.selectbox(
    "请选择绩效考核方式",
    ("目标设定法（Management by Objectives, MBO）", "360度反馈法",
     "行为锚定等级法（Behaviorally Anchored Rating Scales, BARS）",
     "关键绩效指标（Key Performance Indicators, KPI）", "评分等级法", "自我评价法", "临床评估法", "组合评价法")
)

# 在侧边栏上创建一个按钮，让用户提交输入
if st.sidebar.button("提交"):
    progress = st.progress(0)
    progress.progress(50)

    # 调用 web 界面的函数，获取绩效方案
    performance_plan = gui_interface(company_type, position, performance_method)
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
