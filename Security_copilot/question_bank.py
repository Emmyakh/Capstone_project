# question_bank.py
# SME-friendly questionnaire mapped to OWASP Top 10 (2021) and OWASP ASVS (Level 1) control areas.
# Answer options expected by scoring.py: yes / no / not_sure / managed

QUESTIONS = [
    # =========================
    # A01: Broken Access Control
    # =========================
    {
        "id": "Q1.1",
        "section": "Accounts & Access Control",
        "text": "Can staff only access information and features needed for their job role?",
        "owasp": "A01 Broken Access Control",
        "asvs": "V4 Access Control (L1)",
        "weight": 5,
        "remediation": "Implement role-based access control (RBAC) and verify permissions server-side for every request."
    },
    {
        "id": "Q1.2",
        "section": "Accounts & Access Control",
        "text": "When someone leaves the company, is their access removed immediately?",
        "owasp": "A01 Broken Access Control",
        "asvs": "V4 Access Control (L1)",
        "weight": 4,
        "remediation": "Use an offboarding checklist and disable accounts immediately; review access rights regularly."
    },
    {
        "id": "Q1.3",
        "section": "Accounts & Access Control",
        "text": "Is access to admin features restricted to trusted staff only?",
        "owasp": "A01 Broken Access Control",
        "asvs": "V4 Access Control (L1)",
        "weight": 5,
        "remediation": "Restrict admin endpoints, require re-authentication for sensitive actions, and enforce least privilege."
    },

    # =========================================
    # A02: Cryptographic Failures (Data Protection)
    # =========================================
    {
        "id": "Q2.1",
        "section": "Customer Data Protection",
        "text": "Does your website show a padlock (HTTPS) in the browser at all times?",
        "owasp": "A02 Cryptographic Failures",
        "asvs": "V9 Communications (L1)",
        "weight": 5,
        "remediation": "Enable HTTPS site-wide, redirect HTTP to HTTPS, and enable HSTS."
    },
    {
        "id": "Q2.2",
        "section": "Customer Data Protection",
        "text": "Are customer passwords stored securely (not visible in plain text)?",
        "owasp": "A02 Cryptographic Failures",
        "asvs": "V2 Authentication (L1)",
        "weight": 5,
        "remediation": "Hash passwords using a strong algorithm (e.g., bcrypt/Argon2) and never store plain text passwords."
    },
    {
        "id": "Q2.3",
        "section": "Customer Data Protection",
        "text": "Are sensitive customer records encrypted or securely stored?",
        "owasp": "A02 Cryptographic Failures",
        "asvs": "V8 Data Protection (L1)",
        "weight": 4,
        "remediation": "Encrypt sensitive data at rest and use secure storage with access controls; minimise stored sensitive data."
    },

    # ======================
    # A03: Injection
    # ======================
    {
        "id": "Q3.1",
        "section": "Input & Form Security",
        "text": "Has your website been tested to prevent malicious input in forms (e.g., SQL injection)?",
        "owasp": "A03 Injection",
        "asvs": "V5 Validation & Encoding (L1)",
        "weight": 5,
        "remediation": "Use server-side validation and parameterised queries; avoid building SQL with string concatenation."
    },
    {
        "id": "Q3.2",
        "section": "Input & Form Security",
        "text": "Do developers use safe database access methods (e.g., parameterised queries/ORM)?",
        "owasp": "A03 Injection",
        "asvs": "V5 Validation & Encoding (L1)",
        "weight": 5,
        "remediation": "Adopt prepared statements/ORM and validate inputs; implement allow-lists for critical fields."
    },
    {
        "id": "Q3.3",
        "section": "Input & Form Security",
        "text": "Are file uploads restricted to safe file types and scanned if needed?",
        "owasp": "A03 Injection",
        "asvs": "V12 Files and Resources (L1)",
        "weight": 4,
        "remediation": "Restrict file types, enforce size limits, store uploads outside web root, and scan uploads when appropriate."
    },

    # ======================
    # A04: Insecure Design
    # ======================
    {
        "id": "Q4.1",
        "section": "Development & Design Security",
        "text": "Was security considered during the design of the website or application?",
        "owasp": "A04 Insecure Design",
        "asvs": "V1 Architecture (L1)",
        "weight": 4,
        "remediation": "Use threat modelling (e.g., STRIDE) and security requirements early in design."
    },
    {
        "id": "Q4.2",
        "section": "Development & Design Security",
        "text": "Are risky features (admin panels, uploads, payments) designed with extra security controls?",
        "owasp": "A04 Insecure Design",
        "asvs": "V1 Architecture (L1)",
        "weight": 4,
        "remediation": "Apply secure design patterns, rate limiting, strong auth, and additional verification for high-risk functions."
    },
    {
        "id": "Q4.3",
        "section": "Development & Design Security",
        "text": "Are security requirements documented and reviewed before changes go live?",
        "owasp": "A04 Insecure Design",
        "asvs": "V1 Architecture (L1)",
        "weight": 3,
        "remediation": "Define security requirements and conduct design reviews for major changes."
    },

    # ===========================
    # A05: Security Misconfiguration
    # ===========================
    {
        "id": "Q5.1",
        "section": "Website Security & Maintenance",
        "text": "Are default usernames/passwords changed after installation?",
        "owasp": "A05 Security Misconfiguration",
        "asvs": "V14 Configuration (L1)",
        "weight": 4,
        "remediation": "Change default credentials, disable unused accounts, and remove unnecessary services."
    },
    {
        "id": "Q5.2",
        "section": "Website Security & Maintenance",
        "text": "Are secure cookie settings enabled (Secure, HttpOnly, SameSite)?",
        "owasp": "A05 Security Misconfiguration",
        "asvs": "V3 Session Management (L1)",
        "weight": 4,
        "remediation": "Set Secure/HttpOnly/SameSite cookies and enforce session timeouts and CSRF protections."
    },
    {
        "id": "Q5.3",
        "section": "Website Security & Maintenance",
        "text": "Are error messages user-friendly and do they avoid revealing technical details?",
        "owasp": "A05 Security Misconfiguration",
        "asvs": "V7 Error Handling & Logging (L1)",
        "weight": 3,
        "remediation": "Disable verbose errors in production; log details internally and show generic messages to users."
    },

    # ====================================
    # A06: Vulnerable and Outdated Components
    # ====================================
    {
        "id": "Q6.1",
        "section": "Website Security & Maintenance",
        "text": "Are your website software, plugins, and frameworks updated regularly?",
        "owasp": "A06 Vulnerable and Outdated Components",
        "asvs": "V1 Architecture (L1)",
        "weight": 5,
        "remediation": "Maintain patch schedules, track dependencies, and update frameworks/plugins promptly."
    },
    {
        "id": "Q6.2",
        "section": "Website Security & Maintenance",
        "text": "Do you know what third-party libraries/plugins your website depends on?",
        "owasp": "A06 Vulnerable and Outdated Components",
        "asvs": "V1 Architecture (L1)",
        "weight": 4,
        "remediation": "Create a software bill of materials (SBOM) or dependency list and review it regularly."
    },
    {
        "id": "Q6.3",
        "section": "Website Security & Maintenance",
        "text": "Are critical security updates applied quickly when notified?",
        "owasp": "A06 Vulnerable and Outdated Components",
        "asvs": "V1 Architecture (L1)",
        "weight": 4,
        "remediation": "Define SLA for patching critical vulnerabilities and test updates in staging before production."
    },

    # ============================================
    # A07: Identification & Authentication Failures
    # ============================================
    {
        "id": "Q7.1",
        "section": "Accounts & Access Control",
        "text": "Are admin accounts protected with stronger security (e.g., MFA)?",
        "owasp": "A07 Identification & Authentication Failures",
        "asvs": "V2 Authentication (L1)",
        "weight": 5,
        "remediation": "Enable MFA for admin and privileged accounts; enforce strong password policies."
    },
    {
        "id": "Q7.2",
        "section": "Accounts & Access Control",
        "text": "Does the system block or slow repeated failed login attempts?",
        "owasp": "A07 Identification & Authentication Failures",
        "asvs": "V2 Authentication (L1)",
        "weight": 4,
        "remediation": "Implement rate limiting, lockout thresholds, and monitoring for brute-force attempts."
    },
    {
        "id": "Q7.3",
        "section": "Accounts & Access Control",
        "text": "Do user sessions automatically log out after inactivity?",
        "owasp": "A07 Identification & Authentication Failures",
        "asvs": "V3 Session Management (L1)",
        "weight": 3,
        "remediation": "Set session timeouts and implement secure session handling."
    },

    # ======================
    # A08: Software & Data Integrity Failures
    # ======================
    {
        "id": "Q8.1",
        "section": "Development & Deployment",
        "text": "Are software updates reviewed or tested before being deployed?",
        "owasp": "A08 Software and Data Integrity Failures",
        "asvs": "V1 Architecture (L1)",
        "weight": 4,
        "remediation": "Use staging environments and approval steps; apply change control for production releases."
    },
    {
        "id": "Q8.2",
        "section": "Development & Deployment",
        "text": "Are backups performed regularly and tested for restoration?",
        "owasp": "A08 Software and Data Integrity Failures",
        "asvs": "V1 Architecture (L1)",
        "weight": 5,
        "remediation": "Perform regular backups, test restores, and store backups securely and separately."
    },
    {
        "id": "Q8.3",
        "section": "Development & Deployment",
        "text": "Are external scripts/plugins from third parties only loaded from trusted sources?",
        "owasp": "A08 Software and Data Integrity Failures",
        "asvs": "V14 Configuration (L1)",
        "weight": 3,
        "remediation": "Restrict third-party scripts, use integrity checks (SRI) where possible, and review vendors."
    },

    # ======================================
    # A09: Security Logging & Monitoring Failures
    # ======================================
    {
        "id": "Q9.1",
        "section": "Monitoring & Incident Response",
        "text": "Are login attempts and suspicious activities logged?",
        "owasp": "A09 Security Logging & Monitoring Failures",
        "asvs": "V7 Error Handling & Logging (L1)",
        "weight": 5,
        "remediation": "Log authentication events, admin actions, and suspicious requests with timestamps and context."
    },
    {
        "id": "Q9.2",
        "section": "Monitoring & Incident Response",
        "text": "Do you receive alerts for unusual login activity or errors?",
        "owasp": "A09 Security Logging & Monitoring Failures",
        "asvs": "V7 Error Handling & Logging (L1)",
        "weight": 4,
        "remediation": "Enable alerting for brute-force attempts, spikes in errors, and admin access anomalies."
    },
    {
        "id": "Q9.3",
        "section": "Monitoring & Incident Response",
        "text": "Do you have a plan in case your website gets hacked (incident response plan)?",
        "owasp": "A09 Security Logging & Monitoring Failures",
        "asvs": "V1 Architecture (L1)",
        "weight": 4,
        "remediation": "Create an incident response plan including containment, recovery, and communication steps."
    },

    # ======================
    # A10: Server-Side Request Forgery (SSRF)
    # ======================
    {
        "id": "Q10.1",
        "section": "External Connections & Integrations",
        "text": "Does your website connect to other internal services or fetch external URLs on the server side?",
        "owasp": "A10 Server-Side Request Forgery (SSRF)",
        "asvs": "V12 Files and Resources (L1)",
        "weight": 4,
        "remediation": "Audit server-side URL fetching features and restrict outbound requests using allow-lists."
    },
    {
        "id": "Q10.2",
        "section": "External Connections & Integrations",
        "text": "Are external integrations restricted to trusted sources only?",
        "owasp": "A10 Server-Side Request Forgery (SSRF)",
        "asvs": "V12 Files and Resources (L1)",
        "weight": 4,
        "remediation": "Use allow-lists for domains/IPs, block internal IP ranges, and validate/normalise URLs."
    },
    {
        "id": "Q10.3",
        "section": "External Connections & Integrations",
        "text": "Are API keys and integration credentials stored securely (not hardcoded in code)?",
        "owasp": "A10 Server-Side Request Forgery (SSRF)",
        "asvs": "V14 Configuration (L1)",
        "weight": 5,
        "remediation": "Store secrets in environment variables/secret managers and restrict access; rotate keys regularly."
    },
]