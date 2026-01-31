# Todo Frontend Application

A Next.js frontend application for the Todo web application with authentication and task management.

## Getting Started
alembic revision --autogenerate -m "create users table"


First, install the dependencies:

```bash
npm install
```

Next, set up your environment variables by copying the example:

```bash
cp .env.example .env.local
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: The base URL for the backend API (default: http://localhost:8000)
- `NEXT_PUBLIC_BETTER_AUTH_URL`: The URL for the Better Auth service (default: http://localhost:8000)

## Available Scripts

- `npm run dev`: Runs the app in development mode
- `npm run build`: Builds the app for production
- `npm run start`: Starts the production build
- `npm run lint`: Runs the linter

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── (auth)/          # Authentication-related pages
│   │   │   ├── login/
│   │   │   ├── signup/
│   │   │   └── layout.tsx
│   │   ├── dashboard/       # Main task management area
│   │   │   ├── page.tsx
│   │   │   ├── tasks/
│   │   │   │   ├── [id]/
│   │   │   │   └── new/
│   │   │   └── layout.tsx
│   │   ├── globals.css      # Global styles
│   │   ├── layout.tsx       # Root layout
│   │   └── page.tsx         # Home page
│   ├── components/          # Reusable UI components
│   │   ├── ui/              # Base UI components (buttons, inputs, etc.)
│   │   ├── auth/            # Authentication components
│   │   ├── tasks/           # Task management components
│   │   │   ├── TaskCard.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── TaskList.tsx
│   │   └── layout/          # Layout components
│   ├── services/            # API clients and business logic
│   │   ├── api-client.ts    # API client with JWT handling
│   │   ├── auth-service.ts  # Authentication management
│   │   └── task-service.ts  # Task-related API calls
│   ├── hooks/               # Custom React hooks
│   │   ├── useAuth.ts       # Authentication state management
│   │   ├── useTasks.ts      # Task data management
│   │   └── useApi.ts        # Generic API hook
│   ├── lib/                 # Utility functions
│   │   ├── utils.ts         # General utilities
│   │   └── constants.ts     # Application constants
│   └── types/               # TypeScript type definitions
│       ├── auth.ts          # Authentication types
│       ├── task.ts          # Task types
│       └── api.ts           # API response types
├── public/                  # Static assets
├── .env.example             # Environment variables template
├── next.config.js           # Next.js configuration
├── tailwind.config.js       # Tailwind CSS configuration
├── tsconfig.json            # TypeScript configuration
└── package.json             # Dependencies and scripts
```

## Features

- Authentication with login and signup
- Task management (create, read, update, delete, toggle completion)
- JWT-based authentication
- Responsive design
- Error handling and loading states
- Optimistic updates for better UX

## Learn More

To learn more about the technologies used in this project:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [React Documentation](https://reactjs.org/) - learn about React concepts.
- [Tailwind CSS](https://tailwindcss.com/) - learn about Tailwind CSS utility-first framework.
- [TypeScript](https://www.typescriptlang.org/) - learn about TypeScript.