#version 330

in vec2 in_vert;
in vec2 in_uv;

out vec2 vs_uv;

void main(){
    vs_uv = in_uv;
    gl_Position = vec4(in_vert, 0.0, 1.0);
}