import numpy as np
from math import gcd

# =========================
# FUNGSI MATEMATIKA
# =========================

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def matrix_mod_inv(K, mod):
    det = int(round(np.linalg.det(K)))  # determinan
    det = det % mod

    if gcd(det, mod) != 1:
        raise ValueError("Determinan tidak punya invers modulo!")

    det_inv = mod_inverse(det, mod)

    adj = np.round(det * np.linalg.inv(K)).astype(int)

    return (det_inv * adj) % mod


# =========================
# KONVERSI TEKS
# =========================

def text_to_numbers(text):
    return [ord(c) - 65 for c in text.upper() if c.isalpha()]


def numbers_to_text(nums):
    return ''.join(chr(n + 65) for n in nums)


# =========================
# ENKRIPSI
# =========================

def encrypt(plaintext, K):
    mod = 26
    nums = text_to_numbers(plaintext)

    n = K.shape[0]

    while len(nums) % n != 0:
        nums.append(23)  # padding 'X'

    ciphertext = []

    for i in range(0, len(nums), n):
        block = np.array(nums[i:i+n])
        result = np.dot(K, block) % mod
        ciphertext.extend(result)

    return numbers_to_text(ciphertext)


# =========================
# DEKRIPSI
# =========================

def decrypt(ciphertext, K):
    mod = 26
    K_inv = matrix_mod_inv(K, mod)

    nums = text_to_numbers(ciphertext)

    n = K.shape[0]

    plaintext = []

    for i in range(0, len(nums), n):
        block = np.array(nums[i:i+n])
        result = np.dot(K_inv, block) % mod
        plaintext.extend(result)

    return numbers_to_text(plaintext)


# =========================
# PROGRAM UTAMA
# =========================

if __name__ == "__main__":
    print("=== HILL CIPHER (INPUT USER) ===")

    # matriks kunci
    K = np.array([[3, 3],
                  [2, 5]])

    # cek determinan
    det = int(round(np.linalg.det(K)))
    print("Determinan matriks:", det)

    if gcd(det, 26) != 1:
        print("✗ Matriks tidak valid!")
    else:
        print("✓ Matriks valid")

        plaintext = input("Masukkan kata: ")

        cipher = encrypt(plaintext, K)
        decrypted = decrypt(cipher, K)

        print("Plaintext :", plaintext.upper())
        print("Ciphertext:", cipher)
        print("Decrypted :", decrypted)