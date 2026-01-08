import pandas as pd

# t1 (packet no.) = 586
# t2 (packet no.) = 6125


def strip_sqnum_tlv(hex_str, tag=0x86):
    """
    Remove the entire TLV for sqNum (tag 0x86) from a BER-encoded GOOSE APDU.
    Handles short- and long-form length for that tag.
    """
    data = bytearray.fromhex(hex_str)
    n = len(data)
    i = 0

    while i < n:
        if data[i] != tag:
            i += 1
            continue

        if i + 1 >= n:
            break

        len_byte = data[i + 1]

        if len_byte & 0x80:  # long-form length
            num_len_bytes = len_byte & 0x7F
            if i + 2 + num_len_bytes > n:
                break
            val_len = int.from_bytes(
                data[i + 2 : i + 2 + num_len_bytes], "big"
            )
            start = i
            end = i + 2 + num_len_bytes + val_len
        else:  # short-form
            val_len = len_byte
            start = i
            end = i + 2 + val_len

        # Remove tag + length(+ length bytes) + value
        del data[start:end]
        n = len(data)
        # keep i at same index to catch another 0x86 if present

    return data


def neutralize_goose_lengths(data: bytearray) -> bytearray:
    """
    Zero out length fields that are affected by sqNum size:
    - 2-byte GOOSE length after Ethertype+APPID
    - ASN.1 length after tag 0x61 (GOOSEPdu SEQUENCE)
    """
    d = bytearray(data)
    n = len(d)

    # Find Ethertype 0x88b8
    idx = d.find(bytes([0x88, 0xB8]))
    if idx != -1 and idx + 6 <= n:
        # Layout: [88 b8] [appID_hi appID_lo] [len_hi len_lo]
        d[idx + 4] = 0
        d[idx + 5] = 0

    # Find outer GOOSEPdu SEQUENCE tag 0x61 after header
    start = idx + 6 if idx != -1 else 0
    idx61 = d.find(bytes([0x61]), start)
    if idx61 != -1 and idx61 + 1 < n:
        len_byte = d[idx61 + 1]
        if len_byte & 0x80:
            num_len_bytes = len_byte & 0x7F
            # zero the "length header" bytes (0x81,0xXX or 0x82,0xXX,0xYY,...)
            d[idx61 + 1] = 0
            for j in range(idx61 + 2, min(idx61 + 2 + num_len_bytes, n)):
                d[j] = 0
        else:
            d[idx61 + 1] = 0

    return d


def canonicalize_goose(hex_str: str) -> bytes:
    """
    Build a 'canonical' representation of a GOOSE APDU:
    - sqNum TLV removed
    - length fields neutralized
    """
    data = strip_sqnum_tlv(hex_str, tag=0x86)
    data = neutralize_goose_lengths(data)
    return bytes(data)


def equal_ignoring_sqnum_and_lengths(h1: str, h2: str) -> bool:
    return canonicalize_goose(h1) == canonicalize_goose(h2)


# Example usage
# h1 = "010ccd01000100098e2173338100000088b803e8007d00000000617380164c49454431304354524c2f4c4c4e3024537461747573810205dc82164c49454431304354524c2f4c4c4e302453746174757383164c49454431304354524c2f4c4c4e302453746174757384085cd3d9ac8395810a8501008602137c8701008801018901008a0102ab08850204d28502162e"
# h2 = "010ccd01000100098e2173338100000088b803e8007d00000000617380164c49454431304354524c2f4c4c4e3024537461747573810205dc82164c49454431304354524c2f4c4c4e302453746174757383164c49454431304354524c2f4c4c4e302453746174757384085cd3d9ac8395810a850100860213878701008801018901008a0102ab08850204d28502162e"

# print(equal_ignoring_sqnum_and_lengths(h1, h2))

def get_mal_packets(df, start_idx=533, end_idx=6036):
    indexes = []
    first_packet = None
    for i in range(1, len(df)):
        
        if (i >= start_idx) and (i <= end_idx):
            current_packet = df["raw_bytes"][i]
            if i == start_idx:
                first_packet = current_packet
                indexes.append(i)
                
            elif equal_ignoring_sqnum_and_lengths(first_packet, current_packet):
                indexes.append(i)
                
    return indexes

df = pd.read_excel("SASMaker_data/xlsx/DOS_SASMaker.xlsx")

print(df.loc[513, :])

# first attack
indexes = get_mal_packets(df, 516, 5580)

print("First attack: len = ", len(indexes))

# second attack
indexes2 = get_mal_packets(df, 7808, 12870)

print("Second attack: len = ", len(indexes2))

mal_indexes = [*indexes, *indexes2]
print("mal_indexes = ", len(mal_indexes))

labels = [True if i in mal_indexes else False for i in range(len(df.index))]
df = df.assign(label=labels)

df.to_excel("SASMaker_data/xlsx/DOS_SASMaker.xlsx", index=False)

print(df.loc[0, :])
print(df.loc[513, :])