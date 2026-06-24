/**
 * Main Application - Initialize and Wire Everything
 */

// Global state
window.appState = {
    currentOutput: null,
    examples: [
        "Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments. Admins can see analytics.",
        "Create an e-commerce store with product catalog, shopping cart, user reviews, and admin panel for inventory management.",
        "Build a project management tool with task boards, team collaboration, file sharing, and time tracking.",
        "Create a social media platform with user profiles, posts, comments, likes, and direct messaging.",
        "Build a learning management system with courses, quizzes, student progress tracking, and certificate generation."
    ],
    exampleIndex: 0
};

class App {
    constructor() {
        this.init();
    }

    init() {
        // Initialize UI
        this.initUI();
        
        // Initialize event listeners
        this.initEventListeners();
        
        // Load initial state
        this.loadInitialState();
        
        // Start metrics polling
        this.startMetricsPolling();
        
        console.log('🚀 AI Compiler System initialized');
        console.log('📊 System ready for compilation');
    }

    initUI() {
        // Set initial status
        ui.setStatus('ready', 'Ready');
        ui.setExecutionStatus('', 'Waiting');
        
        // Display empty states
        ui.displayEmptyOutput();
        ui.displayEmptyExecution();
        
        // Load first example
        this.loadExample();
    }

    initEventListeners() {
        // Compile button
        const compileBtn = document.getElementById('compileBtn');
        if (compileBtn) {
            compileBtn.addEventListener('click', () => {
                this.handleCompile();
            });
        }

        // Example button
        const exampleBtn = document.getElementById('exampleBtn');
        if (exampleBtn) {
            exampleBtn.addEventListener('click', () => {
                this.loadExample();
            });
        }

        // Clear button
        const clearBtn = document.getElementById('clearBtn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                ui.clearPrompt();
                ui.showToast('Cleared', 'info');
            });
        }

        // Keyboard shortcut: Ctrl+Enter
        const promptInput = document.getElementById('promptInput');
        if (promptInput) {
            promptInput.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'Enter') {
                    this.handleCompile();
                }
            });
        }
    }

    loadInitialState() {
        // Load theme
        const savedTheme = localStorage.getItem('ai-compiler-theme') || 'light';
        ui.setTheme(savedTheme);
    }

    startMetricsPolling() {
        // Poll metrics every 10 seconds
        setInterval(async () => {
            try {
                await metrics.loadMetrics();
            } catch (error) {
                // Silent fail
            }
        }, 10000);
    }

    loadExample() {
        const examples = window.appState.examples;
        const index = window.appState.exampleIndex % examples.length;
        const prompt = examples[index];
        
        ui.setPrompt(prompt);
        window.appState.exampleIndex++;
        
        ui.showToast(`Loaded example: "${prompt.substring(0, 50)}..."`, 'info');
        ui.setStatus('ready', 'Example loaded');
    }

    async handleCompile() {
        const prompt = ui.getPrompt();
        if (!prompt) {
            ui.showToast('Please enter your requirements', 'error');
            return;
        }

        try {
            await pipeline.compile(prompt);
        } catch (error) {
            // Error already handled in pipeline
            console.error('Compile error:', error);
        }
    }
}

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const app = new App();
    window.app = app;
});