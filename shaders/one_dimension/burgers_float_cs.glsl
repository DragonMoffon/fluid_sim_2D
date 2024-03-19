#version 430

layout(local_size_x=1) in;

layout(r32f, binding=0) uniform readonly image2D u_in_data;
layout(r32f, binding=1) uniform writeonly image2D u_out_data;

layout(std430, binding=0) buffer readonly
SimData
{
    float dt;
    float dx;
    float mu;
    float df_x;
    float df_x2;
} sim;

void main() {
    const int img_width = imageSize(u_in_data).x;
    const int index_i = int(gl_GlobalInvocationID.x);
    const int index_im = index_i == 0 ? img_width-1: index_i-1;
    const int index_ip = index_i == img_width-1 ? 0: index_i+1;


    const float u_im = imageLoad(u_in_data, ivec2(index_im, 0)).r;
    const float u_i = imageLoad(u_in_data, ivec2(index_i, 0)).r;
    const float u_ip = imageLoad(u_in_data, ivec2(index_ip, 0)).r;

    float u_n = u_i - u_i * sim.df_x * (u_i - u_im) + sim.mu * sim.df_x2 * (u_ip - 2.0 * u_i + u_im);

    imageStore(u_out_data, ivec2(index_i, 0), vec4(u_n));
}
