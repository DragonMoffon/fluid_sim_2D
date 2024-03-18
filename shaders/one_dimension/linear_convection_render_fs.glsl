#version 330

uniform sampler2D texture_0;

in vec2 vs_uv;

out vec4 fs_colour;

void main(){
    float height = texture(texture_0, vs_uv).r / 2.5;
    float shade = vs_uv.y < height ? 1.0 : 0.0;

    fs_colour = vec4(shade);

}