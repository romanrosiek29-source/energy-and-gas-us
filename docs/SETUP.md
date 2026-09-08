# Energy and Gas for US - Setup Guide

## Prerequisites

- Node.js 18+
- PostgreSQL 14+ or Supabase account
- npm or yarn

## Database Setup

### Option 1: Local PostgreSQL

1. Install PostgreSQL 14+
2. Create database:
```bash
createdb energy_gas_us
```

3. Run schema:
```bash
psql -d energy_gas_us < database/schema.sql
```

4. (Optional) Seed data:
```bash
psql -d energy_gas_us < database/seed/seed.sql
```

### Option 2: Supabase

1. Create a new Supabase project at https://supabase.com
2. Go to SQL Editor
3. Paste contents of `database/schema.sql`
4. Run the SQL
5. Copy your database URL from Settings > Database

## Backend Setup

1. Navigate to backend:
```bash
cd backend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Edit `.env`:
```env
PORT=3000
NODE_ENV=development
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/energy_gas_us
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_EXPIRES_IN=7d
FRONTEND_URL=http://localhost:5173
```

5. Start development server:
```bash
npm run dev
```

Backend will be available at: `http://localhost:3000`

## Frontend Setup

1. Navigate to frontend:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```env
VITE_API_URL=http://localhost:3000/api
```

4. Start development server:
```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## Demo Accounts

### Customer Account
- **Email:** demo@energygas.local
- **Password:** Customer123!

### Admin Account
- **Email:** admin@energygas.local  
- **Password:** Admin123!

**Note:** These accounts require the seed data to be loaded into the database.

## Testing the Application

### 1. Test Public Website
- Navigate to `http://localhost:5173`
- Check homepage loads
- Test ZIP code availability checker (try 77056 for Houston, TX)
- Browse Electricity, Natural Gas, and Plans pages

### 2. Test Customer Portal
- Click "My Account" or navigate to `/login`
- Login with demo customer credentials
- View dashboard, bills, payment history
- **Important:** Bills and payment history are VIEW-ONLY (no payment functionality)

### 3. Test Admin Dashboard
- Navigate to `/admin/login`
- Login with admin credentials
- View dashboard, customers, enrollments, service areas, plans

## API Endpoints

### Public Endpoints
- `POST /api/auth/register` - Register new customer
- `POST /api/auth/login` - Login
- `POST /api/availability/check` - Check ZIP code availability
- `GET /api/plans` - Get all active plans

### Customer Endpoints (Authenticated)
- `GET /api/customer/dashboard` - Get dashboard data
- `GET /api/customer/bills` - Get bills (VIEW-ONLY)
- `GET /api/customer/payment-history` - Get payment history (VIEW-ONLY)
- `GET /api/customer/usage` - Get energy usage
- `GET /api/customer/plan` - Get current plan

### Admin Endpoints (Admin Auth Required)
- `GET /api/admin/dashboard` - Get admin dashboard data
- `GET /api/admin/customers` - List customers
- `GET /api/admin/service-areas` - List service areas
- `GET /api/admin/plans` - List plans
- `GET /api/admin/leads` - Get availability leads

See README.md for complete API documentation.

## Production Deployment

### Database (Supabase)
1. Create Supabase project
2. Run schema SQL
3. Copy connection string

### Backend (Render/Railway)
1. Connect your GitHub repository
2. Set root directory to `backend`
3. Set environment variables:
   - `DATABASE_URL` (from Supabase)
   - `JWT_SECRET` (generate secure random string)
   - `FRONTEND_URL` (your frontend URL)
   - `NODE_ENV=production`

### Frontend (Vercel/Netlify)
1. Connect your GitHub repository
2. Set root directory to `frontend`
3. Set environment variable:
   - `VITE_API_URL` (your backend URL)

## Troubleshooting

### Database Connection Errors
- Check DATABASE_URL format
- Ensure PostgreSQL is running
- Check firewall settings

### CORS Errors
- Verify FRONTEND_URL in backend .env matches your frontend URL
- Check CORS configuration in app.ts

### Authentication Issues
- Ensure JWT_SECRET is set
- Check token expiration (JWT_EXPIRES_IN)
- Clear browser localStorage and re-login

## Security Notes

- Change JWT_SECRET in production
- Use HTTPS in production
- Enable rate limiting
- Keep dependencies updated
- Never commit .env files

## Support

For questions or issues, contact your development team.

---

Energy and Gas for US
P.O. Box 460008, Houston, TX 77056
