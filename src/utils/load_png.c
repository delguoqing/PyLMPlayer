#include <stdio.h>
#include <zlib.h>
#include <png.h>
#include <pthread.h>

int load_png(const char *filename, png_bytep buffer, int stride)
{
	png_image image;
	//printf("init png image!\n");
	memset(&image, 0, sizeof(png_image));
	image.version = PNG_IMAGE_VERSION;
	//printf("loading png!\n");
	if (png_image_begin_read_from_file(&image, filename)) {
		//printf("loading png1!\n");
		image.format = PNG_FORMAT_RGBA;
		png_image_finish_read(&image, NULL/*background*/, buffer, stride,
							  NULL/*colormap*/);
		//printf("loading png2!\n");
	}
	return -1;
}

typedef void (*async_callback)(void *arg);

typedef struct _load_png_arg {
	const char *filename;
	png_bytep buffer;
	int stride;
	async_callback callback;
	void *callback_arg;
} load_png_arg, *load_png_argp;

void *load_png_thread_wrapper(void *arg)
{
	//printf("thread doing work! %p\n", arg);
	load_png_argp _arg = (load_png_argp)arg;
	//printf("thread doing convert work! %p\n", _arg);
	load_png(_arg->filename, _arg->buffer, _arg->stride);
	//printf("thread doing work!2%d\n", _arg->callback);
	_arg->callback(_arg->callback_arg);
	free(arg);
}

void *dummy_thread_worker(void *arg)
{
	printf("thread working!!!\n");	
}

int load_png_async(const char *filename, png_bytep buffer, int stride,
				   async_callback callback, void *callback_arg)
{
	load_png_argp call_arg = malloc(sizeof(load_png_arg));
	call_arg->filename = filename;
	call_arg->buffer = buffer;
	call_arg->stride = stride;
	call_arg->callback = callback;
	call_arg->callback_arg = callback_arg;
	
	//printf("callback function pointer %p\n", callback);
	
	pthread_t thread;
	int rc;
	rc = pthread_create(&thread, NULL, /*dummy_thread_worker*/load_png_thread_wrapper, (void *)call_arg);
	if (rc) {
		printf("can't create loading thread!\n");
		return rc;
	}
	return 0;
}

void on_load_png_finish(void *arg)
{
	int png_idx = (int)arg;
	printf("png %d loading over!\n", png_idx);
	pthread_exit(NULL);
}

int main()
{
	/* simulate the atlas 1024x1024 RGBA*/
	png_bytep atlas;
	atlas = (png_bytep)malloc(4 * 1024 * 1024);
	
	png_bytep buffer = atlas;
	int stride = 1024 * 4;
	const char *file_to_load[] = {"./COS_50_ATAMA_02A.png", "./COS_50_ATAMA_01A.png", "./COS_50_ATAMA_03A.png", "./COS_50_ATAMA_04A.png", NULL};
	const char *p;
	int i;
	
	for (i = 0, p = file_to_load[0]; p != NULL; i ++, p=file_to_load[i]) {
		load_png_async(p, buffer, stride, on_load_png_finish, (void *)i);
	}
	
	pthread_exit(NULL);
	return 0;
}