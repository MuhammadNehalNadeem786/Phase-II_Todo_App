---
name: auth-skill
description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication System Skill

## Instructions

1. **User Signup**
   - Collect email and password
   - Validate input fields (email format, password strength)
   - Hash password before saving using bcrypt or argon2
   - Store user in database
   - Prevent duplicate users

2. **User Signin**
   - Verify email exists
   - Compare provided password with hashed password
   - Generate JWT token on successful login
   - Return meaningful error messages without leaking info

3. **JWT Tokens**
   - Create JWT tokens with expiration
   - Include user ID and role in payload
   - Use a secret key stored in environment variables
   - Middleware to verify JWT on protected routes

4. **Protected Routes & Authorization**
   - Implement middleware to restrict access based on JWT
   - Role-based access control (e.g., user, admin)
   - Example: `/profile` route accessible to authenticated users only
   - Example: `/admin` route accessible only to admin role

5. **Better Auth Integration**
   - Setup Better Auth in the project
   - Configure authentication providers
   - Handle session and token securely
   - Replace manual JWT logic with Better Auth where appropriate

6. **Security Best Practices**
   - Input validation to prevent injection attacks
   - Do not store plain text passwords
   - Use HTTPS for API calls
   - Rate limiting to prevent brute-force attacks
   - Proper error handling without leaking sensitive information

## Deliverables
- Fully functional authentication system
- Signup and signin endpoints
- JWT-based protected routes
- Better Auth integration
- Secure password handling
- Example requests and responses in documentation
