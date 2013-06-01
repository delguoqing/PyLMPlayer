cdef extern from "memory.h" nogil:
	void *memset(void* ptr, int value, size_t num)