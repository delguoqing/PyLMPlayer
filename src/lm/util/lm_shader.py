import shader

# for color transform.(Has texture)
cxform_shader = shader.Shader(
frag=[
"""
uniform vec4 color_add;
uniform vec4 color_mul;
uniform int use_texture;
uniform sampler2D sampler;

void main(void)
{
	vec2 coords = gl_TexCoord[0].st;
	vec4 color;
	if (use_texture) {
		color = texture2D(sampler, coords);
	} else {
		color = gl_Color;
	}
	gl_FragColor = color * color_mul  + color_add;
}
"""
]
)

# for color transform.(No texture)
cxform_shader_no_texture = shader.Shader(frag=[
"""
uniform vec4 color_add;
uniform vec4 color_mul;

void main(void)
{
	gl_FragColor = gl_Color * color_mul  + color_add;
}
"""
]
)