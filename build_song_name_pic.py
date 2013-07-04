import os
import glob
import font
from src.tja import tja_reader, tja_header

reader = tja_reader.CReader()
header = tja_header.CData()

for file_path in glob.glob(r"./song/*/*/*.tja"):
	out_folder = os.path.join("..", os.path.split(file_path)[0])
	
	reader.set_file(file_path)
	
	header.reset()
	header.read(reader)
	header.refresh()
	
	cwd = os.getcwd()
	os.chdir("./font")
	font.gen_song_name_texture(header["TITLE"], header["SUBTITLE"], out_folder, header["FONT"])
	os.chdir(cwd)

