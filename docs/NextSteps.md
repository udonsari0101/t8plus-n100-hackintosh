# Next Steps

## Near Term

1. Preserve the current working Recovery profile in the private repo.
2. Boot macOS Recovery using the known working USB OpenCore path.
3. In Disk Utility, select only the prepared unallocated macOS target space.
4. Format only that macOS target space as APFS.
5. Do not erase the internal SSD as a whole.
6. Do not erase the Windows NTFS partition.
7. Install macOS Sonoma.

## After First Install

1. Confirm Windows still boots.
2. Confirm macOS boots through USB OpenCore.
3. Keep USB OpenCore as the recovery path until both operating systems are
   understood.
4. Build a real USB map and replace UTBDefault.kext.
5. Test Ethernet.
6. Add Intel AX210 Wi-Fi/Bluetooth kexts later, after the base install path is
   stable.
7. Test audio layout.
8. Document graphics limitations clearly.

## Public Documentation Habit

Only sanitized findings should be copied here. Private local configs, generated
identity values, backups, and machine-specific dumps stay out of the public repo.
