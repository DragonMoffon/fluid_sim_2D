#version 430

layout(local_size_x=1) in;

layout(r32f, binding=0) uniform readonly image2D u_in_data;
layout(r32f, binding=1) uniform writeonly image2D u_out_data;

layout(std430, binding=0) buffer readonly
SimData
{
    float dt;
    float dx;
    float ws;
    float df_x;
} sim;

void main() {
    const int img_width = imageSize(u_in_data).x;
    const int index_i = int(gl_GlobalInvocationID.x);
    const int index_ip = int(mod(index_i + 1, img_width));

    const float u_i = imageLoad(u_in_data, ivec2(index_i, 0)).r;
    const float u_ip = imageLoad(u_in_data, ivec2(index_ip, 0)).r;

    float u_n = u_i - sim.ws * sim.df_x * (u_i - u_ip);

    imageStore(u_out_data, ivec2(index_i, 0), vec4(u_n));
}
