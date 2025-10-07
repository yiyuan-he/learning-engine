const codeEditor = document.getElementById('code-editor');
const runBtn = document.getElementById('run-btn');
const helpBtn = document.getElementById('help-btn');
const resultsDiv = document.getElementById('results');
const chatDiv = document.getElementById('chat');
const reflectionSection = document.getElementById('reflection-section');
const reflectionInput = document.getElementById('reflection-input');
const submitReflectionBtn = document.getElementById('submit-reflection-btn');
const reflectionFeedback = document.getElementById('reflection-feedback');

codeEditor.value = `def factorial(n):
    # write your code here
    pass`;

runBtn.addEventListener('click', async () => {
    const code = codeEditor.value;

    resultsDiv.textContent = 'Running tests...';

    try {
        const response = await fetch('/api/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        });

        const data = await response.json();
        resultsDiv.textContent = data.result;

        if (data.result.includes('All tests passed!')) {
            reflectionSection.style.display = 'block';
            reflectionInput.value = '';
            reflectionFeedback.style.display = 'none';
        } else {
            reflectionSection.style.display = 'none';
        }
    } catch (error) {
        resultsDiv.textContent = `Error: ${error.message}`;
    }
});

helpBtn.addEventListener('click', async () => {
    const code = codeEditor.value;

    chatDiv.textContent = 'AI Tutor is thinking...';

    try {
        const response = await fetch('/api/help', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        });

        const data = await response.json();
        chatDiv.textContent = data.response;
    } catch (error) {
        chatDiv.textContent = `Error: ${error.message}`;
    }
});

codeEditor.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
        e.preventDefault();
        const start = codeEditor.selectionStart;
        const end = codeEditor.selectionEnd;

        codeEditor.value = codeEditor.value.substring(0, start) + '    ' + codeEditor.value.substring(end);

        codeEditor.selectionStart = codeEditor.selectionEnd = start + 4;
    }
})

const themeToggle = document.getElementById('theme-toggle');

themeToggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    themeToggle.textContent = next === 'dark' ? '☀️' : '🌙';
});

submitReflectionBtn.addEventListener('click', async () => {
    const code = codeEditor.value;
    const explanation = reflectionInput.value.trim();

    if (!explanation) {
        alert('Please write an explanation first!');
        return;
    }

    reflectionFeedback.textContent = 'AI is evaluating your explanation...';
    reflectionFeedback.style.display = 'block';

    try {
        const response = await fetch('/api/reflect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code, explanation })
        });

        const data = await response.json();
        reflectionFeedback.textContent = data.feedback;
    } catch (error) {
        reflectionFeedback.textContent = `Error: ${error.message}`;
    }
})
