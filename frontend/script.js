const btn = document.getElementById("submit");
const status = document.getElementById("status");
const result = document.getElementById("result");
const historySection = document.getElementById("historySection");
const historyList = document.getElementById("historyList");
const copyBtn = document.getElementById("copyBtn");

const STORAGE_KEY = "resume_ai_history";
const MAX_HISTORY = 5;

// 读取历史
function loadHistory() {
    try {
        return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch {
        return [];
    }
}

// 保存历史
function saveHistory(history) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
}

// 渲染历史
function renderHistory() {
    const history = loadHistory();

    if (history.length === 0) {
        historySection.style.display = "none";
        return;
    }

    historySection.style.display = "block";
    historyList.innerHTML = "";

    history.forEach((item) => {
        const div = document.createElement("div");
        div.className = "history-item";
        div.innerHTML = `
            <div class="history-time">${item.time}</div>
            <div class="history-preview">${item.preview}</div>
        `;
        div.addEventListener("click", () => {
            result.textContent = item.result;
            result.classList.add("show");
            status.textContent = "已加载历史记录。";
            window.scrollTo({ top: result.offsetTop - 100, behavior: "smooth" });
        });
        historyList.appendChild(div);
    });
}

// 添加历史
function addHistory(resultText) {
    const history = loadHistory();

    const now = new Date();
    const time = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")} ${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;

    const preview = resultText.slice(0, 50).replace(/\n/g, " ") + "...";

    history.unshift({ time, preview, result: resultText });

    if (history.length > MAX_HISTORY) {
        history.length = MAX_HISTORY;
    }

    saveHistory(history);
    renderHistory();
}

// 把JSON结果格式化成可读文本
function formatResult(data) {
    let text = "";

    if (data.positionAlert) {
        text += `⚠ 岗位提醒\n\n${data.positionAlert}\n\n`;
    }

    if (data.matchScore !== undefined) {
        text += `一、匹配度\n\n${data.matchScore}%\n\n`;
    }

    if (data.problems && data.problems.length > 0) {
        text += `二、问题清单\n\n`;
        data.problems.forEach((p, i) => {
            text += `${i + 1}. ${p.title}\n   ${p.detail}\n\n`;
        });
    }

    if (data.suggestions && data.suggestions.length > 0) {
        text += `三、逐条建议\n\n`;
        data.suggestions.forEach((s, i) => {
            text += `${i + 1}. 问题：${s.problem}\n   建议：${s.advice}\n\n`;
        });
    }

    if (data.optimizedResume) {
        text += `四、优化后的简历\n\n${data.optimizedResume}\n\n`;
    }

    if (data.diff && data.diff.length > 0) {
        text += `五、修改对比\n\n`;
        data.diff.forEach((d, i) => {
            text += `${i + 1}. [${d.type || "修改"}]\n原文：${d.original}\n改后：${d.optimized}\n原因：${d.reason}\n\n`;
        });
    }

    if (data.pendingItems && data.pendingItems.length > 0) {
        text += `六、需要你补充的信息\n\n`;
        data.pendingItems.forEach((item, i) => {
            text += `${i + 1}. ${item}\n`;
        });
        text += `\n`;
    }
        if (data.learningPath && data.learningPath.length > 0) {
        text += `七、学习路径建议\n\n`;
        data.learningPath.forEach((item, i) => {
            text += `${i + 1}. 差距：${item.gap}\n`;
            text += `   建议：${item.suggestion}\n`;
            if (item.resources) {
                item.resources.forEach((r) => {
                    text += `   - [${r.type}] ${r.name}：${r.note}\n`;
                });
            }
            text += `\n`;
        });
    }
    return text;
}

// 点击优化
btn.addEventListener("click", async () => {
    const resume = document.getElementById("resume").value.trim();
    const jd = document.getElementById("jd").value.trim();

    if (!resume) {
        status.textContent = "请先粘贴简历。";
        return;
    }

    if (resume.length < 50) {
        status.textContent = "简历内容太少，请至少输入 50 个字。";
        return;
    }

    btn.disabled = true;
    status.textContent = "正在诊断，请稍候...";
    result.classList.remove("show");
    result.textContent = "";
    copyBtn.style.display = "none";

    try {
        const res = await fetch("http://127.0.0.1:8000/diagnose", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ resume, jd })
        });

        if (!res.ok) {
            throw new Error("后端返回错误：" + res.status);
        }

        const data = await res.json();

        if (data.error) {
            status.textContent = "出错了：" + data.error;
            result.textContent = data.raw || "";
            result.classList.add("show");
            return;
        }

        const formatted = formatResult(data);
        result.textContent = formatted;
        result.classList.add("show");
        status.textContent = "完成。";
        copyBtn.style.display = "inline-flex";
        copyBtn.textContent = "复制结果";
        copyBtn.classList.remove("copied");

        addHistory(formatted);
    } catch (err) {
        status.textContent = "出错了：" + err.message;
    } finally {
        btn.disabled = false;
    }
});

// 复制结果
copyBtn.addEventListener("click", async () => {
    const text = result.textContent;
    if (!text) return;

    try {
        await navigator.clipboard.writeText(text);
        copyBtn.textContent = "已复制";
        copyBtn.classList.add("copied");
        setTimeout(() => {
            copyBtn.textContent = "复制结果";
            copyBtn.classList.remove("copied");
        }, 2000);
    } catch {
        status.textContent = "复制失败，请手动选中复制。";
    }
});

// 页面加载时，渲染历史
renderHistory();