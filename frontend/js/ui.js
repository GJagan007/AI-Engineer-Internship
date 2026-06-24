/**
 * UI Service - DOM Manipulation
 */

class UIService {
    constructor() {
        this.theme = localStorage.getItem('ai-compiler-theme') || 'light';
        
        // DOM references
        this.elements = {
            themeToggle: document.getElementById('themeToggle'),
            promptInput: document.getElementById('promptInput'),
            compileBtn: document.getElementById('compileBtn'),
            exampleBtn: document.getElementById('exampleBtn'),
            clearBtn: document.getElementById('clearBtn'),
            statusDot: document.getElementById('statusDot'),
            statusText: document.getElementById('statusText'),
            tabBtns: document.querySelectorAll('.tab-btn'),
            outputBody: document.getElementById('outputBody'),
            copyBtn: document.getElementById('copyBtn'),
            downloadBtn: document.getElementById('downloadBtn'),
            executionBody: document.getElementById('executionBody'),
            executionStatus: document.getElementById('executionStatus'),
            helpBtn: document.getElementById('helpBtn'),
            helpModal: document.getElementById('helpModal'),
            helpClose: document.getElementById('helpClose'),
            resetMetricsBtn: document.getElementById('resetMetricsBtn'),
        };

        this.initTheme();
        this.initTabs();
        this.initEventListeners();
    }

    initTheme() {
        this.setTheme(this.theme);
    }

