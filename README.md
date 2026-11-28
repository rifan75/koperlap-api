# Aplikasi Koperasi Pekerja Lepas Indonesia


Auth PKCE2
React
  |
  | POST /auth/login
  | email + password + state + challenge 
  v
FastAPI
  |
  | Verify credentials
  | Generate authorization code
  v
React
  |
  | Validate state
  | POST /auth/authorize
  | verifier + code
  v
FastAPI
  |
  | Validate PKCE
  | Consume code
  | Resolve RBAC
  | Issue JWT + refresh token
  v
React
  |
  | Store access token
  | Store refresh token
  | Store user
  v
Protected API

For RS256, generate an RSA key pair.
<pre>
mkdir -p secrets

openssl genrsa \
  -out secrets/jwt-private.pem \
  4096

openssl rsa \
  -in secrets/jwt-private.pem \
  -pubout \
  -out secrets/jwt-public.pem
</pre>

chmod 600 secrets/jwt-private.pem
chmod 644 secrets/jwt-public.pem



Identity & Membership

users

roles

permissions

members

member_documents

member_status_histories

Savings & Finance

savings_accounts

savings_transactions

accounts

journal_entries

journal_lines

payment_transactions

Loans

loan_products

loan_applications

loans

loan_installments

loan_payments

Freelance Ecosystem

projects

project_applications

project_contracts

project_payments

member_skills

Cooperative Governance

cooperative_settings

annual_financial_reports

shu_periods

shu_distributions

general_meetings

meeting_decisions