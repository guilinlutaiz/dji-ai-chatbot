// 会话ID
const SESSION_ID = "dji_session_" + Date.now();

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    console.log("✅ 大疆聊天机器人加载完成！");

    // 获取元素（你的HTML里的id，完美匹配）
    const sendBtn = document.getElementById('sendBtn');
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');
    const closeChat = document.getElementById('closeChat');
    const chatPopup = document.getElementById('chatPopup');

    // 关闭聊天窗口
    closeChat.addEventListener('click', function() {
        chatPopup.style.display = 'none';
    });

    // 发送按钮点击
    sendBtn.addEventListener('click', sendMessage);

    // 回车发送
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // 欢迎消息
    addMessage("您好！我是大疆客服疆小助 🤖\n请问有什么可以帮您的？", false);
});

// 添加消息到聊天窗口
function addMessage(content, isUser = false) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = isUser ? 'message user' : 'message ai';

    messageDiv.innerHTML = `
        <div class="avatar">${isUser ? '👤' : '🤖'}</div>
        <div class="message-bubble">${content.replace(/\n/g, '<br>')}</div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 发送消息主函数
async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const message = userInput.value.trim();

    if (!message) return;

    // 1. 显示用户消息
    addMessage(message, true);
    userInput.value = '';

    // 2. 禁用按钮
    sendBtn.disabled = true;

    // 3. 显示"正在思考"
    addMessage("正在思考中...", false);

    try {
        // 4. 调用你的后端API（完美匹配你的后端接口）
        const response = await axios.post("http://localhost:8000/api/chat", {
            message: message,
            session_id: SESSION_ID
        });

        // 5. 删除"正在思考"，替换成真实回复
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.removeChild(chatMessages.lastElementChild);
        addMessage(response.data.reply, false);

    } catch (error) {
        // 错误处理
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.removeChild(chatMessages.lastElementChild);

        let errorMsg = "连接失败，请检查：<br>1. 后端main.py是否正在运行<br>2. 端口是否是8000";
        if (error.message) {
            errorMsg += "<br>错误：" + error.message;
        }

        addMessage(errorMsg, false);
        console.error("API错误：", error);
    } finally {
        // 恢复按钮
        sendBtn.disabled = false;
    }
}