import { app, PORT } from './app';
import pool from './database';

async function startServer() {
  try {
    await pool.query('SELECT NOW()');
    console.log('Database connection established');
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
      console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

startServer();
