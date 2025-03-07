emcc main.c sharp.c calc.c fonts.c func.c -o index.html -I../src -L../src -lraylib.web -s USE_GLFW=3 -s FULL_ES2=1 -s FORCE_FILESYSTEM=1 --preload-file resources
