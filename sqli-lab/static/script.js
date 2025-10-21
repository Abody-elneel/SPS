// Tab switching functionality
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.getAttribute('data-tab');
        
        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Remove active class from all buttons
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Show selected tab
        document.getElementById(tabName).classList.add('active');
        button.classList.add('active');
    });
});

// Login form handler
async function handleLogin() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const resultDiv = document.getElementById('loginResult');
    
    if (!username || !password) {
        showResult(resultDiv, 'Please enter both username and password', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResult(resultDiv, data.message, 'success');
            displayUserInfo(resultDiv, data.user);
        } else {
            showResult(resultDiv, data.message, 'error');
        }
    } catch (error) {
        showResult(resultDiv, 'Error: ' + error.message, 'error');
    }
}

// Search form handler
async function handleSearch() {
    const searchTerm = document.getElementById('searchInput').value;
    const resultDiv = document.getElementById('searchResult');
    
    if (!searchTerm) {
        showResult(resultDiv, 'Please enter a search term', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                search: searchTerm
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResult(resultDiv, `Found ${data.count} result(s)`, 'success');
            displaySearchResults(resultDiv, data.results);
        } else {
            showResult(resultDiv, data.message, 'error');
        }
    } catch (error) {
        showResult(resultDiv, 'Error: ' + error.message, 'error');
    }
}

// Raw query handler
async function handleQuery() {
    const query = document.getElementById('queryInput').value;
    const resultDiv = document.getElementById('queryResult');
    
    if (!query) {
        showResult(resultDiv, 'Please enter a SQL query', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/query-debug', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResult(resultDiv, 'Query executed successfully', 'success');
            showResult(resultDiv, `Query: ${data.query_executed}`, 'info');
            displayQueryResults(resultDiv, data.results);
        } else {
            showResult(resultDiv, data.message, 'error');
        }
    } catch (error) {
        showResult(resultDiv, 'Error: ' + error.message, 'error');
    }
}

// Helper function to show results
function showResult(element, message, type) {
    element.className = `result show ${type}`;
    element.innerHTML = `<h3>${message}</h3>`;
}

// Display user info
function displayUserInfo(element, user) {
    const table = `
        <table>
            <tr>
                <th>Field</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>ID</td>
                <td>${user.id}</td>
            </tr>
            <tr>
                <td>Username</td>
                <td>${user.username}</td>
            </tr>
            <tr>
                <td>Email</td>
                <td>${user.email}</td>
            </tr>
            <tr>
                <td>Is Admin</td>
                <td>${user.is_admin ? 'Yes' : 'No'}</td>
            </tr>
        </table>
    `;
    element.innerHTML += table;
}

// Display search results
function displaySearchResults(element, results) {
    if (results.length === 0) {
        element.innerHTML += '<p>No results found</p>';
        return;
    }
    
    let table = '<table><tr><th>ID</th><th>Username</th><th>Email</th></tr>';
    results.forEach(user => {
        table += `<tr><td>${user.id}</td><td>${user.username}</td><td>${user.email}</td></tr>`;
    });
    table += '</table>';
    
    element.innerHTML += table;
}

// Display query results
function displayQueryResults(element, results) {
    if (results.length === 0) {
        element.innerHTML += '<p>No results returned</p>';
        return;
    }
    
    let table = '<table><tr>';
    
    // Get column headers
    const columns = Object.keys(results[0]);
    columns.forEach(col => {
        table += `<th>${col}</th>`;
    });
    table += '</tr>';
    
    // Add rows
    results.forEach(row => {
        table += '<tr>';
        columns.forEach(col => {
            table += `<td>${row[col]}</td>`;
        });
        table += '</tr>';
    });
    
    table += '</table>';
    element.innerHTML += table;
}