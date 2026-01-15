from hwmon.curves.curves import apply_profile


def main():
    apply_profile("cpu")
    apply_profile("gpu")
    apply_profile("mid")
    print("Curves applied successfully")


if __name__ == "__main__":
    main()
