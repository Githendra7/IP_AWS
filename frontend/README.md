# ProtoStruc: Frontend Repository

This contains the presentation logic for the ProtoStruc dashboard. It utilizes a stateful edge-rendered approach built entirely on Next.js 14 and TailwindCSS. 

## Development Setup

The UI strictly relies on standard Node/NPM architecture. 

```bash
# 1. Install packages
npm install

# 2. Assign environment variables inside `.env.local`
# NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api

# 3. Boot the local server
npm run dev
```

Visit `http://localhost:3000` to interact with the environment. Next.js natively handles hot-module reloads for immediate UI feedback.

## Key Directories

* `/src/app/`: The Next.js App Router layer where all layouts, phase views, and authentication structures map to URLs.
* `/src/components/`: Houses internal React components, ranging from small UI primitives (like standard ShadCN elements) to complex modules like our collapsible navigation `Sidebar.tsx`.
* `/src/lib/api.ts`: **Core SDK File**. All endpoints leading into the backend architecture must be statically typed and invoked strictly from this centralized handler file.

## Styling Syntax
Do NOT use custom overarching CSS parameters unless completely unavoidable. The application leverages pure utility-based Tailwind classes to establish grids, mobile responsiveness, and dark-mode implementations.

For UI animations, leverage Framer Motion (`motion.div`) hooks already present in the UI layers.
