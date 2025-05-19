import { Hono } from 'hono'
import { serveStatic } from 'hono/cloudflare-pages'

const app = new Hono()

// Serve static files from the public directory
app.use('/*', serveStatic({ root: './public' }))

// Handle Python application
app.all('*', async (c) => {
  try {
    const pythonApp = await import('./app.py')
    return pythonApp.export(c.req)
  } catch (error) {
    console.error('Error handling request:', error)
    return new Response('Internal Server Error', { status: 500 })
  }
})

export default app 