#version 330

uniform sampler2D texture_0;
uniform sampler2D colour_ramp_0;

in vec2 vs_uv;

out vec4 fs_colour;

void main(){
    float height = texture(texture_0, vs_uv).r / 2.0;
    vec3 shade = texture(colour_ramp_0, vec2(height, 0.0)).rgb;

    fs_colour = vec4(shade, 1.0);
}