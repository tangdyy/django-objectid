import os

if os.name == 'nt':
    try:
        import win32con, win32file, pywintypes
    except ImportError:
        raise ImportError(
            "Couldn't import win32. Are you sure pywin32 installed?"
        )
    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
    LOCK_SH = 0
    LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
    __overlapped = pywintypes.OVERLAPPED()

    def lock_file(fo, flags=0):
        hfile = win32file._get_osfhandle(fo.fileno())
        win32file.LockFileEx(hfile, LOCK_EX|LOCK_NB, 0, 0xffff0000, __overlapped)

    def unlock_file(fo):
        hfile = win32file._get_osfhandle(fo.fileno())
        win32file.UnlockFileEx(hfile, 0, 0xffff0000, __overlapped)

elif os.name == 'posix':
    import fcntl 

    def lock_file(fo, flags=0):
        fcntl.flock(fo.fileno(), fcntl.LOCK_EX)

    def unlock_file(fo):
        fcntl.flock(fo.fileno(), fcntl.LOCK_UN)

else:
    raise RuntimeError('File Locker only support NT and Posix platforms.')