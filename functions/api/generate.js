export async function onRequestPost(context) {
  return new Response(JSON.stringify({ 
    status: "success",
    message: "API endpoint ready" 
  }), {
    headers: { 
      "content-type": "application/json",
      "Access-Control-Allow-Origin": "*"
    }
  });
}

export async function onRequestOptions(context) {
  return new Response(null, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    }
  });
} 