# Setting Up the Project Locally

This guide provides all required steps to run the project locally — including environment variable setup, expected formats, and where to obtain the necessary credentials.

---

## 1. Prerequisites

Make sure you have the following installed:

- **Node.js** (v18 or later)
- **npm** (v9 or later)
- Access to **MongoDB Atlas**
- Access to **Clerk Dashboard** for authentication keys

Install project dependencies:

```bash
npm install
```

---

## 2. Environment Variables

Create a file named **`.env.local`** at the root of the project:

```bash
touch .env.local
```

Add the following variables:

```env
# MongoDB Atlas connection string
MONGODB_URI=""

# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=""
CLERK_SECRET_KEY=""

# App URL for Clerk redirects
NEXT_PUBLIC_BASE_URL="http://localhost:3000"
```

---

## 3. Expected Values and Formats

### **MONGODB_URI**
A valid MongoDB Atlas connection string.

**Format:**
```
mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/todo?retryWrites=true&w=majority
```

**Where to get it:**
1. Go to **MongoDB Atlas → Database**
2. Click **Connect**
3. Choose **Drivers**
4. Copy the connection string
5. Replace `<username>`, `<password>`, and the database name if needed

---

### **NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY**
Frontend key required by Clerk.

**Format example:**
```
pk_test_1234567890abcdefghijkl
```

**Where to get it:**
- Clerk Dashboard → Your Project → **API Keys** → Publishable Key

---

### **CLERK_SECRET_KEY**
Backend secret used to validate Clerk sessions.

**Format example:**
```
sk_test_abcdefghijklmnopqrstuvwxyz123456
```

**Where to get it:**
- Clerk Dashboard → API Keys → **Secret Key**

---

### **NEXT_PUBLIC_BASE_URL**
URL used for Clerk callback redirects during development.

Default:
```
http://localhost:3000
```

Leave unchanged unless running the app on a different port.

---

## 4. Running the Project

Start the development server:

```bash
npm run dev
```

Visit the app in your browser:

```
http://localhost:3000
```

---

## 5. Troubleshooting

### **MongoDB connection errors**
- Ensure your `MONGODB_URI` is valid.
- Whitelist your local machine IP in **Atlas → Network Access**.

### **Clerk authentication errors**
- Missing or incorrect `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` or `CLERK_SECRET_KEY`.
- Make sure **BASE_URL** matches Clerk redirect URLs.

---

## 6. Updating This File

If you add new environment variables or modify project setup, update this document immediately to keep onboarding smooth for new contributors.

---
