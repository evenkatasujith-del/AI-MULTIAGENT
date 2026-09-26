/**
 * VerifyAI API Service
 * Centralized client for communicating with the FastAPI backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

/**
 * Checks whether the backend is up and running.
 */
export async function checkBackendHealth() {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000);

    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'GET',
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (response.ok) {
      const data = await response.json();
      return { online: true, message: data.message || 'Connected' };
    }
    return { online: false, message: `HTTP ${response.status}` };
  } catch (error) {
    return { online: false, error: error.message };
  }
}

/**
 * Submits a question to the /smart-verify unified endpoint.
 * Backend automatically detects whether it is FACT, MATH, or CODE.
 */
export async function verifyQuestion(question, responseText = '', geminiApiKey = '') {
  if (!question || !question.trim()) {
    throw new Error('Please enter a question or problem to verify.');
  }

  const url = `${API_BASE_URL}/smart-verify`;

  const payload = {
    question: question.trim(),
  };

  if (responseText && responseText.trim()) {
    payload.response = responseText.trim();
  }

  if (geminiApiKey && geminiApiKey.trim()) {
    payload.gemini_api_key = geminiApiKey.trim();
  }

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      let errorDetail = `Backend returned status ${response.status}`;
      try {
        const errJson = await response.json();
        if (errJson.detail) {
          errorDetail = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail);
        }
      } catch {
        // Fallback to status text
      }
      throw new Error(errorDetail);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error(
        'Unable to connect to VerifyAI backend. Please make sure the FastAPI server is running on ' + API_BASE_URL
      );
    }
    throw error;
  }
}

export { API_BASE_URL };
