import ctypes

libmain = ctypes.cdll.LoadLibrary("code/C/libmain.dll")
libmain.main()
