# Heitz Bluenoise SSBO Generator
This is the repository to generate ready-to-use bluenoise sampling SSBO data for your Iris shaders.

I wrote this originally to use in my [Lyrae Shaderpack](https://modrinth.com/shader/lyrae-shaders). If you use it and find it helpful, I'd appreciate attribution.

<img src="https://raw.githubusercontent.com/kadir014/iris-heitz-bluenoise-gen/refs/heads/main/github_assets/lyrae_noise_findings.png" width=600>

You can see my findings on different noise methods and how it affects a path traced sc ene.

### Where can I use this?
This is meant to be used in path tracers or other graphical stochastic applications where Monte-Carlo sampling error exists.

### Why should I use this?
Usually at low sample amounts Monte-Carlo produces high-variance and dissimilar pixels which results in white noise. Heitz et al (see references) provides a solution that uses a low-discripancy sampling method to distribute error as blue noise.



# Generation
Make sure you have Python 3.12+ installed. Clone the repository and enter it.
```shell
$ git clone https://github.com/kadir014/iris-heitz-bluenoise-gen.git
$ cd iris-heitz-bluenoise-gen
```

Run the generator with the required spp amount (you can also use `-h`). It is going to generate the SSBO file which you can simply plug in and use in your Iris shaders.
```shell
$ python gen.py <spp>
```


# Usage
First you need to tell Iris to load in the SSBO file.
```properties
#// SSBO size = 128 * 128 * 8 * 2 + 256 * 256
bufferObject.X = 1310720 data/heitz_bluenoise_Nspp.ssbo
```

In the shader pass you're going to sample bluenoise, you need to define the same SSBO layout with the index. The order is the same as the data file.
```glsl
layout(std430, binding = X) readonly buffer BluenoiseLayout {
    int heitz_ranking[131072]; // 128 * 128 * 8
    int heitz_scrambling[131072]; // 128 * 128 * 8
    int heitz_sobol[65536]; // 256 * 256
};
```

And finally, you can use `heitz_sample` function with the correct state for bluenoise sampling. (The code is directly from the paper, modified slightly to be used in GLSL.)
```glsl
ivec2 heitz_state_pixel;
int heitz_state_sample;
int heitz_state_dimension;

float heitz_sample() {
    int pixel_i = heitz_state_pixel.x;
    int pixel_j = heitz_state_pixel.y;

    // Wrap arguments
    pixel_i = pixel_i & 127;
    pixel_j = pixel_j & 127;
    int sample_idx = heitz_state_sample & 255;
    int sample_dim = heitz_state_dimension & 255;

    // XOR index based on optimized ranking
    int ranked_sample_idx = sample_idx ^ heitz_ranking[sample_dim + (pixel_i + pixel_j * 128) * 8];

    // Fetch value in sequence
    int value = heitz_sobol[sample_dim + ranked_sample_idx * 256];

    // If the dimension is optimized, xor sequence value based on optimized scrambling
    value = value ^ heitz_scrambling[(sample_dim % 8) + (pixel_i + pixel_j * 128) * 8];

    // Increase dimension after each call
    // Uncomment this if you have temporal accumulation
    // heitz_state.dim += 1;

    return (0.5 + float(value)) / 256.0;
}
```



# References
This repository wouldn't be possible without E. Heitz's work. Please check out their paper:
- E. Heitz et al — [A Low-Discrepancy Sampler that Distributes Monte Carlo Errors as a Blue Noise in Screen Space](https://eheitzresearch.wordpress.com/762-2/)



# License
[GNU GPL v3](LICENSE) © Kadir Aksoy