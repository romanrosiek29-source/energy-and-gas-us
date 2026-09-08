# PythonAnywhere Deployment Guide

## Quick Setup

1. **Sign up for PythonAnywhere**
   - Go to https://www.pythonanywhere.com
   - Create a free account

2. **Create a Web App**
   - Go to Web tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.10

3. **Configure WSGI File**
   - Click on the WSGI configuration file link
   - Replace contents with `wsgi.py` from this folder
   - Update paths and environment variables

4. **Set Up Database**
   - Go to Databases tab
   - Create a MySQL or PostgreSQL database
   - Note your database credentials
   - Update `DATABASE_URL` in WSGI file

5. **Upload Code**
   - Go to Files tab
   - Upload `app.py` and `requirements.txt`
   - Or clone from GitHub using Bash console:
   ```bash
   git clone https://github.com/romanrosiek29-source/energy-and-gas-us.git
   ```

6. **Install Dependencies**
   - Go to Bash console
   - Run:
   ```bash
   pip install -r --user pythonanywhere/requirements.txt
   ```

7. **Configure Web App**
   - Go back to Web tab
   - Set Source code to: `/home/yourusername/energy-and-gas-us/pythonanywhere`
   - Set Working directory to: `/home/yourusername/energy-and-gas-us/pythonanywhere`
   - Update WSGI configuration file path

8. **Set Environment Variables**
   - In Web tab, add environment variables:
     - `DATABASE_URL`: Your database connection string
     - `JWT_SECRET`: Your secret key
     - `FRONTEND_URL`: Your PythonAnywhere URL

9. **Reload the App**
   - Click the green "Reload" button

10. **Access Your App**
    - Your app will be at: `https://yourusername.pythonanywhere.com`

## Database Setup on PythonAnywhere

### MySQL (Default)
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@hostname/databasename'
```

### PostgreSQL (Paid)
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@hostname/databasename'
```

## Frontend Configuration

Update frontend `.env`:
```env
VITE_API_URL=https://yourusername.pythonanywhere.com/api
```

Then deploy frontend to:
- Vercel: https://vercel.com
- Netlify: https://netlify.com
- Or PythonAnywhere static files

## Important Notes

- Free tier has limited CPU and storage
- App sleeps after inactivity (paid tier avoids this)
- Use external database for production
- Update CORS origins in `app.py`

## Demo Accounts

- Customer: demo@energygas.local / Customer123!
- Admin: admin@energygas.local / Admin123!

## Troubleshooting

### App Not Loading
- Check error log in Web tab
- Verify WSGI file path
- Check database connection

### CORS Errors
- Update CORS origins in `app.py`
- Ensure FRONTEND_URL is set correctly

### Database Errors
- Verify connection string
- Check database credentials
- Ensure tables are created

## Support

For PythonAnywhere-specific issues:
- Help pages: https://help.pythonanywhere.com/
- Forums: https://www.pythonanywhere.com/forums/
