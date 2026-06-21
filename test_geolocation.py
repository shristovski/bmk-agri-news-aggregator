"""
Tests the geolocation module with simulated IPs from different countries.
Run: python3 test_geolocation.py
"""
import sys
sys.path.insert(0, ".")

from src.geolocation import extract_client_ip, detect_location


def test_header(label, headers, expect_none=False):
    ip = extract_client_ip(headers)
    if expect_none:
        status = "✓" if ip is None else "✗"
        print(f"  {status} {label}: {ip}  (expected: None)")
    else:
        status = "✓" if ip else "✗"
        print(f"  {status} {label}: {ip}")
    return ip


def test_location(label, client_ip):
    print(f"  → {label}...")
    loc = detect_location(client_ip)
    print(f"    Result: {loc.country} / {loc.region} / {loc.continent}")
    if loc.country == "Global":
        print(f"    ⚠  Detection failed")
    else:
        print(f"    ✓  Detected successfully")
    print()
    return loc


def main():
    print("=" * 60)
    print("GEOLOCATION MODULE TESTS")
    print("=" * 60)

    US_IP = "8.8.8.8"
    AU_IP = "1.1.1.1"
    MK_IP = "77.28.0.1"

    # ---- 1. HEADER EXTRACTION ----
    print("\n--- 1. Header Extraction (no API calls) ---\n")

    test_header("CF-Connecting-IP (US)",       {"CF-Connecting-IP": US_IP})
    test_header("X-Real-IP (Australia)",        {"X-Real-IP": AU_IP})
    test_header("True-Client-IP (Macedonia)",   {"True-Client-IP": MK_IP})
    test_header("X-Forwarded-For (US, skip private)",
                {"X-Forwarded-For": "192.168.1.1, 10.0.0.1, " + US_IP})
    test_header("X-Forwarded-For (Australia first)",
                {"X-Forwarded-For": AU_IP + ", 10.0.0.1"})
    test_header("No headers",                   {}, expect_none=True)
    test_header("Private IPs only",
                {"X-Forwarded-For": "127.0.0.1, 10.0.0.1, 192.168.1.1"},
                expect_none=True)

    # ---- 2. LOCATION DETECTION ----
    print("\n--- 2. Location Detection (calls ipapi.co / ipinfo.io) ---\n")

    test_location("No IP — server-side fallback (your real IP)", None)
    test_location(f"US IP — {US_IP}", US_IP)
    test_location(f"Australia IP — {AU_IP}", AU_IP)

    print("\n" + "=" * 60)
    print("To test via the web app with different IPs:")
    print("=" * 60)
    print()
    print("  1. Run the app:")
    print("     GEOLOCATION_DEBUG=1 streamlit run app.py")
    print()
    print("  2. Open http://localhost:8501 in your browser")
    print("     → Should show your real location (North Macedonia)")
    print()
    print("  3. Simulate a US visitor (open in another terminal):")
    print("     curl -H 'CF-Connecting-IP: 8.8.8.8' http://localhost:8501")
    print()
    print("  4. Simulate an Australian visitor:")
    print("     curl -H 'X-Real-IP: 1.1.1.1' http://localhost:8501")
    print()
    print("  The GEOLOCATION_DEBUG=1 mode shows a debug panel")
    print("  with the detected IP, headers, and final location.")


if __name__ == "__main__":
    main()
