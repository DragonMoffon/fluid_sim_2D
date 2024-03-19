#version 330

uniform isampler2D texture_0;

uniform float max_value;

in vec2 vs_uv;

out vec4 fs_colour;

void main(){
    float height = float(texture(texture_0, vs_uv).r) / 100000.0 / max_value;
    float shade = vs_uv.y < height ? 1.0 : 0.0;

    fs_colour = vec4(shade);
}