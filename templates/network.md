<!-- filename: network-{room-slug}-{YYYY-MM-DD}.md -->

# {Room Name} — Network

| Field      | Value         |
|------------|---------------|
| Type       | Network       |
| Date       | {YYYY-MM-DD}  |
| Difficulty | {difficulty}  |
| Tags       | {tag1, tag2}  |

---

## Network Map

| Host | IP | Role | OS |
|------|----|------|----|
|      |    |      |    |

---

## Nmap

```bash
nmap -sC -sV -p- --min-rate 5000 -oN nmap/full {target}
nmap -sU --top-ports 100 -oN nmap/udp {target}
```

---

## Pivoting

```bash
# SSHuttle
sshuttle -r {user}@{pivot-host} {subnet}/24

# Chisel
# Server (attacker)
chisel server -p {port} --reverse
# Client (pivot)
chisel client {attacker-ip}:{port} R:{local-port}:{target}:{remote-port}
```

---

## Proxychains

```bash
# /etc/proxychains4.conf
socks5 127.0.0.1 {port}

proxychains nmap -sT -Pn {internal-target}
```

---

## VPN / Tunnel Notes

<!-- Any unusual routing, split tunnels, interface names -->

---

## Key Takeaways

- 
- 
- 

---

## References

- 
