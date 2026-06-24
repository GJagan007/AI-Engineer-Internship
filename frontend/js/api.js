/**
 * API Service - Backend Communication
 */

class APIService {
    constructor() {
        this.baseURL = window.location.origin;
        this.timeout = 60000;
    }

    async compile(prompt) {
        try {
            const response = await fetch(`${this.baseURL}/compile`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt }),
                signal: AbortSignal.timeout(this.timeout),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            if (error.name === 'TimeoutError') {
                throw new Error('Request timed out. Please try again.');
            }
            throw error;
        }
    }

    async getMetrics() {
        try {
            const response = await fetch(`${this.baseURL}/metrics`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Failed to fetch metrics:', error);
            return null;
        }
    }

    async healthCheck() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Health check failed:', error);
            return null;
        }
    }
}

const api = new APIService();