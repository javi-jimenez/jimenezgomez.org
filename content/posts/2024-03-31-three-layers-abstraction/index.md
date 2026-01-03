---title: "Three layers abstraction"
date: 2024-03-31 20:52:00 +02:00
draft: false
categories: [writing, software, architecture]
tags: [layer, fractal]
layout: post
image: "og-image.svg"
---

![Three Layers as Leafs](three-layers-as-leafs-gettyimages-1000px-157287379-2048x2048.jpg)

The software design can be simplified in three layers:
- View
- Business
- Data

For example, in a web application, you have:
- View, usually in JavaScript, HTML and CSS
- Business, usually JavaScript or a backend API
- Data, the pure data, that can be structured data as a database or a dictionary, for example

If we want to stablish a relation between layers and Fractal Architecture, we can view the previous Business layer as composed of three layers:
- View, the backend API
- Business, the Domain
- Data, the objects that represent the underlying data

In the initial decomposition, the Data layer can be seen again as a three layer design:
- View, the accepted commands and the REPL or API
- Business, the internal logic or the database application
- Data, the internal structures used by the application to effectively store the data

As you see, you can extend the concept to other domains.

This brief idea can be of help when we design or think about architecture.

Finally, to fit this idea into the Fractal Architecture, all three (or any you have) layers, must be considered as an atomic autonomous block with an input and an output, as a black box pattern.
