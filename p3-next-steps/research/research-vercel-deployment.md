---
name: Vercel deployment
type: research
project: P3 — 3D Model Lifecycle Pipeline
date: P3
---

# Research: Vercel Deployment

**Sources:**
1. Vercel official documentation — https://vercel.com/docs
2. Claude (iterative troubleshooting during deployment)

**What was consulted:** Vercel docs for Python/Flask deployment configuration, serverless function constraints, filesystem behavior, and environment variable handling. Claude was consulted when specific errors arose during the deployment process.

**When:** During P3, while deploying the Flask application to Vercel.

**What I took from it:** Understanding of Vercel's serverless constraints — read-only filesystem outside `/tmp/`, 4MB upload limit, cold start behavior, and the requirement to restructure the entry point for serverless execution. These constraints directly shaped the `_IS_VERCEL` environment check in `app.py` and the storage path logic throughout the application.
