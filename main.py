# ========== 第一步：导入所有依赖包 ==========
from dotenv import load_dotenv
import os
from openai import OpenAI
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import time
import random

# ========== 第二步：导入本地模块 ==========
from database import engine, get_db, Base, SessionModel, MessageModel, KnowledgeModel

# ========== 第三步：加载环境变量 ==========
load_dotenv()

# ========== 第四步：初始化大模型客户端 ==========
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "sk-2c5421bcfb744a5ca90a77a2f272977e"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
)

# ========== 第五步：初始化数据库 ==========
Base.metadata.create_all(bind=engine)

# ========== 第六步：创建FastAPI应用 ==========
app = FastAPI(title="大疆无人机AI客服系统", version="3.0")

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== 数据模型定义 ==========
class ChatRequest(BaseModel):
    message: str
    session_id: str


class ChatResponse(BaseModel):
    reply: str
    session_id: str


class KnowledgeCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = "通用"


# ========== 智能问答核心逻辑 ==========
def get_ai_response(user_msg: str, db: Session) -> str:
    msg = user_msg.lower()

    # 1. 无关问题直接拦截
    UNRELATED = ["小米", "华为", "苹果", "手机", "汽车", "电脑", "冰箱", "电视", "oppo", "vivo"]
    for w in UNRELATED:
        if w in user_msg:
            return "抱歉，我是大疆无人机专属客服，只回答大疆无人机相关问题哦~"

    # 2. 2026年新款产品
    if "2026" in msg or "新款" in msg or "mini 5" in msg or "air 3s" in msg or "mavic 4" in msg:
        return """✅ 2026年大疆全系新款无人机：

🌟 【DJI Mini 5 Pro】入门旗舰
• 价格：标准版5288元 | 畅飞套装6588元
• 重量：249g（全国免实名登记）
• 续航：47分钟超长续航
• 相机：1英寸CMOS传感器，5.3K/60fps
• 避障：全向避障Pro
• 适合：新手、旅行、日常航拍

🚁 【DJI Air 3S】中端旗舰
• 价格：标准版7688元 | 畅飞套装9288元
• 重量：595g
• 续航：48分钟
• 相机：双主摄升级（广角+中焦）
• 亮点：夜景增强、AI跟拍2.0
• 适合：自媒体、专业创作者

🎥 【DJI Mavic 4】专业旗舰
• 价格：标准版12888元
• 重量：920g
• 续航：50分钟
• 相机：哈苏2代、8K/30fps视频
• 亮点：全向避障Max、夜航模式
• 适合：专业影视、商业航拍

💡 新手首选：Mini 5 Pro（免登记+全向避障）"""

    # 3. 产品推荐与选购
    if "推荐" in msg or "买哪款" in msg or "新手" in msg or "怎么选" in msg:
        return """🎯 大疆无人机选购指南：

💰 【预算3000-5000元】→ Mini 4K / Mini 5 Pro
• Mini 4K：3288元，入门首选，249g免登记
• Mini 5 Pro：5288元，全向避障，新手必备

💰 【预算6000-9000元】→ Air 3 / Air 3S
• Air 3：6988元，双主摄，创作者首选
• Air 3S：7688元，2026新款，夜景更强

💰 【预算10000元以上】→ Mavic 3 / Mavic 4
• Mavic 3 Classic：9288元，哈苏相机
• Mavic 4：12888元，2026专业旗舰

✅ 纯新手闭眼入：Mini 5 Pro（249g免登记+全向避障）"""

    # 4. 价格查询
    if "多少钱" in msg or "价格" in msg:
        if "mini 5 pro" in msg or "mini5pro" in msg:
            return "Mini 5 Pro 标准版5288元，畅飞套装6588元。"
        if "mini 4 pro" in msg or "mini4pro" in msg:
            return "Mini 4 Pro 标准版4788元，畅飞套装5988元。"
        if "mini 4k" in msg or "mini4k" in msg:
            return "Mini 4K 标准版3288元，入门首选。"
        if "air 3s" in msg:
            return "Air 3S 标准版7688元，畅飞套装9288元。"
        if "air 3" in msg:
            return "Air 3 标准版6988元，畅飞套装8388元。"
        if "mavic 4" in msg:
            return "Mavic 4 标准版12888元，专业旗舰。"
        if "mavic 3" in msg:
            return "Mavic 3 Classic 标准版9288元，哈苏相机专业画质。"

    # 5. 实名登记与法规
    if "实名" in msg or "登记" in msg or "禁飞" in msg or "法规" in msg:
        return """📋 无人机飞行法规：

✅ 实名登记：
• 重量≥250g必须在民航局实名登记
• Mini系列（249g）全国多数地区免登记
• 登记后粘贴二维码在机身上

🚫 禁飞区域：
• 机场周边5公里内绝对禁飞
• 军事区、政府机关、人群密集区
• 北京六环内、上海内环等核心区域

⚠️ 飞行注意：
• 高度不超过120米，视距内飞行
• 远离高压线、基站、建筑物
• 电量剩余30%立即返航"""

    # 6. 售后与保修
    if "保修" in msg or "售后" in msg or "炸机" in msg or "摔坏" in msg or "随心换" in msg:
        return """🛠️ 大疆售后政策：

📋 保修范围：
• 主机：保修期1年
• 电池、遥控器：保修期6个月
• 人为损坏、进水、炸机不在免费保修范围内

💥 炸机处理：
1. 保持现场，不要强行开机
2. DJI APP内申请「意外保障」
3. 购买随心换可享低价置换

🔄 DJI Care随心换：
• 1年内享2次低价置换
• 覆盖炸机、进水、丢失
• 建议新手必买！"""

    # 7. 电池与续航
    if "电池" in msg or "续航" in msg or "充电" in msg:
        return """🔋 电池使用指南：

⏱️ 各机型续航：
• Mini 5 Pro：47分钟
• Mini 4 Pro：45分钟
• Air 3S：48分钟
• Mavic 4：50分钟

💡 使用建议：
1. 飞行前检查电池触点是否氧化
2. 低温环境续航下降30%-50%，注意保暖
3. 剩余30%电量建议立即返航
4. 长期存放保持50%电量，每月充放一次"""

    # 8. 安全飞行
    if "安全" in msg or "注意" in msg or "雨天" in msg or "防水" in msg or "室内" in msg:
        return """⚠️ 安全飞行重要提醒：

🌧️ 防水问题：
• 大疆消费级无人机均不防水！
• 严禁雨天、雾天飞行
• 进水损坏不在保修范围内

🏠 室内飞行：
• 无GPS信号，容易漂移
• 新手不建议室内飞行
• 必须开启视觉定位

🚨 避障失效场景：
• 纯黑环境、无纹理墙面
• 细电线、树枝等细小物体
• 强光逆光环境
• 水面、镜面反射"""

    # 9. 大模型兜底
    try:
        system_prompt = """你是大疆官方专业客服「疆小助」，专业、友好、耐心。
        只回答大疆无人机相关问题，专业准确，重点用表情标注，分点清晰。"""

        response = client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return """抱歉，我暂时无法回答这个问题。

您可以问：
• 新手推荐哪款？
• Mini 5 Pro多少钱？
• 需要实名登记吗？
• 炸机了怎么办？"""


# ========== API 接口 ==========
@app.post("/api/chat", response_model=ChatResponse, summary="处理用户聊天请求")
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    ai_reply = get_ai_response(request.message, db)
    return {"reply": ai_reply, "session_id": request.session_id}


@app.get("/health", summary="健康检查")
async def health_check():
    return {"status": "ok", "timestamp": time.time()}


@app.post("/api/knowledge/add", summary="添加一条知识")
async def add_knowledge(knowledge: KnowledgeCreate, db: Session = Depends(get_db)):
    new_knowledge = KnowledgeModel(
        question=knowledge.question,
        answer=knowledge.answer,
        category=knowledge.category
    )
    db.add(new_knowledge)
    db.commit()
    db.refresh(new_knowledge)
    return {"message": "知识添加成功", "id": new_knowledge.id}


@app.get("/api/knowledge/list", summary="获取所有知识列表")
async def list_knowledge(db: Session = Depends(get_db)):
    items = db.query(KnowledgeModel).all()
    return [{"id": item.id, "question": item.question, "answer": item.answer} for item in items]


# ========== 启动服务器 ==========
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)