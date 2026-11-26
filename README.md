# Aplikasi Koperasi Pekerja Lepas Indonesia
Struktur Kode  :
koperasi-backend/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py
│   │   ├── exceptions.py
│   │   ├── permissions.py
│   │   ├── constants.py
│   │   └── logging.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── session.py
│   │   ├── base.py
│   │   └── dependencies.py
│   │
│   ├── common/
│   │   ├── __init__.py
│   │   ├── pagination.py
│   │   ├── response.py
│   │   ├── enums.py
│   │   └── utils.py
│   │
│   ├── modules/
│   │   │
│   │   ├── auth/
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── service.py
│   │   │   └── dependencies.py
│   │   │
│   │   ├── client/
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── service.py
│   │   │
│   │   ├── members/
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── service.py
│   │   │
│   │   ├── admin/
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── service.py
│   │   │
│   │   ├── savings/
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── service.py
│   │   │
│   │   ├── loans/
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── service.py
│   │   │
│   │   ├── transactions/
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── service.py
│   │   │
│   │   ├── projects/
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── service.py
│   │   │
│   │   ├── shu/
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── service.py
│   │   │
│   │   ├── reports/
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   │
│   │   └── notifications/
│   │       ├── router.py
│   │       ├── schemas.py
│   │       └── service.py
│   │
│   └── integrations/
│       ├── payment_gateway/
│       ├── email/
│       ├── whatsapp/
│       └── storage/
│
├── migrations/
│   └── versions/
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
│
├── scripts/
│   ├── seed.py
│   └── create_admin.py
│
├── docker/
│   └── Dockerfile
│
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── pyproject.toml
└── README.md



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