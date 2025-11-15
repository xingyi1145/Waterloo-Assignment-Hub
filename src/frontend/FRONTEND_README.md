# Frontend - Waterloo CS Assignment Hub

React + TypeScript frontend for the Waterloo CS Assignment Hub.

## 🚀 Quick Start

```bash
cd src/frontend
npm install
npm run dev
```

App runs at `http://localhost:5173`

## 📁 Structure

- `api.ts` - API client
- `types.ts` - TypeScript types
- `AuthContext.tsx` - Auth state management
- `pages/` - All page components
- `components/` - Reusable components

## ✅ Features Complete

✅ User authentication (login/signup)
✅ Course browsing & creation (professors)
✅ Assignment & question management
✅ Solution submission with code editor
✅ Solution viewing, likes, and comments
✅ Role-based access control
✅ Responsive design

## 🔧 Backend Connection

Ensure FastAPI backend runs on `http://localhost:8000` before starting frontend.

## 📝 Key Pages

- `/` - Home
- `/login` - Login
- `/signup` - Signup  
- `/courses` - Course list
- `/courses/:id` - Course detail
- `/assignments/:id` - Assignment detail
- `/questions/:id` - Question & solutions
- `/solutions/:id` - Solution detail

All routes except home/login/signup require authentication.
