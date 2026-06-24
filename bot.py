from openai import OpenAI
from knowledge import PRODUCTS, FAQ

# 通义千问配置
client = OpenAI(
    api_key="sk-2c5421bcfb744a5ca90a77a2f272977e",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 格式化产品信息
product_text = "\n".join([f"【{name}】\n{info}" for name, info in PRODUCTS.items()])
faq_text = "\n".join([f"Q：{item['q']}\nA：{item['a']}" for item in FAQ])

# 优化后的系统提示词
system_prompt = f"""你是大疆官方专业客服「疆小助」，专业、友好、耐心。

【2026年最新产品库】
{product_text}

【常见问题解答】
{faq_text}

回答规则：
1. ✅ 只回答大疆无人机相关的问题
2. ❌ 如果用户问手机、汽车、其他品牌等无关问题，直接回复：
   "抱歉，我是大疆无人机专属客服，只回答大疆无人机相关问题哦~"
3. 优先使用上面的产品信息和FAQ回答，保证准确
4. 回答要专业准确，不编造信息
5. 重点内容用 ✅ ⚠️ 📋 等表情标注
6. 涉及安全的问题一定要重点提醒用户
7. 语气友好，多用换行让内容清晰易读"""

print("=" * 50)
print("🤖 大疆客服疆小助已上线！（输入quit退出）")
print("=" * 50)

# 对话循环
while True:
    user_input = input("\n👤 您：")

    if user_input.lower() in ["quit", "exit", "退出"]:
        print("🤖 感谢您的咨询，再见！")
        break

    # 先做本地关键词匹配
    user_msg_lower = user_input.lower()

    # 无关问题过滤
    UNRELATED = ["小米", "华为", "苹果", "手机", "汽车", "电脑"]
    for w in UNRELATED:
        if w in user_input:
            print("\n🤖 疆小助：抱歉，我是大疆无人机专属客服，只回答大疆无人机相关问题哦~")
            continue

    # 2026新款查询
    if "2026" in user_msg_lower or "新款" in user_msg_lower or "mini 5" in user_msg_lower:
        print(
            "\n🤖 疆小助：✅ 2026年大疆全系新款无人机：\n\n🌟 【DJI Mini 5 Pro】入门旗舰\n• 价格：标准版5288元\n• 重量：249g免登记\n• 续航：47分钟\n• 相机：1英寸传感器\n\n🚁 【DJI Air 3S】中端旗舰\n• 价格：标准版7688元\n• 续航：48分钟\n• 亮点：双主摄+夜景增强\n\n🎥 【DJI Mavic 4】专业旗舰\n• 价格：标准版12888元\n• 续航：50分钟\n• 亮点：哈苏2代+8K视频")
        continue

    # 调用大模型
    try:
        response = client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        print(f"\n🤖 疆小助：{response.choices[0].message.content}")
    except Exception as e:
        print(f"\n🤖 疆小助：抱歉，服务暂时不可用，请稍后再试。错误：{str(e)}")