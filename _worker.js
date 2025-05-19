import { Hono } from 'hono'
import { handle } from 'hono/vercel'
import { serveStatic } from 'hono/cloudflare-pages'

const app = new Hono()

// Serve static files
app.use('/*', serveStatic({ root: './' }))

// Handle Python application
app.all('*', async (c) => {
  const pythonApp = await import('./app.py')
  return pythonApp.default(c)
})

export default app 