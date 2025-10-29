// Activity Impact Tracker - Frontend JavaScript
// API Base URL
const API_BASE_URL = '/api';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    initializeThemeToggle();
});

// Theme Toggle Functionality
function initializeThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    const savedTheme = localStorage.getItem('theme') || 'dark';
    
    // Apply saved theme
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
    }
    
    // Toggle theme on click
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('light-theme');
        const currentTheme = document.body.classList.contains('light-theme') ? 'light' : 'dark';
        localStorage.setItem('theme', currentTheme);
    });
}

async function initializeApp() {
    await loadCategories();
    await loadActivities();
    await loadStats();
    await checkAIStatus();
    
    // Set up event listeners
    document.getElementById('activity-form').addEventListener('submit', handleAddActivity);
    document.getElementById('filter-category').addEventListener('change', handleFilterChange);
    document.getElementById('clear-filters').addEventListener('click', clearFilters);
    document.getElementById('generate-summary-btn').addEventListener('click', handleGenerateSummary);
    document.getElementById('generate-review-summary-btn').addEventListener('click', handleGenerateReviewSummary);
    document.getElementById('copy-review-btn').addEventListener('click', copyReviewToClipboard);
    
    // Set today's date as default
    document.getElementById('date').valueAsDate = new Date();
}

// Load categories from API and populate dropdowns
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/categories`);
        const data = await response.json();
        
        const categorySelect = document.getElementById('category');
        const filterCategorySelect = document.getElementById('filter-category');
        
        data.categories.forEach(category => {
            const option1 = document.createElement('option');
            option1.value = category;
            option1.textContent = category;
            categorySelect.appendChild(option1);
            
            const option2 = document.createElement('option');
            option2.value = category;
            option2.textContent = category;
            filterCategorySelect.appendChild(option2);
        });
    } catch (error) {
        console.error('Error loading categories:', error);
        showToast('Error loading categories', 'error');
    }
}

// Load all activities from API
async function loadActivities(filters = {}) {
    try {
        let url = `${API_BASE_URL}/activities`;
        const params = new URLSearchParams();
        
        if (filters.circle) params.append('circle', filters.circle);
        if (filters.category) params.append('category', filters.category);
        
        if (params.toString()) {
            url += '?' + params.toString();
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        displayActivities(data.activities);
    } catch (error) {
        console.error('Error loading activities:', error);
        showToast('Error loading activities', 'error');
    }
}

// Toggle activity collapse/expand
function toggleActivity(header) {
    const card = header.parentElement;
    const content = card.querySelector('.activity-content');
    const icon = header.querySelector('.collapse-icon');
    
    if (content.style.display === 'none') {
        content.style.display = 'block';
        icon.textContent = '▼';
        card.classList.remove('collapsed');
    } else {
        content.style.display = 'none';
        icon.textContent = '▶';
        card.classList.add('collapsed');
    }
}

// Display activities grouped by impact circle
function displayActivities(activities) {
    const container = document.getElementById('all-activities');
    container.innerHTML = '';
    
    if (activities.length === 0) {
        container.innerHTML = '<div class="empty-message">No activities yet. Add your first activity above!</div>';
    } else {
        activities.forEach(activity => {
            const activityCard = createActivityCard(activity);
            container.appendChild(activityCard);
        });
    }
}

// Create an activity card element
function createActivityCard(activity) {
    const card = document.createElement('div');
    card.className = 'activity-card collapsed';
    
    const date = new Date(activity.date);
    const formattedDate = date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
    
    let html = `
        <div class="activity-header" onclick="toggleActivity(this)" style="cursor: pointer;">
            <div style="display: flex; align-items: center; gap: 8px; flex: 1;">
                <span class="collapse-icon">▶</span>
                <div class="activity-title">${escapeHtml(activity.title)}</div>
            </div>
            <div class="activity-date">${formattedDate}</div>
        </div>
        <div class="activity-category">${escapeHtml(activity.category)}</div>
        <div class="activity-content" style="display: none;">
    `;
    
    if (activity.description) {
        html += `<div class="activity-description">${escapeHtml(activity.description)}</div>`;
    }
    
    if (activity.ai_summary) {
        html += `
            <div class="activity-ai-summary">
                <div class="impact-label">🤖 AI Summary:</div>
                <div>${escapeHtml(activity.ai_summary)}</div>
            </div>
        `;
    }
    
    if (activity.tags && activity.tags.length > 0) {
        html += '<div class="activity-tags">';
        activity.tags.forEach(tag => {
            html += `<span class="tag">#${escapeHtml(tag)}</span>`;
        });
        html += '</div>';
    }
    
    html += `
            <div class="activity-actions">
                <button class="btn btn-danger" onclick="deleteActivity(${activity.id}); event.stopPropagation();">Delete</button>
            </div>
        </div>
    `;
    
    card.innerHTML = html;
    return card;
}

