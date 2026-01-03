---title: "Vera Architecture"
date: 2025-04-04T11:09:00+02:00
draft: false
layout: post
image: "og-image.svg"
---

<meta property="og:image" content="vera-arch-202504041121.drawio.png" alt="Vera Architecture" />

<meta name="twitter:image" content="vera-arch-202504041121.drawio.png" alt="Vera Architecture" />

![Vera Architecture](vera-arch-202504041121.drawio.png)

Vera Architecture or Vero Architecture, how it was called initially by me in around year 2000, is a software architecture based on interfaces and abstract data types (ADT).

It isolates the business logic from any kind of external data.

The core of the architecture is the business logic.

Internally the business logic defines and uses internal Abstract Data Types, which are data structures.

Externally there exists the data in some formats.

For communication between spaces, it uses SWIVELS, which are the core of the movable parts: business and data.

Nowadays, there is something similar called Hexagonal Architecture.

You can exchange in real-time the data parts, that allows, for example, to store data in a file, and later, switch to database without noticing it in the business.

Each node can be developed independently from one to another, you only take into account the interfaces, which are the same between all data nodes for a SWIVEL.

The uniformity in the data formats come from projects as schema.org, which tries to define which fields are common in objects as person, cinema or city, for example.

If you define the same object person in different applications, you can give uniformity to that using standarization formats as the provided by schema.org or similar projects, but you have to choose one of them, to avoid fragmentation.
