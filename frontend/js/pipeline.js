/**
 * Pipeline Service - Orchestrate the Compilation Pipeline
 */

class PipelineService {
    constructor() {
        this.isCompiling = false;
        this.retryCount = 0;
        this.maxRetries = 3;
        this.currentOutput = null;
    }

    async compile(prompt) {
        if (this.isCompiling) return;
        if (!prompt) {
            ui.showToast('Please enter your requirements', 'error');
            return;
        }

        this.isCompiling = true;
        this.retryCount = 0;
        ui.setCompiling(true);

        try {
            const startTime = performance.now();
            
            // Update status
            ui.setStatus('compiling', 'Sending request...');
            
            // Make API call
            const result = await api.compile(prompt);
            
            const latency = performance.now() - startTime;
            
            // Check for errors
            if (result.error) {
                throw new Error(result.error);
            }
            
            // Store output
            this.currentOutput = result;
            window.appState.currentOutput = result;
            
            // Display results
            ui.displayOutput(result);
            
            // Track metrics
            metrics.trackRequest(true, latency);
            
            // Check for repairs
            if (result.validation?.needs_repair) {
                metrics.trackRepair();
            }
            
            // Display execution if available
            if (result.execution) {
                ui.displayExecution(result.execution);
            }
            
            // Update status
            ui.setStatus('success', '✅ Compilation successful');
            ui.showToast('Compilation successful!', 'success');
            
            // Switch to output tab
            ui.switchTab('output');
            
            // Reload metrics
            await metrics.loadMetrics();
            
            return result;
            
        } catch (error) {
            console.error('Compilation failed:', error);
            
            // Retry logic
            if (this.retryCount < this.maxRetries) {
                this.retryCount++;
                metrics.trackRetry();
                ui.setStatus('compiling', `Retrying... (${this.retryCount}/${this.maxRetries})`);
                ui.showToast(`Retrying (${this.retryCount}/${this.maxRetries})...`, 'warning');
                await new Promise(resolve => setTimeout(resolve, 2000));
                return this.compile(prompt);
            }
            
            // Final failure
            metrics.trackRequest(false, 0);
            ui.setStatus('error', `❌ Compilation failed: ${error.message}`);
            ui.showToast(`Compilation failed: ${error.message}`, 'error');
            
            throw error;
            
        } finally {
            this.isCompiling = false;
            ui.setCompiling(false);
        }
    }

    reset() {
        this.currentOutput = null;
        window.appState.currentOutput = null;
        ui.displayEmptyOutput();
        ui.displayEmptyExecution();
        ui.setStatus('ready', 'Ready');
        ui.showToast('Reset complete', 'info');
    }
}

const pipeline = new PipelineService();