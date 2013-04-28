import shader

# for color transform.(Has texture)
cxform_shader = shader.Shader(
frag=[
"""
uniform vec4 color_add;
uniform sampler2D sampler;

void main(void)
{
	gl_FragColor = texture2D(sampler, gl_TexCoord[0].st) * gl_Color  + color_add;
}
"""
]
)