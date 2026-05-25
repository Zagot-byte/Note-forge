<!-- filename: forensics-{room-slug}-{YYYY-MM-DD}.md -->

# {Room Name} — Forensics

| Field      | Value         |
|------------|---------------|
| Type       | Forensics     |
| Date       | {YYYY-MM-DD}  |
| Difficulty | {difficulty}  |
| Tags       | {tag1, tag2}  |

---

## Artefact Inventory

| File | Type | Size | Hash (MD5) |
|------|------|------|------------|
|      |      |      |            |

---

## Disk / Image Analysis

```bash
file {image}
fdisk -l {image}
mmls {image}

# Mount partition
mount -o loop,ro,offset={offset} {image} /mnt/target
```

---

## Volatility

```bash
# Profile detection
vol.py -f {dump} imageinfo

# Common plugins
vol.py -f {dump} --profile={profile} pslist
vol.py -f {dump} --profile={profile} netscan
vol.py -f {dump} --profile={profile} filescan
vol.py -f {dump} --profile={profile} dumpfiles -Q {addr} -D ./output/
```

---

## File Carving

```bash
foremost -i {image} -o ./carved/
binwalk -e {file}
photorec {image}
```

---

## Metadata

```bash
exiftool {file}
strings {file} | grep -i {pattern}
```

---

## Steganography

```bash
steghide extract -sf {file}
zsteg {file}
stegsolve {file}
```

---

## Key Takeaways

- 
- 
- 

---

## References

- 
