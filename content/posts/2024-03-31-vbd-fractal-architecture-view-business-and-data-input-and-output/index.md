---title: "VBD, Fractal Architecture: View, Business and Data. Input and Output."
date: 2024-03-31 20:44:00 +02:00
draft: false
categories: [writing, software, architecture, layer]
tags: [layer]
layout: post
image: "og-image.svg"
---

<meta property="og:image" content="2024-03-31-vbd-fractal-architecture-view-business-and-data-input-and-output/fractal-maldelbrot-illustration-1000px-gettyimages-488635425-2048x2048.jpg" />

<meta name="twitter:image" content="2024-03-31-vbd-fractal-architecture-view-business-and-data-input-and-output/fractal-maldelbrot-illustration-1000px-gettyimages-488635425-2048x2048.jpg" />

![Maldelbrot set](fractal-maldelbrot-illustration-1000px-gettyimages-488635425-2048x2048.jpg)

One of the main purpose of a computer system is to process data.

And the principle: data travels between services.

Applications have an input and an output:
- Input, the application receives data
- Internally the application process data
- Output, after processing the data, the application produces an output.

With this pattern, applications can be reduced to software that does input and produces output.

You are doing Fractal Architecture when you link the services, then you have a bigger system, sure, thats reasoning is trivial, but with this, your new system can be seen as an autonomous system. And that new system can be used in another bigger systems.

That can be replicated as in fractals, if you zoom, you see the same pattern over and over again.

If you try to extract that pattern from designs, you will find that it is usually repeated. This is related to Fractal Architecture.

If you see this from an holistic point of view, and you put the best effort in your application, with one specific and well designed functionallity, this lead us to a basic design principle: do one thing and do it well, as in the unix-like world.

This has deep implications in microservices, in the case where you design an autonomous service, for a single task and you put a lot of effort in doing that task really well.

You can then link microservices between them, using an orchestrator or not, the key point is to have services that do one task and do it well.
