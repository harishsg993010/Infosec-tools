import pefile

def main():
  # Parse command-line arguments
  if len(sys.argv) != 2:
    print("Usage: python3 scan.py /path/to/exe")
    return

  exe_path = sys.argv[1]

  # Parse the PE file
  pe = pefile.PE(exe_path)

  # Check for common vulnerabilities in the PE file
  if pe.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE:
    print("EXE uses dynamic base")
  if pe.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_NX_COMPAT:
    print("EXE is compatible with Data Execution Prevention (DEP)")
  if pe.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_GUARD_CF:
    print("EXE uses Control Flow Guard (CFG)")

if __name__ == "__main__":
  main()