// Handle form submission to add new activity
async function handleAddActivity(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const tags = formData.get('tags') 
        ? formData.get('tags').split(',').map(t => t.trim()).filter(t => t)
        : [];
    
    // Get AI summary if it was generated
    const summaryBox = document.getElementById('ai-summary');
    const aiSummary = summaryBox.textContent.trim();
    
    const activity = {
        title: formData.get('title'),
        description: formData.get('description'),
        category: formData.get('category'),
        ai_summary: aiSummary || '',
        date: formData.get('date') || new Date().toISOString(),
        tags: tags
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/activities`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(activity)
        });
        
        if (!response.ok) {
            throw new Error('Failed to create activity');
        }
        
        const data = await response.json();
        
        // Reset form and AI summary section
        event.target.reset();
        document.getElementById('date').valueAsDate = new Date();
        document.getElementById('ai-summary-section').style.display = 'none';
        summaryBox.textContent = '';
        
        // Reload activities and stats
        await loadActivities();
        await loadStats();
        
        showToast('Activity added successfully! 🎉', 'success');
    } catch (error) {
        console.error('Error adding activity:', error);
        showToast('Error adding activity', 'error');
    }
}

// Delete an activity
async function deleteActivity(activityId) {
    if (!confirm('Are you sure you want to delete this activity?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/activities/${activityId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete activity');
        }
        
        // Reload activities and stats
        await loadActivities();
        await loadStats();
        
        showToast('Activity deleted successfully', 'success');
    } catch (error) {
        console.error('Error deleting activity:', error);
        showToast('Error deleting activity', 'error');
    }
}

// Handle filter changes
function handleFilterChange() {
    const category = document.getElementById('filter-category').value;
    
    const filters = {};
    if (category) filters.category = category;
    
    loadActivities(filters);
}

// Clear all filters
function clearFilters() {
    document.getElementById('filter-category').value = '';
    loadActivities();
}

// Load and display statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        const data = await response.json();
        
        document.getElementById('total-activities').textContent = data.total_activities;
        document.getElementById('total-categories').textContent = data.categories_used || 0;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.className = 'toast';
    }, 3000);
}

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Generate Performance Review Summary
async function handleGenerateReviewSummary() {
    const button = document.getElementById('generate-review-summary-btn');
    const summarySection = document.getElementById('review-summary-section');
    const summaryContent = document.getElementById('review-summary-content');
    
    try {
        button.disabled = true;
        button.textContent = '🔄 Generating...';
        
        // Get all activities
        const response = await fetch(`${API_BASE_URL}/activities`);
        const data = await response.json();
        const activities = data.activities;
        
        // Filter activities that have AI summaries
        const activitiesWithSummaries = activities.filter(a => a.ai_summary);
        
        if (activitiesWithSummaries.length === 0) {
            showToast('No activities with AI summaries found', 'error');
            button.disabled = false;
            button.textContent = '🤖 Generate Performance Review Summary';
            return;
        }
        
        // Call the new API endpoint to generate review summary
        const summaryResponse = await fetch(`${API_BASE_URL}/generate-review-summary`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                activities: activitiesWithSummaries
            })
        });
        
        const summaryData = await summaryResponse.json();
        
        if (summaryResponse.ok && summaryData.summary) {
            summaryContent.innerHTML = `<pre>${escapeHtml(summaryData.summary)}</pre>`;
            summarySection.style.display = 'block';
            showToast('Performance review summary generated!', 'success');
        } else {
            showToast(summaryData.error || 'Failed to generate summary', 'error');
        }
        
    } catch (error) {
        console.error('Error generating review summary:', error);
        showToast('Error generating summary', 'error');
    } finally {
        button.disabled = false;
        button.textContent = '🤖 Generate Performance Review Summary';
    }
}

// Copy review summary to clipboard
function copyReviewToClipboard() {
    const summaryContent = document.getElementById('review-summary-content');
    const text = summaryContent.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showToast('Failed to copy to clipboard', 'error');
    });
}

// Check if AI service is available
async function checkAIStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/ai-status`);
        const data = await response.json();
        
        const generateBtn = document.getElementById('generate-summary-btn');
        const aiHelp = document.querySelector('.ai-help');
        
        if (!data.enabled) {
            generateBtn.disabled = true;
            generateBtn.textContent = '🤖 AI Not Available';
            aiHelp.style.display = 'block';
            aiHelp.textContent = 'Foundry Local is not running. Install and run it to enable AI summaries.';
        } else {
            aiHelp.style.display = 'block';
            aiHelp.textContent = `Powered by ${data.model}`;
        }
    } catch (error) {
        console.error('Error checking AI status:', error);
    }
}

