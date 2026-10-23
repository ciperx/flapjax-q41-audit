import json, os, time
from decimal import Decimal, getcontext
import scan as S

getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__))
POOL = "0xca93ec685b8623688e6b236f9068034b298c2150"
TREASURY = "0x7c34e9e21ee28a49ff0b84b61774119e6633359f"
TOKEN = "0x90c8889f428f9ebb77bb8f15cad3a50a9ac680df"
WBNB = "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

ARCH = "https://bsc-mainnet.public.blastapi.io"

def acall(method, params, tries=7):
    import urllib.request, urllib.error
    last = None
    for i in range(tries):
        req = urllib.request.Request(ARCH, data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode(),
                                     headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                j = json.loads(r.read().decode())
            if "result" in j:
                return j["result"]
            last = RuntimeError(str(j.get("error"))[:120])
            if "pruned" in str(last) or "execution reverted" in str(last):
                raise last
        except Exception as e:
            last = e
        time.sleep(0.8 + i * 1.2)
    raise RuntimeError("archive call failed: %s" % str(last)[:160])

def call(to, data, block="latest"):
    return acall("eth_call", [{"to": to, "data": data}, block])

def addr_word(h):
    return "0x" + h[-40:]

t0 = addr_word(call(POOL, "0x0dfe1681"))
t1 = addr_word(call(POOL, "0xd21220a7"))
fee = int(call(POOL, "0xddca3f43"), 16)
dec_fj = int(call(TOKEN, "0x313ce567"), 16)
dec_wbnb = int(call(WBNB, "0x313ce567"), 16)
print("token0", t0, "token1", t1, "fee", fee, "dec", dec_fj, dec_wbnb)

def slot0(block):
    raw = call(POOL, "0x3850c7bd", hex(block))
    w = raw[2:]
    ws = [w[i:i+64] for i in range(0, len(w), 64)]
    sq = int(ws[0], 16)
    tick = int(ws[1], 16)
    if tick >= (1 << 255):
        tick -= (1 << 256)
    return {"sqrtPriceX96": str(sq), "tick": tick, "liquidity": str(int(ws[3], 16))}

def bnb_bal(block):
    return int(acall("eth_getBalance", [TREASURY, hex(block)]), 16)

def nonce(block):
    return int(acall("eth_getTransactionCount", [TREASURY, hex(block)]), 16)

def fj_bal(block):
    raw = call(TOKEN, "0x70a08231" + "0" * 24 + TREASURY[2:], hex(block))
    return int(raw, 16)

r = json.load(open(os.path.join(HERE, "range.json")))
b1, b2 = r["b1"], r["b2"]

swaps = json.load(open(os.path.join(HERE, "swaps_decoded.json")))["swaps"]
tre = [x for x in swaps if x["treasury_involved"]]

receipts = {}
for x in tre:
    txh = x["tx"]
    if txh in receipts:
        continue
    tx = acall("eth_getTransactionByHash", [txh])
    rc = acall("eth_getTransactionReceipt", [txh])
    fj_tr = []
    for lg in rc["logs"]:
        if lg["address"].lower() == TOKEN and lg["topics"][0] == TRANSFER:
            fj_tr.append({"from": addr_word(lg["topics"][1]), "to": addr_word(lg["topics"][2]),
                          "value": str(int(lg["data"], 16))})
    receipts[txh] = {
        "tx_from": tx["from"].lower(),
        "tx_to": tx["to"].lower() if tx.get("to") else None,
        "value_wei": str(int(tx["value"], 16)),
        "status": rc["status"],
        "gasUsed": str(int(rc["gasUsed"], 16)),
        "block": int(rc["blockNumber"], 16),
        "fj_transfers": fj_tr,
        "logs_n": len(rc["logs"]),
    }

rows = []
for x in tre:
    b = x["block"]
    s_before = slot0(b - 1)
    s_at = slot0(b)
    fj_out = -x["amount0"] if x["amount0"] < 0 else 0
    wbnb_in = x["amount1"] if x["amount1"] > 0 else 0
    # price from slot0: token1 per token0 raw, adjusted for decimals
    p_before = (Decimal(s_before["sqrtPriceX96"]) / (Decimal(2) ** 96)) ** 2
    p_at = (Decimal(s_at["sqrtPriceX96"]) / (Decimal(2) ** 96)) ** 2
    # convert to BNB per FJ depending on token order
    if t0 == TOKEN.lower() and t1 == WBNB.lower():
        price_bnb_per_fj_before = p_before * Decimal(10) ** (dec_fj - dec_wbnb)
        price_bnb_per_fj_at = p_at * Decimal(10) ** (dec_fj - dec_wbnb)
        order = "token0=FLAPJAX, token1=WBNB"
    else:
        price_bnb_per_fj_before = (Decimal(1) / p_before) * Decimal(10) ** (dec_wbnb - dec_fj)
        price_bnb_per_fj_at = (Decimal(1) / p_at) * Decimal(10) ** (dec_wbnb - dec_fj)
        order = "token0=WBNB, token1=FLAPJAX"
    rows.append({
        "tx": x["tx"], "block": b, "ts": x["ts"],
        "utc": time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime(x["ts"])),
        "cot": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(x["ts"] - 5 * 3600)),
        "cot_day": time.strftime("%Y-%m-%d", time.gmtime(x["ts"] - 5 * 3600)),
        "bnb_in_wei": str(wbnb_in), "fj_out_wei": str(fj_out),
        "bnb_in": str(Decimal(wbnb_in) / Decimal(10) ** 18),
        "fj_out": str(Decimal(fj_out) / Decimal(10) ** 18),
        "eff_price_bnb_per_fj": str((Decimal(wbnb_in) / Decimal(10) ** 18) / (Decimal(fj_out) / Decimal(10) ** 18)) if fj_out else None,
        "slot0_before_block": b - 1,
        "slot0_before": s_before,
        "slot0_at": s_at,
        "pool_price_before_bnb_per_fj": str(price_bnb_per_fj_before),
        "pool_price_at_bnb_per_fj": str(price_bnb_per_fj_at),
        "tx": x["tx"],
        "receipt": receipts[x["tx"]],
        "treasury_bnb_before_wei": str(bnb_bal(b - 1)),
        "treasury_bnb_after_wei": str(bnb_bal(b)),
        "treasury_fj_before_wei": str(fj_bal(b - 1)),
        "treasury_fj_after_wei": str(fj_bal(b)),
        "treasury_nonce_before": nonce(b - 1),
        "treasury_nonce_after": nonce(b),
    })
    json.dump({"partial": True, "buys": rows}, open(os.path.join(HERE, "buys_raw.json"), "w"), indent=1)
    print(rows[-1]["utc"], rows[-1]["cot"], b, rows[-1]["bnb_in"], rows[-1]["fj_out"],
          "eff", rows[-1]["eff_price_bnb_per_fj"], "poolbefore", rows[-1]["pool_price_before_bnb_per_fj"], flush=True)
    time.sleep(1.0)

meta = {
    "token0": t0, "token1": t1, "fee": fee, "dec_fj": dec_fj, "dec_wbnb": dec_wbnb,
    "order": order,
    "window": {"b1": b1, "b2": b2},
    "bnb_start_wei": str(bnb_bal(b1 - 1)), "bnb_end_wei": str(bnb_bal(b2)),
    "fj_start_wei": str(fj_bal(b1 - 1)), "fj_end_wei": str(fj_bal(b2)),
    "nonce_start": nonce(b1 - 1), "nonce_end": nonce(b2),
    "slot0_start": slot0(b1 - 1), "slot0_end": slot0(b2),
}
print(meta)
json.dump({"meta": meta, "buys": rows}, open(os.path.join(HERE, "buys_raw.json"), "w"), indent=1)
