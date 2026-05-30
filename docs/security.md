# Security Documentation

## 1. Password Hashing
- Algorithm: bcrypt with 12 salt rounds
- Library: bcrypt (Python)
- All passwords hashed before storing in database
- Timing-safe comparison using bcrypt.checkpw()

## 2. Authentication — JWT Tokens
- Library: PyJWT
- Algorithm: HS256
- Token contains: user_id, role
- Secret stored in environment variable (JWT_SECRET)
- Token passed via Authorization: Bearer header

## 3. SQL Injection Prevention
- ORM: SQLAlchemy
- All queries use parameterized statements automatically
- No raw SQL queries used anywhere in the application
- Input validation on all API endpoints

## 4. XSS Prevention
- Jinja2 auto-escaping enabled for all templates
- Content-Security-Policy header: default-src 'self'
- X-XSS-Protection: 1; mode=block header set in Nginx

## 5. Security Headers
- X-Frame-Options: DENY (prevents clickjacking)
- X-Content-Type-Options: nosniff
- Strict-Transport-Security: max-age=31536000
- Content-Security-Policy: default-src 'self'
- Referrer-Policy: strict-origin-when-cross-origin

## 6. Rate Limiting
- Nginx rate limiting: 10 requests/second per IP
- Login endpoint: 5 requests/minute per IP
- Burst allowance: 20 requests

## 7. Firewall — UFW
- Port 22: SSH (bastion only)
- Port 80: HTTP
- Port 443: HTTPS
- All other ports: DENY

## 8. Brute Force Protection — Fail2ban
- Max retries: 3
- Ban time: 3600 seconds (1 hour)
- Find time: 600 seconds
- Monitors: /var/log/auth.log

## 9. RBAC — Role Based Access Control
- Roles: user, admin
- JWT payload contains role
- Admin routes protected by admin_required decorator
- User routes protected by token_required decorator

## 10. SSH Hardening
- Root login disabled: PermitRootLogin no
- Password auth disabled: PasswordAuthentication no
- Key-based auth only
- Bastion host as jump server
