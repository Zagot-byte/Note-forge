<!-- filename: active-directory-{room-slug}-{YYYY-MM-DD}.md -->

# {Room Name} — Active Directory

| Field      | Value              |
|------------|--------------------|
| Type       | Active Directory   |
| Date       | {YYYY-MM-DD}       |
| Domain     | {domain.local}     |
| Difficulty | {difficulty}       |
| Tags       | {tag1, tag2}       |

---

## Environment

| Role          | Hostname | IP  |
|---------------|----------|-----|
| DC            |          |     |
| Workstation   |          |     |

---

## Enumeration

```bash
# BloodHound ingestor
bloodhound-python -u {user} -p {pass} -d {domain} -ns {dc-ip} -c All

# ldapdomaindump
ldapdomaindump -u '{domain}\{user}' -p {pass} {dc-ip}

# enum4linux
enum4linux -a {dc-ip}
```

---

## Attacks

### {Attack Name — e.g. Kerberoasting}

```bash

```

### {Attack Name — e.g. AS-REP Roasting}

```bash

```

---

## Lateral Movement

```bash
# Pass-the-Hash / Pass-the-Ticket / WinRM / etc
```

---

## Persistence

```bash
# Golden ticket, DCSync, scheduled task, etc
```

---

## Key Takeaways

- 
- 
- 

---

## References

- 
