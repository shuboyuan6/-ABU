import requests, time, json

t0 = time.time()
try:
    r = requests.post("http://localhost:11434/api/generate",
        json={"model": "noahs:r1-8b-clean",
              "prompt": "简短回答：1+1等于几？",
              "stream": False,
              "options": {"num_predict": 30}},
        timeout=240)
    elapsed = time.time() - t0
    resp = r.json()
    print(f"OK ({elapsed:.0f}s)")
    print(f"response: {resp.get('response','')[:100]}")
    print(f"thinking: {resp.get('thinking','')[:100]}")
except Exception as e:
    print(f"FAIL after {time.time()-t0:.0f}s: {e}")
