import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "resume_rules.json")
REFERENCE_PATH = os.path.join(os.path.dirname(__file__), "reference", "good_resume_example.md")
LEARNING_PATH = os.path.join(os.path.dirname(__file__), "reference", "learning_resources.md")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_reference():
    with open(REFERENCE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def load_learning():
    with open(LEARNING_PATH, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt(resume, jd):
    config = load_config()
    reference = load_reference()
    learning = load_learning()

    sections_text = ""
    for section in config["sections"]:
        sections_text += f"\n【{section['name']}】\n"
        sections_text += f"必须包含：{', '.join(section['required'])}\n"
        if section.get("optional"):
            sections_text += f"可选：{', '.join(section['optional'])}\n"
        if section.get("rules"):
            for rule in section["rules"]:
                sections_text += f"- {rule}\n"

    problems_text = "\n".join([f"- {p}" for p in config["problems_to_check"]])

    prompt = f"""你是一位资深简历优化师，专门服务{config['target_user']}。

【最高优先级规则 - 学习路径资源约束】
- 你的 learningPath 字段里的 resources，只能从下方【学习资源池】里选。
- 资源池里没有的课程、项目、网站，一律不许写。
- 如果资源池里没有匹配的资源，resources 写空数组 []，不要用其他方向的资源凑。
- 如果 resources 为空，在 suggestion 里追加一句：搜索建议：在B站搜"xxx"，在牛客网搜"xxx"。
- 不要编造任何课程名、UP主名、网站名。只允许从资源池里复制。

【参考案例】
以下是一份优秀的简历案例，请参考它的表达方式和结构：
{reference}

【简历各模块要求】
{sections_text}

【需要检查的问题】
{problems_text}

【学习资源池】
以下是真实存在的学习资源，只能从里面选，不要自己编造：
{learning}

【目标岗位】
{jd if jd else "未提供"}

【简历原文】
{resume}

【输出要求】
请严格按照以下JSON格式输出，不要输出任何其他内容：

{{
  "positionAlert": "岗位校准提醒。如果目标岗位的要求明显高于用户当前经历（比如本科在读对标架构师、应届对标5年经验岗位），在这里写一句提醒，建议调整目标岗位。如果匹配，写空字符串。",
  "matchScore": 匹配度数字（0-100）,
  "problems": [
    {{"title": "问题标题", "detail": "问题详细说明"}}
  ],
  "suggestions": [
    {{"problem": "对应问题", "advice": "具体建议"}}
  ],
  "optimizedResume": "优化后的简历全文",
  "diff": [
    {{"original": "原文", "optimized": "改后", "reason": "修改原因", "type": "修改/补充"}}
  ],
  "pendingItems": [
    "需要用户补充的信息1",
    "需要用户补充的信息2"
  ],
  "learningPath": [
    {{
      "gap": "能力差距描述",
      "suggestion": "建议怎么补。如果资源池里没有匹配的资源，在这里加上搜索建议。",
      "resources": [
        {{"type": "课程", "name": "资源名称（只能从资源池复制）", "note": "重点看什么"}}
      ]
    }}
  ]
}}

【硬性规则】
1. 只输出JSON，不要输出任何解释、说明、markdown符号。
2. 不要用```json```包裹。
3. 确保JSON格式合法，能被Python的json.loads()解析。
4. 只改写原文已有的事实，不新增原文没有的学历、公司、项目、证书、时间。

【角色约束 - 必须严格遵守】
5. 如果原文是"参与""跟随""协助""配合"，不要改成"独立完成""主导""负责"。
6. 保留原文的角色定位，只优化表达方式，不升级角色。

【自我评价约束】
7. 不要写"持续研究""注重培养""不断学习""努力提升"这类没有具体指向的空话。
8. 自我评价要么挂到具体经历上，要么删掉。

【量化数据约束】
9. 需要量化但原文没数字的地方，用[请填写真实数字]标记。
10. 所有[请填写真实数字]的地方，都要在pendingItems里列出来，格式："项目名/模块名：需要补充什么"。

【岗位校准】
11. 如果目标岗位的要求明显高于用户当前经历，在positionAlert里写一句提醒，建议调整目标岗位。
12. 如果匹配，positionAlert写空字符串。

【学习路径约束 - 必须严格遵守】
13. learningPath 里的 resources，只能从【学习资源池】里选。资源池里没有的，一律不许写。
14. 如果资源池里没有匹配的资源，resources 写空数组 []，不要用其他方向的资源凑。
15. 如果 resources 为空，在 suggestion 后面追加一行：搜索建议：在B站搜"xxx"，在牛客网搜"xxx"，在Kaggle搜"xxx"。
16. learningPath 只针对"用户和目标岗位之间最核心的1-3个差距"给出建议，不要罗列一堆。
17. 不要编造任何课程名、UP主名、网站名。只允许从资源池里复制。
"""
    return prompt