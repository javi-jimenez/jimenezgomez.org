---
og_image: og-image-1200x630.png
image: og-image-1200x630.png
---

---title: "Monoliths and microservices"
date: 2023-12-24T00:00:00+02:00
draft: false
categories: [writing, software, architecture, layer]
tags: [monolith, microservice]
layout: post
image: "og-image.svg"
---

<!-- preview image on social media -->
<meta property="og:image" content="2023-12-24-monoliths-and-microservices/inca-bricks-1000px.jpg" />

![Monoliths and MicroServices](inca-bricks-1000px.jpg)

Monoliths are the first approach to an application build.

Microservices are the refinement and the evolution of monoliths.

If the system is designed carefuly from the begining, a system composed of microservices can be built. But the base is always a monolith, not as complex as some final products that must be converted to microservices.

Commonly, a monolith is a big microservice, that is, a complex system that must be divided or splitted into parts to manage it properly.

It happens the same as with files that compose an application, which have a lot of methods or are very complex, the recommendation is to reduce the size and complexity of the file. By that reason, big files and big applications, share the same principle (problem), complexity.

Microservices allow to reduce complexity, between other things.

A system composed with microservices and a monolith are, almost the same. The monolith calls to other funcionalities are made using libraries, the calls in a system composed by microservices are made using message queues, but in essence, it is the same.

The only difference is the way to call methods, or better said, to call funcionality.

Abstracting the concept, we can write an application that call to methods, but internally it is calling to other remote services, that has been doing from time ago.

If you want to center your efforts in architecture, you can design services that can be used to compose multiple big systems. That will allow you to think in sharing functionality. You must center your efforts in functionality, and you must design and build the minimal autonomous system. That minimal autonomous system must be perfected and reused. Microservices, with remote calls, ease this, in relation to distributing systems, but the diagram must be the same as with monoliths.

The base for reusing funcionality, modules, services or whatever is to build the minimal functionality in one module, an autonomous system.

The diagram in a monolith or a microservice must be the same, the only change is the way calls are made. You must abstract it the most you can to get that.

A requirement for making autonomous systems is to develop based on the use of interfaces. Today we know API, which is the same idea. A public face to the world.

As a final note I must to say that you must to specify the ADT or Abstract Data Type or your internal data structures, the allowed input and the allowed or expected output.

And as another useful tip: An interesting standarization of Abstract Data Types is the project schema.org, which contains vocabularies for including and standarize those data types. For example, you know what to expect when working with a postal address, it has a postal code, it is a street or other type of place, and similar things. With that, when you receive an Address compliant with schema.org, you know what the names of the fields are and which is the meaning of each field.

