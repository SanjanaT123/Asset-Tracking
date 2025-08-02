# main.py on Pico #1 (BLE Peripheral)
import bluetooth
import machine

# Advertising helper (merged into the same file)
def advertising_payload(limited_disc=False, br_edr=False, name=None):
    payload = bytearray()
    flags = 0x02 | (0x04 if limited_disc else 0x00) | (0x18 if not br_edr else 0x00)
    payload += bytes((2, 0x01, flags))
    if name:
        name_bytes = name.encode()
        payload += bytes((len(name_bytes) + 1, 0x09)) + name_bytes
    return payload

# Start BLE
ble = bluetooth.BLE()
ble.active(True)

name = "PicoTag"
payload = advertising_payload(name=name)

ble.gap_advertise(100_000, adv_data=payload)
print("Advertising as", name)

# Keep running
while True:
    machine.idle()
