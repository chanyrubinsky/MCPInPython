const observer = new MutationObserver(() => {
    const toolbars = document.querySelectorAll('.J-Z');
    toolbars.forEach(toolbar => {
        if (!toolbar.querySelector('#mcp-style-btn')) {
            injectButton(toolbar);
        }
    });
});

observer.observe(document.body, { childList: true, subtree: true });

function injectButton(toolbar) {
    const btn = document.createElement('div');
    btn.id = 'mcp-style-btn';
    btn.title = 'Style Assistant';
    btn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L14.5 9.5H22L16 14L18.5 21.5L12 17L5.5 21.5L8 14L2 9.5H9.5L12 2Z" fill="#6C47FF"/>
        </svg>
    `;
    btn.style.cssText = `cursor:pointer; padding:6px; border-radius:6px; display:flex; align-items:center; margin:0 2px; transition:background 0.15s;`;

    btn.onmouseenter = () => btn.style.background = '#EDE9FF';
    btn.onmouseleave = () => btn.style.background = 'transparent';
    btn.onclick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        toggleSidebar(toolbar);
    };

    toolbar.insertBefore(btn, toolbar.firstChild);
}

let sidebarFrame = null;

function toggleSidebar(toolbar) {
    if (sidebarFrame) {
        sidebarFrame.remove();
        sidebarFrame = null;
        return;
    }

    const composeWindow = toolbar.closest('.aoI');
    if (!composeWindow) return;

    sidebarFrame = document.createElement('iframe');
    // שימוש ב-chrome.runtime.getURL מחייב הגדרה במניפסט
    sidebarFrame.src = chrome.runtime.getURL('sidebar.html');

    // הגדרות CSS חזקות יותר כדי למנוע חסימה או עיוות
    sidebarFrame.style.cssText = `
        width: 340px !important;
        height: 100% !important;
        border: none !important;
        border-left: 1px solid #e0e0e0 !important;
        flex-shrink: 0 !important;
        display: block !important;
    `;

    // הפיכת חלון המייל ל-Flex כדי שהסיידבר יוצג לצדו
    composeWindow.style.display = 'flex';
    composeWindow.style.flexDirection = 'row';
    composeWindow.appendChild(sidebarFrame);

    // טיפול בהודעות מה-iframe
    const handleMessage = (e) => {
        if (e.data.type === 'INSERT_TEXT') {
            const body = composeWindow.querySelector('[contenteditable="true"]');
            if (body) {
                // שימוש ב-innerText בטוח יותר מ-innerHTML
                body.innerText = e.data.text;
                body.focus();
            }
        }
    };

    window.addEventListener('message', handleMessage, { once: false });
}