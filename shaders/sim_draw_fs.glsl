#version 330

uniform sampler2D texture_0;

in vec2 vs_uv;

out vec4 fs_colour;

void main(){
    fs_colour = vec4(texture(texture_0, vs_uv).r);
}