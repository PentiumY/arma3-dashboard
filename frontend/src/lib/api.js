const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

async function get(endpoint) {
    const res = await fetch(`${BASE_URL}/${endpoint}`);
    if (!res.ok) throw new Error(`Failed to fetch ${endpoint}: ${res.statusText}`);
    return res.json();
}

async function post(endpoint, body, isFormData = false) {
    const options = {
        method: 'POST',
        headers: isFormData ? {} : { 'Content-Type': 'application/json' },
        body: isFormData ? body : JSON.stringify(body),
    };
    const res = await fetch(`${BASE_URL}/${endpoint}`, options);
    if (!res.ok) throw new Error(`Failed to post ${endpoint}: ${res.statusText}`);
    return res.json();
}

/**
 * Generic fetch helper for custom requests.
 * @param {string} endpoint - API endpoint (relative to BASE_URL)
 * @param {object} options - Fetch options (method, headers, body, etc.)
 * @returns {Promise<any>} - Parsed JSON response
 */
async function fetchRequest(endpoint, options = {}) {
    const res = await fetch(`${BASE_URL}/${endpoint}`, options);
    if (!res.ok) throw new Error(`Failed to fetch ${endpoint}: ${res.statusText}`);
    return res.json();
}

export default { get, post, fetchRequest };
