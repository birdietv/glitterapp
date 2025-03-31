export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Construct the backend URL (change this to your actual backend URL once deployed)
    const backendUrl = new URL(request.url);
    backendUrl.hostname = 'your-app-name.your-username.workers.dev';
    
    // Forward the request to the backend
    return fetch(new Request(backendUrl, request));
  }
}; 