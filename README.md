# Energy and Gas for US

A complete, production-ready energy services platform for electricity and natural gas providers in the United States.

## Company Information

- **Company Name:** Energy and Gas for US
- **Address:** P.O. Box 460008, Houston, TX 77056
- **Business:** Electricity and Natural Gas Services

## Features

### Public Website
- Premium parrot-green/white energy-company UI
- Homepage with hero section and availability checker
- Electricity, Natural Gas, and Plans pages
- ZIP code availability system (database-backed)
- How It Works, Why Us, Energy Saving Tips, FAQ, Contact pages

### Customer Portal
- Secure authentication (login/register)
- Customer dashboard
- My Bills (VIEW-ONLY, NO payment functionality)
- Payment History (VIEW-ONLY)
- My Plan, Energy Usage, Profile, Notifications

### Admin Dashboard
- Secure admin authentication
- Dashboard with analytics
- Customer, enrollment, service area, plan management
- FAQs, testimonials, leads management

## Tech Stack

- **Frontend:** React 19 + TypeScript + Vite + Tailwind CSS
- **Backend:** Node.js + Express + TypeScript
- **Database:** PostgreSQL / Supabase
- **Auth:** JWT with bcryptjs

## Demo Accounts

### Customer
- Email: demo@energygas.local
- Password: Customer123!

### Admin
- Email: admin@energygas.local
- Password: Admin123!

## Quick Start

### Backend
```bash
cd backend
npm install
cp .env.example .env
# Edit .env with your DATABASE_URL
npm run dev
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Important Notes

- **NO PAYMENT FUNCTIONALITY** - Bills and payment history are VIEW-ONLY
- Database schema in `database/schema.sql`
- Seed data in `database/seed/seed.sql`

---

P.O. Box 460008, Houston, TX 77056
