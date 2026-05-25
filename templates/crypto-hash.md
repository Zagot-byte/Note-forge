<!-- filename: crypto-hash-{room-slug}-{YYYY-MM-DD}.md -->

# {Room Name} — Crypto / Hash

| Field      | Value         |
|------------|---------------|
| Type       | Crypto/Hash   |
| Date       | {YYYY-MM-DD}  |
| Difficulty | {difficulty}  |
| Tags       | {tag1, tag2}  |

---

## Hash Identification

| Hash          | Type     | Length | Tool Used |
|---------------|----------|--------|-----------|
|               |          |        |           |

```bash
hashid '{hash}'
hash-identifier
```

---

## Cracking Workflow

```bash
# hashcat
hashcat -m {mode} hash.txt /usr/share/wordlists/rockyou.txt

# john
john --format={format} --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

---

## Mode Reference

| Hash Type | Hashcat -m | John --format |
|-----------|-----------|---------------|
| MD5       | 0         | raw-md5       |
| SHA1      | 100       | raw-sha1      |
| SHA256    | 1400      | raw-sha256    |
| bcrypt    | 3200      | bcrypt        |
| NTLM      | 1000      | nt            |

---

## Gotchas

<!-- Document anything that bit you: encoding issues, salts, unusual modes -->

---

## Key Takeaways

- 
- 
- 

---

## References

- 
