# Digital Evidence Management System

A secure web-based system for law enforcement officers to upload, manage, and share digital evidence.

## Features

- Role-based access control (RBAC)
- Immutable evidence storage
- Tamper-proof evidence tracking with hash verification
- Comprehensive audit trail
- High-speed video streaming
- Secure file sharing

## Technical Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Django
- Database: MongoDB
- File Storage: AWS S3 (configurable)

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
MONGODB_URI=your-mongodb-uri
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Security Features

- SHA-256/Ed25519 hash verification
- Immutable file storage
- Role-based access control
- Comprehensive audit logging
- Secure file sharing with expiration
- Video streaming without download

## License

This project is licensed under the MIT License - see the LICENSE file for details. 