// Container Poker - Main JavaScript
// Educational container orchestration platform

// Global state
const state = {
    containers: [],
    selectedContainer: null,
    autoRefresh: true,
    refreshInterval: 5000
};

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎓 Container Poker initialized!');
    console.log('💡 Check the browser console for educational tips');
    
    // Set up global error handler for educational feedback
    window.addEventListener('error', function(event) {
        console.error('❌ JavaScript Error:', event.error);
        console.log('💡 TIP: Check your browser developer tools for debugging');
    });
});

// Utility Functions

// Show notification
function showNotification(message, type = 'info') {
    // For now, use alert. In production, use a proper notification library
    const icon = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️'
    };
    
    alert(`${icon[type] || ''} ${message}`);
}

// Format timestamp
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

// Format bytes to human readable
function formatBytes(bytes) {
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 B';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
}

// API Helper Functions

// Make API request with error handling
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'API request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Container Management Functions

// Get container status icon
function getStatusIcon(status) {
    const icons = {
        'running': '🟢',
        'exited': '🔴',
        'paused': '⏸️',
        'restarting': '🔄',
        'dead': '💀',
        'created': '🆕'
    };
    return icons[status] || '❓';
}

// Get container action buttons based on status
function getContainerActions(container) {
    const actions = [];
    
    if (container.status === 'running') {
        actions.push(
            { action: 'stop', label: '⏹️ Stop', class: 'btn-warning' },
            { action: 'restart', label: '🔄 Restart', class: 'btn-info' }
        );
    } else {
        actions.push(
            { action: 'start', label: '▶️ Start', class: 'btn-success' }
        );
    }
    
    actions.push(
        { action: 'logs', label: '📋 Logs', class: 'btn-secondary' },
        { action: 'remove', label: '🗑️ Remove', class: 'btn-danger' }
    );
    
    return actions;
}

// Educational Helper Functions

// Show educational tip
function showEducationalTip(context, tip) {
    console.log(`💡 ${context}: ${tip}`);
}

// Get debugging suggestions based on error
function getDebuggingSuggestions(error) {
    const suggestions = [];
    
    if (error.includes('permission denied')) {
        suggestions.push('Check Docker permissions: sudo usermod -aG docker $USER');
        suggestions.push('Make sure Docker daemon is running: sudo systemctl status docker');
    } else if (error.includes('not found')) {
        suggestions.push('Check if the container/image exists: docker ps -a');
        suggestions.push('Pull missing images: docker pull <image-name>');
    } else if (error.includes('network')) {
        suggestions.push('Check network connectivity');
        suggestions.push('Verify Flask server is running on port 5000');
    }
    
    return suggestions;
}

// Event Handlers

// Handle container action
async function handleContainerAction(containerId, action) {
    if (action === 'remove' && !confirm('Are you sure you want to remove this container?')) {
        return;
    }
    
    try {
        const result = await apiRequest(`/api/containers/${containerId}/action`, {
            method: 'POST',
            body: JSON.stringify({ action })
        });
        
        showNotification(result.message, 'success');
        showEducationalTip('Container Action', result.educational_tip);
        
        // Refresh container list if on containers page
        if (window.refreshContainers) {
            window.refreshContainers();
        }
    } catch (error) {
        showNotification(`Failed to ${action} container: ${error.message}`, 'error');
        const suggestions = getDebuggingSuggestions(error.message);
        suggestions.forEach(s => console.log(`💡 ${s}`));
    }
}

// Handle example execution
async function handleExampleExecution(exampleId) {
    console.log(`🎓 Running example: ${exampleId}`);
    
    try {
        const result = await apiRequest(`/api/examples/${exampleId}`, {
            method: 'POST',
            body: JSON.stringify({})
        });
        
        if (result.success) {
            console.log('✅ Example completed successfully');
            console.log('📊 Results:', result.result);
            result.educational_notes?.forEach(note => 
                showEducationalTip('Example Note', note)
            );
        } else {
            console.error('❌ Example failed:', result.error);
            result.debugging_tips?.forEach(tip => 
                console.log(`🔧 Debugging tip: ${tip}`)
            );
        }
        
        return result;
    } catch (error) {
        console.error('Failed to execute example:', error);
        throw error;
    }
}

// Export functions for use in pages
window.containerPoker = {
    apiRequest,
    showNotification,
    showEducationalTip,
    handleContainerAction,
    handleExampleExecution,
    getStatusIcon,
    formatTimestamp,
    formatBytes
};

// Educational console messages
console.log('%c🎓 Welcome to Container Poker!', 'font-size: 20px; color: #3498db;');
console.log('%c💡 Learning Tips:', 'font-size: 16px; color: #2ecc71;');
console.log('1. Use the browser DevTools to inspect API calls');
console.log('2. Check the Network tab to see Docker API interactions');
console.log('3. Try modifying the code in ./src - it auto-reloads!');
console.log('4. Run "make logs" to see server-side logs');
console.log('5. Experiment with different container configurations');
console.log('\n%c🐳 Happy Learning!', 'font-size: 14px; color: #e74c3c;');