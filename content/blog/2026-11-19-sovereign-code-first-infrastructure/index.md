---
title: "Sovereign Code-First Infrastructure: Decoupling Business Logic from Persistent Plumbing"
date: 2026-11-19T00:30:00+01:00
draft: false
description: "A sober, architecture-first model in which infrastructure is not a separate deployment artifact but an explicit declarative intent embedded in the code itself."
image: "og-image-1200x630.png"
og_image: "og-image-1200x630.png"
tags:
  - software architecture
  - sovereignty
  - vendor lock-in
  - ports and adapters
  - infrastructure as code
  - compliance
---

Modern software engineering has fallen into a trap of excessive operational friction. Developers spend more time orchestrating Docker networks, configuring connection strings, managing YAML manifests, and tying application code to vendor-specific SDKs than building actual business logic.

This article sets out a sober, architecture-first model in which infrastructure is treated not as a separate deployment artifact, but as an explicit, declarative intent embedded directly within the code. By establishing a universal abstraction layer and ephemeral runtime plumbing, we eliminate vendor lock-in, guarantee local-to-production parity, and restore absolute sovereignty to the engineering lifecycle.

> This piece is adapted from the whitepaper *Sovereign Code-First Infrastructure: Decoupling Business Logic from Persistent Plumbing*, by **Francisco Javier Jiménez Gómez** (BRISECOM SL), written as an architectural position paper for sovereign, vendor-agnostic systems.

## The problem: the accidental complexity of modern stacks

For years, the industry standard for building distributed systems has involved a fractured workflow:

1. Provision infrastructure manually using Infrastructure as Code (IaC) tools such as Terraform.
2. Hardcode environment variables, ports, and proprietary SDK drivers (`pg`, `amqplib`, `@aws-sdk/client-s3`) directly into the application layer.
3. Waste hours debugging local development environments where containers fail to mirror production setups.

This creates tight coupling. If an organisation decides to switch from PostgreSQL to a different storage engine, or from RabbitMQ to NATS, or migrates from local MinIO storage to a sovereign S3-compatible cloud, the codebase suffers a cascade of invasive refactoring. The business logic becomes polluted by infrastructure concerns.

The cost is not only technical. Every hour spent reconstructing a broken local stack is an hour not spent on the problem the software exists to solve. And every proprietary driver embedded in a domain module is a contractual clause written into the architecture on behalf of a vendor.

## The solution: code-first abstraction and ephemeral runtime

To achieve true technical sovereignty, we invert the paradigm. The application should never know *how* a database runs, *where* a queue is hosted, or *what* protocol delivers a file; it should only declare *what* capability it requires.

The architecture rests on three foundational pillars.

### 1. Declarative intent in code

Instead of configuring external files or binding to proprietary drivers, the developer expresses capability directly through clean, typed primitives within the business logic:

> *"This module requires a relational data store, an asynchronous message queue, and an object storage bucket."*

The application code remains entirely pure — defining abstract ports rather than concrete technological dependencies.

```text
module Orders

requires:
    relational store      as orders_db
    asynchronous queue    as events
    object storage        as invoices

operations:
    place_order(cart) -> Order
    settle(order)     -> Receipt
```

Nothing in that declaration names PostgreSQL, RabbitMQ, or S3. Those are decisions, and decisions belong to the environment — not to the domain model. This is, in essence, the same discipline as hexagonal architecture (ports and adapters): the port describes a capability, the adapter supplies a technology. What changes here is that the port is also the *provisioning contract*.

### 2. Transparent ephemeral plumbing and engine provisioning

The developer should never have to manually spin up containers, write complex `docker-compose` networks from scratch, or seed migration scripts by hand.

- Upon initialising the development workspace, an intelligent local engine inspects the application's declared intents.
- It automatically provisions lightweight, ephemeral local containers behind the scenes — for example an isolated PostgreSQL instance, a Redis or NATS broker, and a MinIO object store.
- It injects the initial creation scripts and database migrations transparently, establishing all virtual networking cables without manual intervention.

The key word is *ephemeral*. The local stack is derived, disposable, and reproducible: it exists because the code says it is needed, and it disappears when it is no longer. There is no hand-crafted `docker-compose.yml` to drift, no undocumented port mapping, no "remember to run the seed script" in a wiki page nobody reads.

### 3. Pure business logic isolation

With the plumbing handled entirely by the runtime engine, the program focuses exclusively on execution. The code simply invokes universal verbs:

```text
database.save(order)
queue.push(OrderPlaced, payload)
storage.store(invoice_pdf)
```

The underlying engine maps these calls dynamically to the correct physical driver. In local development they hit ephemeral containers; in production they map to hardened cluster nodes — all **without changing a single line of business logic or binding to a vendor-locked SDK**.

This is the point where the abstraction earns its keep. An abstraction that only hides a single implementation is indirection. An abstraction that can be re-pointed at a different implementation — local, on-premise, or sovereign cloud — without touching the domain is a boundary.

## Architectural implications for sovereign systems

Adopting this code-first, decoupled model yields profound operational advantages, particularly for high-assurance environments requiring rigorous compliance (such as ENS, ISO/IEC 27001, and the EU AI Act):

- **Zero vendor lock-in.** Because the application speaks a universal domain language rather than proprietary cloud APIs, infrastructure can be swapped, migrated, or repatriated to on-premise sovereign hardware instantly.
- **Absolute reproducibility.** Every developer on the team runs the exact same self-provisioned stack derived purely from the application's intent, eliminating the classic *"it works on my machine"* failure mode.
- **Auditable architecture.** System boundaries remain crystal clear. Security audits can verify data flows and storage boundaries at the code level without wading through a maze of scattered configuration files.

There is a fourth consequence worth naming, because it is usually discovered too late: **portability becomes a property of the codebase rather than a negotiation with a provider**. Repatriation stops being a migration project and becomes a configuration change. For a public administration or a regulated SME, that is not an optimisation — it is the difference between owning a system and renting one.

## What this model does not claim

Intellectual honesty requires limits, and an architectural position paper that promises everything is worth nothing.

This model does not eliminate the need to understand storage engines, message brokers, or object stores. It does not make distributed transactions trivial, and it does not remove the obligation to design schemas, delivery guarantees, or retention policies. What it removes is the *coupling* between those decisions and the business logic — and, with it, the accidental complexity that accumulates every time the two are confused.

Nor is it a licence to abstract everything. Only genuine capabilities deserve a port. A port created for a technology that will never change is just a layer of indirection with a maintenance bill attached.

## Conclusion

True software sovereignty begins by stripping away accidental complexity. By treating infrastructure as a runtime abstraction derived directly from application intent — backed by automated, transparent local provisioning — we empower engineering teams to build resilient, portable, and maintainable systems that outlive any single cloud provider or technology stack.

The business logic should describe the business. Everything else is plumbing, and plumbing should be provisioned, not hand-soldered into the walls.
