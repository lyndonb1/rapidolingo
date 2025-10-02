# RápidoLingo Frontend

Next.js 14 frontend for RápidoLingo - AI Spanish Tutor

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
Create `.env.local` file with:
```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_key
CLERK_SECRET_KEY=your_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Run development server:
```bash
npm run dev
```

## Features

- ✅ Landing page with Clerk authentication
- ✅ Onboarding flow (3 steps)
- ✅ Dashboard with lesson cards
- ✅ Responsive design with Tailwind CSS
- 🚧 LiveKit tutoring interface (next)

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Clerk Auth
- LiveKit Components
- Axios

## Pages

- `/` - Landing page
- `/onboarding` - User setup
- `/dashboard` - Lesson selection
- `/tutoring` - Live voice sessions

## Backend API

Connects to FastAPI backend at `http://localhost:8000`

Endpoints used:
- `GET /api/lessons` - Fetch available lessons
- `POST /api/session/start` - Create LiveKit session
- `POST /api/session/end` - End session

