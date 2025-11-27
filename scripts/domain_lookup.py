import socket
import dns.resolver

def whois_query(domain, server="whois.iana.org"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server, 43))
        s.send((domain + "\r\n").encode("utf-8"))

        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data
        return response.decode("utf-8", errors="replace")


def get_whois(domain):
    iana_result = whois_query(domain, "whois.iana.org")

    whois_server = None
    for line in iana_result.splitlines():
        if line.lower().startswith("whois:"):
            whois_server = line.split(":", 1)[1].strip()
            break

    if not whois_server:
        whois_server = "whois.verisign-grs.com"

    print("WHOIS Server:", whois_server)

    return whois_query(domain, whois_server)


def get_dns_records(domain):
    record_types = ["A", "AAAA", "CNAME", "TXT", "SPF", "MX", "NS", "SOA"]
    output_lines = []

    for rtype in record_types:
        output_lines.append(f"=== {rtype} Records ===")
        try:
            answers = dns.resolver.resolve(domain, rtype)

            for rdata in answers:
                output_lines.append(str(rdata))

        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.exception.Timeout):
            output_lines.append("No records found.")

        output_lines.append("")  # empty line between record types

    return "\n".join(output_lines)