# Diffusion and Consistency Models Toy Example

This is a toy example on 1-D data to demonstrate diffusion models and probability flow ODEs, and consistency models (both CD and CT).

It should take about 1~2 minutes on a laptop CPU to train each section.

Following [Consistency Models](https://arxiv.org/abs/2011.13456), this toy example uses the forward SDE is defined as:

$$
    \mathrm d \bold x(t)  = \sqrt{2 t} \mathrm d \bold w(t)
$$

and the probability flow ODE is:

$$
    \mathrm d \bold x(t) = -t \nabla_{\bold x(t)}\log p_t (\bold x(t))\mathrm d t
$$

**Note:** I wish this toy example helps you learn and understand, and it is limited to this purpose. It implements the main techniques mentioned in the paper, but there are still details that are not aligned with the paper or other popular implementations. Please refer to Song's [offical repo](https://github.com/openai/consistency_models) if you are going deeper.

Some related papers:

* Denoising Diffusion Probabilistic Models [2006.11239.pdf (arxiv.org)](https://arxiv.org/pdf/2006.11239.pdf)
* Score-based Generative Modeling through Stochastic Differential Equations [2011.13456.pdf (arxiv.org)](https://arxiv.org/pdf/2011.13456.pdf)
* Denoising Diffusion Implicit Models [2010.02502.pdf (arxiv.org)](https://arxiv.org/pdf/2010.02502.pdf)
* Elucidating the Design Space of Diffusion-Based Generative Models [2206.00364.pdf (arxiv.org)](https://arxiv.org/pdf/2206.00364.pdf)
* Consistency Models [2011.13456.pdf (arxiv.org)](https://arxiv.org/pdf/2011.13456.pdf)