/**
 * Metrics Service - Track and Display Performance Metrics
 */

class MetricsService {
    constructor() {
        this.metrics = {
            totalRequests: 0,
            successCount: 0,
            failureCount: 0,
            totalRetries: 0,
            totalRepairs: 0,
            successRate: 0,
            avgLatencyMs: 0
        };

        this.elements = {
            totalRequests: document.getElementById('totalRequests'),
            successRate: document.getElementById('successRate'),
            avgLatency: document.getElementById('avgLatency'),
            totalRetries: document.getElementById('totalRetries'),
            totalFailures: document.getElementById('totalFailures'),
            totalRepairs: document.getElementById('totalRepairs'),
            resetMetricsBtn: document.getElementById('resetMetricsBtn'),
        };

        this.initEventListeners();
        this.loadMetrics();
    }

    initEventListeners() {
        if (this.elements.resetMetricsBtn) {
            this.elements.resetMetricsBtn.addEventListener('click', () => {
                this.reset();
            });
        }
    }

    async loadMetrics() {
        try {
            const data = await api.getMetrics();
            if (data) {
                this.update(data);
            }
        } catch (error) {
            console.error('Failed to load metrics:', error);
        }
    }

    update(data) {
        this.metrics = { ...this.metrics, ...data };
        this.render();
    }

    render() {
        if (this.elements.totalRequests) {
            this.elements.totalRequests.textContent = this.metrics.totalRequests || 0;
        }
        if (this.elements.successRate) {
            const rate = this.metrics.successRate || 0;
            this.elements.successRate.textContent = `${rate.toFixed(1)}%`;
        }
        if (this.elements.avgLatency) {
            const latency = this.metrics.avgLatencyMs || 0;
            this.elements.avgLatency.textContent = `${latency.toFixed(0)}ms`;
        }
        if (this.elements.totalRetries) {
            this.elements.totalRetries.textContent = this.metrics.totalRetries || 0;
        }
        if (this.elements.totalFailures) {
            this.elements.totalFailures.textContent = this.metrics.failureCount || 0;
        }
        if (this.elements.totalRepairs) {
            this.elements.totalRepairs.textContent = this.metrics.totalRepairs || 0;
        }
    }

    reset() {
        this.metrics = {
            totalRequests: 0,
            successCount: 0,
            failureCount: 0,
            totalRetries: 0,
            totalRepairs: 0,
            successRate: 0,
            avgLatencyMs: 0
        };
        this.render();
        ui.showToast('Metrics reset', 'success');
    }

    trackRequest(success, latency) {
        this.metrics.totalRequests++;
        if (success) {
            this.metrics.successCount++;
        } else {
            this.metrics.failureCount++;
        }
        
        // Calculate rates
        if (this.metrics.totalRequests > 0) {
            this.metrics.successRate = (this.metrics.successCount / this.metrics.totalRequests) * 100;
        }
        
        this.render();
    }

    trackRetry() {
        this.metrics.totalRetries++;
        this.render();
    }

    trackRepair() {
        this.metrics.totalRepairs++;
        this.render();
    }
}

const metrics = new MetricsService();