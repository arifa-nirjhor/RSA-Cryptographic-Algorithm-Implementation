def extended_gcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r

        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    if old_r < 0:
        old_r = -old_r
        old_s = -old_s
        old_t = -old_t

    return old_r, old_s, old_t


def main():
    print("===== EXTENDED EUCLIDEAN ALGORITHM =====")

    try:
        a = int(input("Enter first integer (a): "))
        b = int(input("Enter second integer (b): "))

        if a == 0 and b == 0:
            print("Both numbers cannot be zero.")
            return

        gcd_value, x, y = extended_gcd(a, b)

        print("\n===== RESULTS =====")
        print("GCD:", gcd_value)
        print("Coefficient x:", x)
        print("Coefficient y:", y)

        print("\nVerification:")
        print(f"{a}({x}) + {b}({y}) = {a*x + b*y}")

    except ValueError:
        print("Error: Please enter valid integers.")


if __name__ == "__main__":
    main()
