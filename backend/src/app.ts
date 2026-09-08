import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import dotenv from 'dotenv';
import { apiLimiter } from './middleware/rateLimit';
import authRoutes from './routes/auth';
import availabilityRoutes from './routes/availability';
import plansRoutes from './routes/plans';
import customerRoutes from './routes/customer';
import enrollmentsRoutes from './routes/enrollments';
import adminRoutes from './routes/admin';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;
const FRONTEND_URL = process.env.FRONTEND_URL || 'http://localhost:5173';

app.use(helmet());
app.use(cors({ origin: FRONTEND_URL, credentials: true }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(compression());

app.use('/api/auth', authRoutes);
app.use('/api/availability', availabilityRoutes);
app.use('/api/plans', plansRoutes);
app.use('/api/customer', apiLimiter, customerRoutes);
app.use('/api/enrollments', apiLimiter, enrollmentsRoutes);
app.use('/api/admin', apiLimiter, adminRoutes);

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.use((req, res) => {
  res.status(404).json({ success: false, error: 'Route not found' });
});

app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Error:', err);
  res.status(500).json({ success: false, error: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message });
});

export { app, PORT };
