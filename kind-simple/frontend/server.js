const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const port = 3000;

// Proxy API requests to the backend service
app.use('/api', createProxyMiddleware({
    target: 'http://backend-service.demo-app.svc.cluster.local', // Target backend service in Kubernetes
    changeOrigin: true,
    pathRewrite: {
        '^/api': '/api', // The path rewrite is to keep the /api prefix when forwarding
    },
    onProxyReq: (proxyReq, req, res) => {
        console.log(`[Proxy] Forwarding request to: ${proxyReq.path}`);
    },
    onError: (err, req, res) => {
        console.error('[Proxy] Error:', err);
        res.writeHead(500, {
            'Content-Type': 'text/plain',
        });
        res.end('Something went wrong with the proxy.');
    }
}));

// Serve static files from the 'public' directory
app.use(express.static(__dirname));

// Send the main index.html file for any other requests
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(port, () => {
    console.log(`Frontend server listening at http://localhost:${port}`);
});
