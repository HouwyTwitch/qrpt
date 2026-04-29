"""CLI entrypoint for `python -m qrpt`."""

from . import __doc__ as package_doc


def main() -> int:
    print("qrpt installed successfully.")
    print("Use examples in your project, e.g. `from qrpt import seal_to_public_key`.")
    if package_doc:
        print("\n" + package_doc.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