// Handle AI summary generation
async function handleGenerateSummary() {
    const description = document.getElementById('description').value;
    const category = document.getElementById('category').value;
    const title = document.getElementById('title').value;
    const tags = document.getElementById('tags').value;
    
    if (!description) {
        showToast('Please fill in the description first', 'error');
        return;
    }
    
    const generateBtn = document.getElementById('generate-summary-btn');
    const summarySection = document.getElementById('ai-summary-section');
    const summaryBox = document.getElementById('ai-summary');
    
    // Show loading state
    generateBtn.disabled = true;
    generateBtn.textContent = '⏳ Generating...';
    summaryBox.className = 'ai-summary-box loading';
    summaryBox.textContent = '';
    summarySection.style.display = 'block';
    
    try {
        const response = await fetch(`${API_BASE_URL}/generate-summary`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: title,
                description: description,
                category: category,
                tags: tags
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate summary');
        }
        
        // Display the generated summary
        summaryBox.className = 'ai-summary-box';
        summaryBox.textContent = data.summary;
        
        showToast('AI summary generated successfully! 🎉', 'success');
        
    } catch (error) {
        console.error('Error generating summary:', error);
        summaryBox.className = 'ai-summary-box';
        summaryBox.textContent = `Error: ${error.message}`;
        showToast('Failed to generate AI summary', 'error');
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = '🤖 Generate AI Summary';
    }
}

// Toggle filter section
function toggleFilterSection() {
    const filterContent = document.getElementById('filter-content');
    const header = event.currentTarget;
    const icon = header.querySelector('.collapse-icon');
    
    if (filterContent.style.display === 'none') {
        filterContent.style.display = 'block';
        icon.textContent = '▼';
    } else {
        filterContent.style.display = 'none';
        icon.textContent = '▶';
    }
}

// Toggle activities section
function toggleActivitiesSection() {
    const activitiesContent = document.getElementById('all-activities');
    const header = event.currentTarget;
    const icon = header.querySelector('.collapse-icon');
    
    if (activitiesContent.style.display === 'none') {
        activitiesContent.style.display = 'block';
        icon.textContent = '▼';
    } else {
        activitiesContent.style.display = 'none';
        icon.textContent = '▶';
    }
}

// Toggle performance review section
function togglePerformanceSection() {
    const performanceContent = document.getElementById('performance-review-content');
    const header = event.currentTarget;
    const icon = header.querySelector('.collapse-icon');
    
    if (performanceContent.style.display === 'none') {
        performanceContent.style.display = 'block';
        icon.textContent = '▼';
    } else {
        performanceContent.style.display = 'none';
        icon.textContent = '▶';
    }
}
