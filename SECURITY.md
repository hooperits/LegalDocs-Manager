# Security Policy

Thank you for helping keep **LegalDocs Manager** secure. We take the security of our application, clients, cases, and documents very seriously. 

This document outlines our supported versions, vulnerability reporting process, existing security controls, and scope for security research.

> [!TIP]
> The canonical version of this security policy is maintained in the [.github/SECURITY.md](.github/SECURITY.md) file.

---

## Supported Versions

Currently, security updates are actively provided for the following versions of **LegalDocs Manager**:

| Version | Supported | Notes |
| ------- | :---: | ----- |
| **1.0.x** | :white_check_mark: | Active stable branch |
| **< 1.0** | :x: | Development and pre-release versions (Deprecated) |

> [!NOTE]
> We recommend always running the latest patch release of the `1.0.x` branch and ensuring your dependencies (especially Django) are kept up to date.

---

## Reporting a Vulnerability

If you discover a security vulnerability in this project, **please do not report it publicly** (do not open a GitHub Issue or Pull Request). Instead, report it privately so we can address it responsibly.

### How to Report

1. Send an email to [security@hooperits.com](mailto:security@hooperits.com) with the details of the vulnerability.
2. In your report, please include:
   - A detailed description of the vulnerability and its potential impact.
   - Step-by-step instructions (or a Proof of Concept script/exploit) to reproduce the issue.
   - Any details about your environment or configuration.

### What to Expect

- **Acknowledgement**: You will receive an initial response acknowledging your report within **48 hours**.
- **Investigation**: We will investigate the issue and keep you updated as we work on a fix.
- **Resolution**: We aim to resolve verified vulnerabilities within **30 days** of receiving the report.
- **Disclosure**: Once a fix is deployed, we will coordinate the public disclosure of the vulnerability with you, giving you full credit for the discovery if desired.

---

## Existing Security Controls

To assist security researchers and administrators, here is a summary of the security controls already built into **LegalDocs Manager**:

### 1. Authentication & Authorization
- **Token-Based Authentication**: Django REST Framework (DRF) tokens are required for all API endpoints.
- **Object-Level Permissions**: Access to document deletion is restricted to the document owner (`uploaded_by`) or staff administrators via custom permission classes.

### 2. File Upload Security
- **Strict MIME Validation**: File type validation is enforced on upload using `python-magic` to inspect file headers (magic bytes), preventing bypasses using renamed extensions.
- **Size Limitation**: File uploads are capped at a maximum of **10 MB** (`MAX_UPLOAD_SIZE`).
- **Secure Object Storage**: Integration with AWS S3 / MinIO ensures all uploaded documents are stored in a private bucket. Direct downloads are served exclusively via secure pre-signed URLs that automatically expire in **1 hour** (`querystring_auth=True`).

### 3. Rate Limiting & Protection
- **Brute Force Lockout**: Integrated with `django-axes` to protect against login brute force. Accounts are locked out based on a combination of username and IP address after **5 failed attempts** for a duration of **15 minutes**.
- **DRF Throttling**:
  - **Anonymous Users**: 100 requests/day.
  - **Authenticated Users**: 1,000 requests/day.
  - **Authentication Endpoints** (Login/Register): 5 requests/minute.
  - **Global Search**: 30 requests/minute.

### 4. Production Security Headers
In production (`DEBUG=False`), the following headers and security policies are enforced:
- **HSTS (HTTP Strict Transport Security)**: Enforced for 1 year, including subdomains and preloading.
- **Secure Cookies**: Session and CSRF cookies are flagged as `Secure` (transmitted over HTTPS only).
- **Security Headers**: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, and `X-XSS-Protection` are fully enabled.

---

## Scope & Guidelines

### In-Scope
We are particularly interested in reports related to:
- Authentication bypass or privilege escalation.
- Document upload validation bypass (e.g., uploading executable files or unauthorized formats).
- Access control bypass on private documents or client/case records.
- SQL injection or Remote Code Execution (RCE).

### Out-of-Scope
The following are considered out of scope:
- Vulnerabilities in third-party libraries (e.g., Django, Python libraries) unless they are caused by our specific implementation or configuration.
- Denial of Service (DoS) or Distributed Denial of Service (DDoS) attacks.
- Social engineering or physical security attacks.
- Brute force reports on authentication endpoints that do not bypass `django-axes` or rate limiting.
