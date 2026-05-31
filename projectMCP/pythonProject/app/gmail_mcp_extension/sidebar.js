const MCP = "http://localhost:5678";

document.addEventListener('DOMContentLoaded', () => {
    // מאזינים לצ'יפים
    document.querySelectorAll('.chip').forEach(chip => {
        chip.addEventListener('click', function() {
            document.querySelectorAll(".chip").forEach(c => c.classList.remove("active"));
            this.classList.add("active");
        });
    });

    // מאזין לכפתור יצירה
    document.getElementById('genBtn').addEventListener('click', generate);

    // מאזין לכפתור העתקה
    document.getElementById('copyBtn').addEventListener('click', () => {
        const text = document.getElementById("resultText").textContent;
        navigator.clipboard.writeText(text);
    });

    // מאזין לכפתור נסח שוב
    document.getElementById('retryBtn').addEventListener('click', generate);

    // מאזין לכפתור הכנס למייל
    document.getElementById('insertBtn').addEventListener('click', () => {
        const text = document.getElementById("resultText").textContent;
        window.parent.postMessage({ type: "INSERT_TEXT", text }, "*");
    });
});

async function generate() {
    const text = document.getElementById("txt").value.trim();
    if (!text) { document.getElementById("txt").focus(); return; }

    const style = document.querySelector(".chip.active")?.textContent || "מקצועי";
    const tone  = document.getElementById("tone").value / 100;

    const btn = document.getElementById("genBtn");
    const sp  = document.getElementById("sp");
    const lbl = document.getElementById("genLbl");
    const err = document.getElementById("err");
    const res = document.getElementById("result");

    btn.disabled = true; sp.style.display = "block"; lbl.textContent = "מנסח...";
    err.style.display = "none"; res.classList.remove("show");

    try {
        const r = await fetch(MCP + "/compose", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, style, tone })
        });
        const data = await r.json();
        document.getElementById("resultText").textContent = data.result || data.error;
        res.classList.add("show");
        lbl.textContent = "✦ נסח שוב";
    } catch (e) {
        err.style.display = "block";
        lbl.textContent = "✦ נסח מייל";
    } finally {
        btn.disabled = false; sp.style.display = "none";
    }
}