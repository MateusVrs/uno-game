import ctypes

mainc = ctypes.cdll.LoadLibrary("code/C/libmain.dll")
mainc.main()