    setTheme(theme) {
        this.theme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        if (this.elements.themeToggle) {
            this.elements.themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
        localStorage.setItem('ai-compiler-theme', theme);
    }

    toggleTheme() {
        this.setTheme(this.theme === 'light' ? 'dark' : 'light');
    }

    initTabs() {
        this.elements.tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const tab = btn.dataset.tab;
                this.switchTab(tab);
            });
        });
    }

    switchTab(tabId) {
        this.elements.tabBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabId);
        });

        document.querySelectorAll('.tab-panel').forEach(panel => {
            panel.classList.toggle('active', panel.id === `${tabId}Tab`);
        });
    }

    setStatus(status, text) {
        if (this.elements.statusDot) {
            this.elements.statusDot.className = `status-dot ${status}`;
        }
        if (this.elements.statusText) {
            this.elements.statusText.textContent = text;
        }
    }

    setExecutionStatus(status, text) {
        if (this.elements.executionStatus) {
            this.elements.executionStatus.className = `execution-status ${status}`;
            this.elements.executionStatus.textContent = text;
        }
    }

    displayOutput(data) {
        if (!this.elements.outputBody) return;
        
        const formatted = JSON.stringify(data, null, 2);
        const highlighted = this.syntaxHighlight(formatted);
        this.elements.outputBody.innerHTML = highlighted;
    }

    displayExecution(result) {
        if (!this.elements.executionBody) return;

        let html = '';
        
        if (result.success) {
            html += '✅ <strong>Execution Successful</strong>\n\n';
            for (const phase of result.results) {
                const icon = phase.status === 'success' ? '✅' : 
                           phase.status === 'warning' ? '⚠️' : '❌';
                html += `${icon} ${phase.phase}: ${phase.message}\n`;
                if (phase.details) {
                    html += `   └─ ${JSON.stringify(phase.details, null, 2)}\n`;
                }
            }
            html += `\n⏱️ Summary: ${result.summary?.successful_phases || 0}/${result.summary?.total_phases || 0} phases successful`;
        } else {
            html += '❌ <strong>Execution Failed</strong>\n\n';
            for (const phase of result.results) {
                const icon = phase.status === 'success' ? '✅' : 
                           phase.status === 'warning' ? '⚠️' : '❌';
                html += `${icon} ${phase.phase}: ${phase.message}\n`;
            }
        }
        
        this.elements.executionBody.innerHTML = html.replace(/\n/g, '<br>');
        this.setExecutionStatus(
            result.success ? 'success' : 'failed',
            result.success ? '✅ Success' : '❌ Failed'
        );
    }

    displayEmptyOutput() {
        if (!this.elements.outputBody) return;
        this.elements.outputBody.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">🚀</span>
                <p>Enter your requirements and click "Compile" to generate the application configuration</p>
            </div>
        `;
    }

    displayEmptyExecution() {
        if (!this.elements.executionBody) return;
        this.elements.executionBody.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">▶</span>
                <p>Compile your application to see execution validation</p>
            </div>
        `;
        this.setExecutionStatus('', 'Waiting');
    }

    syntaxHighlight(json) {
        json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
            let cls = 'json-number';
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = 'json-key';
                } else {
                    cls = 'json-string';
                }
            } else if (/true|false/.test(match)) {
                cls = 'json-boolean';
            } else if (/null/.test(match)) {
                cls = 'json-null';
            }
            return '<span class="' + cls + '">' + match + '</span>';
        });
    }

    setCompiling(isCompiling) {
        if (!this.elements.compileBtn) return;
        if (isCompiling) {
            this.elements.compileBtn.disabled = true;
            this.elements.compileBtn.innerHTML = '<span class="spinner"></span> Compiling...';
            this.setStatus('compiling', 'Compiling...');
        } else {
            this.elements.compileBtn.disabled = false;
            this.elements.compileBtn.innerHTML = '<span class="btn-icon">▶</span> Compile';
        }
    }

    showToast(message, type = 'info') {
        const container = document.querySelector('.toast-container') || (() => {
            const c = document.createElement('div');
            c.className = 'toast-container';
            document.body.appendChild(c);
            return c;
        })();

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(20px)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    copyOutput(data) {
        const text = JSON.stringify(data, null, 2);
        navigator.clipboard.writeText(text).then(() => {
            this.showToast('Copied to clipboard!', 'success');
        }).catch(() => {
            // Fallback
            const textarea = document.createElement('textarea');
            textarea.value = text;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            textarea.remove();
            this.showToast('Copied to clipboard!', 'success');
        });
    }

    downloadOutput(data) {
        const text = JSON.stringify(data, null, 2);
        const blob = new Blob([text], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `app-config-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
        this.showToast('Downloaded successfully!', 'success');
    }

    initEventListeners() {
        // Theme toggle
        if (this.elements.themeToggle) {
            this.elements.themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // Help modal
        if (this.elements.helpBtn) {
            this.elements.helpBtn.addEventListener('click', () => {
                this.elements.helpModal.classList.add('active');
            });
        }
        if (this.elements.helpClose) {
            this.elements.helpClose.addEventListener('click', () => {
                this.elements.helpModal.classList.remove('active');
            });
        }
        if (this.elements.helpModal) {
            this.elements.helpModal.addEventListener('click', (e) => {
                if (e.target === this.elements.helpModal) {
                    this.elements.helpModal.classList.remove('active');
                }
            });
        }

        // Output actions
        if (this.elements.copyBtn) {
            this.elements.copyBtn.addEventListener('click', () => {
                const data = window.appState?.currentOutput;
                if (data) this.copyOutput(data);
                else this.showToast('No output to copy', 'error');
            });
        }
        if (this.elements.downloadBtn) {
            this.elements.downloadBtn.addEventListener('click', () => {
                const data = window.appState?.currentOutput;
                if (data) this.downloadOutput(data);
                else this.showToast('No output to download', 'error');
            });
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                if (this.elements.helpModal?.classList.contains('active')) {
                    this.elements.helpModal.classList.remove('active');
                }
            }
        });
    }

    getPrompt() {
        return this.elements.promptInput?.value?.trim() || '';
    }

    setPrompt(value) {
        if (this.elements.promptInput) {
            this.elements.promptInput.value = value;
        }
    }

    clearPrompt() {
        if (this.elements.promptInput) {
            this.elements.promptInput.value = '';
        }
        this.setStatus('ready', 'Ready');
        this.displayEmptyOutput();
        this.displayEmptyExecution();
        window.appState.currentOutput = null;
    }
}

const ui = new UIService();