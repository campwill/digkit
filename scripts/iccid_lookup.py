import json

# referenced and validated using information from:
# http://phone.fyicenter.com/1155_ICCID_SIM_Card_Number_Checker_Decoder.html
# http://phone.fyicenter.com/900_What_Is_the_SIM_Card_Number.html

# information sourced from:
# https://github.com/bifravst/e118-iin-list
with open('data//cccii.json', 'r') as f:
    cciii_data = json.load(f)

# information sourced from :
# https://github.com/pbakondy/mcc-mnc-list/
# https://mcc-mnc.com/
with open('data//mccmnc.json', 'r') as f:
    mccmnc_data = json.load(f)

def luhn_checksum(number):
    num_str = str(number)
    total = 0
    reverse_digits = num_str[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

def lookup_iccid(number):
    num_str = str(number)

    if not num_str.startswith("89"):
        print(f"Denied: {num_str} does not start with 89")
        return

    if not luhn_checksum(num_str):
        print(f"Invalid checksum: {num_str}")
        return

    # everything after '89'
    body = num_str[2:]

    # check iccid format
    sorted_iccid_prefixes = sorted(cciii_data.keys(), key=len, reverse=True)
    for prefix in sorted_iccid_prefixes:
        if body.startswith(prefix):
            details = cciii_data[prefix]

            account_number = body[len(prefix):][:-1]
            checksum = body[len(prefix):][-1]

            print(f"Your SIM Card number, {num_str}, uses ICCID format:\n")
            print(f"Major Industry Identifier (MII): 89 - Telecom - Private agency")
            print(f"International Calling Region: {details.get("ccc", "N/A")} - {details.get('country', 'N/A')}")
            print(f"Issuer: {details.get("ii", "N/A")} - {details.get('issuer', 'N/A')}")
            print(f"Account Number: {account_number}")
            print(f"Checksum: {checksum}\n")
            return

    imsi_found = False

    # check imsi format
    sorted_imsi_prefixes = sorted(mccmnc_data.keys(), key=len, reverse=True)
    for prefix in sorted_imsi_prefixes:
        if body.startswith(prefix):
            details = mccmnc_data[prefix]

            imsi_found = True

            account_number = body[len(prefix):][:-1]
            checksum = body[len(prefix):][-1]

            print(f"Your SIM Card number, {num_str}, potentially uses MCC-MNC format:\n")
            print(f"Major Industry Identifier (MII): 89 - Telecom - Private agency")
            print(f"MCC (Mobile Country Code): {details.get('mcc', 'N/A')} - {details.get('country', 'N/A')}")

            network = details.get('network', 'N/A')
            if isinstance(network, list):
                if len(network) == 1:
                    print(f"MNC (Mobile Network Code): {details.get('mnc', 'N/A')} - {network[0]}")
                else:
                    print(f"MNC (Mobile Network Code): {details.get('mnc', 'N/A')} - Multiple Networks:")
                    for n in network:
                        print(f"  - {n}")
            else:
                print(f"MNC (Mobile Network Code): {details.get('mnc', 'N/A')} - {network}")

            print(f"Account Number: {account_number}")
            print(f"Checksum: {checksum}\n")
            break

    # country codes sourced from mccmnc.json
    COUNTRY_CODES = [
        "1","7","20","27","30","31","32","33","34","36","39","40","41","43","44","45",
        "46","47","48","49","51","52","53","54","55","56","57","58","60","61","62","63",
        "64","65","66","79","81","82","84","86","90","91","92","93","94","95","98",
        "212","213","216","218","220","221","222","223","224","225","226","227","228",
        "229","230","231","232","233","234","235","236","237","238","239","240","241",
        "242","243","244","245","248","249","250","251","252","253","254","255","256",
        "257","258","260","261","262","263","264","265","266","267","268","269","284",
        "291","297","298","299","350","351","352","353","354","355","356","357","358",
        "359","370","371","372","373","374","375","376","377","378","380","381","382",
        "383","385","386","387","389","420","421","423","500","501","502","503","504",
        "505","506","507","508","509","591","592","593","594","595","597","598","599",
        "670","673","674","675","676","677","678","679","680","682","683","684","685",
        "686","687","689","691","850","852","853","855","856","880","882","886","960",
        "961","962","963","964","965","966","967","968","970","971","972","973","974",
        "975","976","977","992","993","994","995","996","998","1242","1246","1264",
        "1268","1345","1441","1473","1664","1671","1758","1767","1784","1809","1868",
        "1869","1876"
    ]

    # check hybrid format
    for ccc in COUNTRY_CODES:

        possible_ccc = ccc
        zero_padded_ccc = ccc.zfill(len(ccc) + 1)

        if body.startswith(possible_ccc) or body.startswith(zero_padded_ccc):

            matched_ccc = zero_padded_ccc if body.startswith(zero_padded_ccc) else possible_ccc
            remaining = body[len(matched_ccc):]

            for key, entry in mccmnc_data.items():
                if entry.get("country_code") != ccc:
                    continue

                mnc = entry["mnc"]

                if remaining.startswith(mnc):

                    after_mnc = remaining[len(mnc):]
                    account_number = after_mnc[:-1]
                    checksum = after_mnc[-1]

                    if imsi_found:
                        print(f"Your SIM Card number, {num_str}, may also use Hybrid format:\n")
                    else:
                        print(f"Your SIM Card number, {num_str}, potentially uses Hybrid format:\n")
                    
                    
                    print(f"Major Industry Identifier (MII): 89 - Telecom - Private agency")
                    print(f"International Calling Region (CCC): {matched_ccc} - {entry['country']}")

                    network = entry.get("network", "N/A")
                    if isinstance(network, list):
                        if len(network) == 1:
                            print(f"MNC (Mobile Network Code): {mnc} - {network[0]}")
                        else:
                            print(f"MNC (Mobile Network Code): {mnc} - Multiple Networks:")
                            for n in network:
                                print(f"  - {n}")
                    else:
                        print(f"MNC (Mobile Network Code): {mnc} - {network}")

                    print(f"Account Number: {account_number}")
                    print(f"Checksum: {checksum}\n")
                    return


    if imsi_found:
        return

    print(f"Unknown format for {num_str}.")
    return