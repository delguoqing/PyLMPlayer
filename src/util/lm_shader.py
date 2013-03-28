import shader

# for color transform.(Has texture)
cxform_shader = shader.Shader(
frag=[
"""
uniform vec4 color_add;
uniform vec4 color_mul;
uniform sampler2D sampler;

void main(void)
{
	vec2 coords = gl_TexCoord[0].st;
	vec4 final_color = texture2D(sampler, coords);
	gl_FragColor = final_color * color_mul  + color_add;
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
	gl_FragColor = gl_FrontColor * color_mul  + color_add;
}
"""
]
)