DATA = {

	0xF001: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("symbol_cnt", 0x4, ">I"),
		("symbol_list", "g['symbol_cnt']", "list",
			(
				("symbol_len", 0x4, ">I"),
				("symbol", "g['symbol_len']", "'>%ds'%g['symbol_len']"),
				("zero", 0x1, ">B"),
				("padding", "3-(g['off']+3)%4", "'>%ds'%(3-(g['off']+3)%4)"),
			)
		),
	),

	0xF002: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("color_cnt", 0x4, ">I"),
		("color_list", "g['color_cnt']", "list",
			(
				("R", 0x2, ">h"),
				("G", 0x2, ">h"),
				("B", 0x2, ">h"),
				("A", 0x2, ">h"),		
			)
		),
	),
	
	# Matrix:
	# [scale_x,     rotateskew_x]
	# [rotateskew_y,     scale_y]
	# [trans_x,          trans_y]
	#
	# In flash:
	# x' = x * scale_x + y * rotateskew_y + trans_x
	# y' = y * rotateskew_x + y * scale_y + trans_y
	# 
	# Which equals to:
	# [x']   [scale_x,      rotateskew_y, trans_x]   [x]
	# [y'] = [rotateskew_x, scale_y,      trans_y] * [y]
	# [1 ]   [0,            0,                  1]   [1]
	# 	 		
	0xF003: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("mat_cnt", 0x4, ">I"),
		("mat_list", "g['mat_cnt']", "list",
			(
				("scale_x", 0x4, ">f"),
				("rotateskew_x", 0x4, ">f"),
				("rotateskew_y", 0x4, ">f"),
				("scale_y", 0x4, ">f"),
				("trans_x", 0x4, ">f"),
				("trans_y", 0x4, ">f"),
			)
		),
	),
	
	0xF103: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("pos_cnt", 0x4, ">I"),
		("pos_list", "g['pos_cnt']", "list",
			(
				("x", 0x4, ">f"),
				("y", 0x4, ">f"),
			),
		),
	),

	# bounding rect list
	0xF004: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("box_cnt", 0x4, ">I"),
		("box_list", "g['box_cnt']", "list",
			(
				("xmin", 0x4, ">f"),
				("ymin", 0x4, ">f"),
				("xmax", 0x4, ">f"),
				("ymax", 0x4, ">f"),
			),
		),
	),

	0xF005: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("as_cnt", 0x4, ">I"),
		("as_list", "g['as_cnt']", "list",
			(
				("as_len", 0x4, ">I"),
				("bytecode", "g['as_len']", "'>%ds'%g['as_len']"),
				("padding", "3-(g['off']+3)%4", "'>%ds'%(3-(g['off']+3)%4)"),
			)
		),
	),

	0xF007: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("img_cnt", 0x4, ">I"),
		("img_list", "g['img_cnt']", "list",
			(
				("img_idx", 0x4, ">I"),
				("name_idx", 0x4, ">I"),
				("width", 0x4, ">f"),
				("height", 0x4, ">f"),
			)
		),
	),

	0xF008: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("unk_cnt", 0x4, ">I"),
		("unk_list", "g['unk_cnt']", "list",
			(
				("unk1", 0x4, ">I"),
				("unk2", 0x4, ">I"),
			)
		),
	),

	0xF009: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("unk", 0x4, ">I"),
	),

	0xF00A: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("unk_cnt", 0x4, ">I"),
		("unk_list", "g['unk_cnt']", "list",
			(
				("idx", 0x4, ">I"),
				("unk2", 0x4, ">I"),
				("text_idx", 0x4, ">I"),
				("unk4", 0x4, ">I"),
				("unk5", 0x4, ">I"),
			)
		),
	),
	
	0xF00B: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("unk", 0x4, ">I"),
	),
				
	0xF00C: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("v", 0x4, ">I"),
		("e", 0x4, ">I"),
		("r", 0x4, ">I"),
		("max_character_id", 0x4, ">I"),
		("reserved", 0x4, ">i"),
		("start_character_id", 0x4, ">I"),
		("unk", 0x2, ">H"),
		("reserved2", 0x2, ">H"),
		("fps", 0x4, ">f"),
		("width", 0x4, ">f"),
		("height", 0x4, ">f"),
		("x", 0x4, ">f"),
		("y", 0x4, ">f"),
	),

	# an overview of all character define tags
	0xF00D: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("f022_cnt", 0x4, ">I"),	# 'super' shape / texture sprite
		("0007_cnt", 0x4, ">I"),	# button
		("0027_cnt", 0x4, ">I"),	# sprite / movieclip
		("000b_cnt", 0x4, ">I"),	# static text
		("0025_cnt", 0x4, ">I"),	# edit text
		("const0_0", 0x4, ">I"),	# unknown1
		("const1_0", 0x4, ">I"),	# unknown2
		("const2_0", 0x4, ">I"),	# unknown3
	),

	0xF022: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("character_id", 0x4, ">I"),
		("const0_0", 0x4, ">I"),
		("size_idx", 0x4, ">I"),
		("f023_cnt", 0x4, ">I"),
		("f024_cnt", "(g['tag_size']-4)*4", ">I"),	# optional
	),
			
	0xF023: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("x0", 0x4, ">f"),
		("y0", 0x4, ">f"),
		("u0", 0x4, ">f"),
		("v0", 0x4, ">f"),
		("x1", 0x4, ">f"),
		("y1", 0x4, ">f"),
		("u1", 0x4, ">f"),
		("v1", 0x4, ">f"),
		("x2", 0x4, ">f"),
		("y2", 0x4, ">f"),
		("u2", 0x4, ">f"),
		("v2", 0x4, ">f"),
		("x3", 0x4, ">f"),
		("y3", 0x4, ">f"),
		("u3", 0x4, ">f"),
		("v3", 0x4, ">f"),
		("fill_idx", 0x4, ">I"),
		("fill_style", 0x2, ">H"),
		("const0_0", 0x2, ">H"),
	),
		
	0xF024: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("fill_idx", 0x4, ">I"),
		("fill_style", 0x2, ">H"),
		("unk1", 0x2, ">H"),
		("unk2", 0x4, ">I"),
		("x0", 0x4, ">f"),
		("y0", 0x4, ">f"),
		("u0", 0x4, ">f"),
		("v0", 0x4, ">f"),
		("x1", 0x4, ">f"),
		("y1", 0x4, ">f"),
		("u1", 0x4, ">f"),
		("v1", 0x4, ">f"),
		("x2", 0x4, ">f"),
		("y2", 0x4, ">f"),
		("u2", 0x4, ">f"),
		("v2", 0x4, ">f"),
		("x3", 0x4, ">f"),
		("y3", 0x4, ">f"),
		("u3", 0x4, ">f"),
		("v3", 0x4, ">f"),
		("unk3", 0x4, ">I"),
		("unk4", 0x2, ">H"),
		("unk5", 0x2, ">H"),
		("unk6", 0x4, ">I"),
	),
	
	0x0027: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("character_id", 0x4, ">I"),
		("const0_0", 0x4, ">I"),
		("class_name_idx", 0x4, ">I"),
		("frame_label_cnt", 0x4, ">I"),
		("0001_cnt", 0x4, ">I"),
		("key_frame_cnt", 0x4, ">I"),
		("max_depth", 0x2, ">H"),
		("const1_0", 0x2, ">H"),
	),
		
	0x0001: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("frame_id", 0x4, ">I"),
		("cmd_cnt", 0x4, ">I"),
	),
					
	0x0004: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("character_id", 0x4, ">I"),
		("inst_id", 0x4, ">i"),
		("unk1", 0x4, ">I"),
		("name_idx", 0x4, ">I"),
		("flags", 0x2, ">H"),
		("blend_mode", 0x2, ">H"),
		("depth", 0x2, ">H"),
		("clip_depth", 0x2, ">H"),
		("ratio", 0x2, ">H"),
		("unk5", 0x2, ">H"),
		("trans_idx", 0x4, ">i"),
		("color_mul_idx", 0x4, ">i"),
		("color_add_idx", 0x4, ">i"),
		("unk6", 0x4, ">I"),
		("clip_action_cnt", 0x4, ">I"),
		("unk7", 0x0, ">I"),	# missing
	),
	
	0xF105: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("frame_id", 0x4, ">I"),
		("cmd_cnt", 0x4, ">I"),
	),

	# DefineFont
	0x000A: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("font_cnt", 0x4, ">I"),
		("font_list", "g['font_cnt']", "list",
			(
				("idx", 0x4, ">I"),
				("unk1", 0x4, ">I"),
				("name_idx", 0x4, ">I"),	# refer to tagF001
				("unk3", 0x4, ">I"),
				("unk4", 0x4, ">I"),
			)
		),
	),
	
	0x000C: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("as_idx", 0x4, ">I"),
		("unk0", 0x4, ">I"),
	),
					
	0x002B: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("name_idx", 0x4, ">I"),
		("frame_id", 0x4, ">I"),
		("unk0", 0x4, ">I"),
	),

	0x0005: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("unk0", 0x4, ">I"),
		("depth", 0x2, ">H"),
		("unk1", 0x2, ">H"),
	),

	0xF014: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("as_idx", 0x4, ">I"),
		("clip_event_flags", 0x4, ">I"),
	),

	# Define Button2
	0x0007: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("character_id", 0x4, ">I"),
		("const0_0", 0x4, ">I"),
		("const1_0", 0x4, ">I"),
		("box_idx", 0x4, ">I"),
		("unk_flags", 0x4, ">I"),
		("f018_cnt", 0x4, ">I"),
		("1019_cnt", 0x4, ">I"),
	),

	# Button Record
	0xF018: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("character_id", 0x4, ">I"),
		("trans_idx", 0x4, ">I"),
		("color_mul_idx", 0x4, ">I"),
		("color_add_idx", 0x4, ">I"),
		("depth", 0x2, ">H"),
		("unk0", 0x2, ">H"),
		("unk1", 0x1, ">B"),
		("button_state_flags", 0x1, ">B"),
		("unk2", 0x2, ">H"),
	),

	# Button cond Action
	0xF019: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("as_idx", 0x4, ">I"),
		("cond_flags", 0x2, ">H"),
		("cond_key_press", 0x2, ">H"),	# Z, X, C, V found in some file, haha
	),

	# Define Edit Text?
	0x0025: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("character_id", 0x4, ">I"),
		("font_id", 0x4, ">I"),		
		("init_txt_idx", 0x4, ">I"),
		("font_class_name_idx", 0x4, ">I"),		
		("color_idx", 0x4, ">I"),
		("rect_idx", 0x4, ">I"),		
		("var_name_idx", 0x4, ">I"),	# idx of name of variable
		("unk0", 0x4, ">I"),
		("align", 0x2, ">H"),
		("max_length", 0x2, ">H"),		
		("flags0", 0x4, ">I"),		
		("flags1", 0x4, ">I"),
		("font_size", 0x4, ">f"),		
		("left_margin", 0x4, ">f"),				
		("right_margin", 0x4, ">f"),				
		("indent", 0x4, ">f"),				
		("leading", 0x4, ">f"),										
	),

	# DefineText
	0x000B: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("character_id", 0x4, ">I"),		
		("rect_idx", 0x4, ">I"),
		("trans_idx", 0x4, ">I"),		
		("txt_idx?", 0x4, ">I"),				
		("f00e_cnt", 0x4, ">I"),						
	),

	# TextRecord
	0xF00E: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("ori_text_idx", 0x4, ">I"),	# refer to 0xF00A
		("font_id", 0x4, ">I"),
		("height", 0x4, ">f"),
		("xoffset", 0x4, ">f"),
		("yoffset", 0x4, ">f"),		
		("color_id", 0x4, ">I"),
	),

	# Start Sound
	0x000F: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
		("character_id", 0x4, ">I"),
		("unk0", 0x4, ">I"),
		("unk1", 0x4, ">I"),
		("unk2", 0x4, ">I"),
		("unk3", 0x4, ">I"),
		("unk4", 0x4, ">I"),										
	),
				
	0xFF00: (
		("tag_type", 0x4, ">I"),
		("tag_size", 0x4, ">I"),
	),
}

HEADER_SIZE = 0x8