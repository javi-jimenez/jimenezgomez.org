---
title: "From Unix Commands to APIs: Designing Software Around Contracts, Not Interfaces"
date: 2026-09-07
draft: false
layout: post
image: "og-image.svg"
og_image: og-image.svg
tags:
  - software architecture
  - unix
  - APIs
  - design
---

# From Unix Commands to APIs: Designing Software Around Contracts, Not Interfaces

There is a recurring problem in software engineering that is rarely discussed explicitly: we often design the program around its user interface.

A command-line application becomes a collection of commands. A web application becomes a collection of HTTP endpoints. A desktop application becomes a collection of screens and event handlers.

Then, sooner or later, someone wants an API, a CLI, a GUI, a Python library, or a browser extension.

The result is often duplication, adapters built on top of other adapters, and business logic scattered across presentation layers.

There is another way.

The approach I have been exploring can be summarized as:

> **Define the operation and its input/output contract first. Make the interface an adapter.**

I would call this **Contract-First, Interface-Agnostic Design**.

It is not a completely new architecture. It is a practical combination of several established ideas: Unix philosophy, separation of concerns, hexagonal architecture (Ports and Adapters), structured data contracts, and file-based persistence.

But putting them together leads to a particularly useful design style for small Unix-oriented tools.

## The Interface Should Not Define the Program

Consider a simple operation:

```text
get secret
```

The important question is not whether this operation is exposed through HTTP or a shell command.

The important question is:

```text
What does "get secret" mean?

What does it receive?

What does it return?

What errors can it produce?
```

For example:

```text
Input:
    path = "brisecom/ovh"

Output:
    name
    type
    content
    metadata

Errors:
    NOT_FOUND
    ACCESS_DENIED
    DECRYPTION_FAILED
```

Once this contract exists, many interfaces can implement it.

A command-line interface might expose:

```bash
secrets get brisecom/ovh
```

An HTTP API might expose:

```http
GET /v1/secrets/brisecom/ovh
```

A Python client might expose:

```python
secrets.get("brisecom/ovh")
```

A graphical application might present:

```text
Secrets
+-- brisecom
    +-- ovh
```

But underneath, they are all invoking the same operation.

The operation is the important abstraction.

The interface is not.

## Unix Already Had This Idea

The Unix philosophy has always encouraged small programs that do one thing well and communicate through simple interfaces.

For example:

```bash
cat file | grep something | sort
```

Each program has a relatively simple contract:

```text
input -> processing -> output
```

Standard input, standard output, standard error and exit codes provide a surprisingly powerful protocol.

The problem is that modern application development often abandons this simplicity.

Instead of:

```text
input -> operation -> output
```

we get:

```text
HTTP request
    |
controller
    |
framework
    |
service
    |
ORM
    |
database
    |
model
    |
serializer
    |
HTTP response
```

Sometimes all of that is justified.

Sometimes it is simply accidental complexity.

## Structured Output Changes Everything

A traditional Unix command might print:

```text
Secret found: brisecom/ovh
Username: paco
Password: ********
```

That is convenient for a human but difficult for another program to consume reliably.

Instead, the command can provide structured output:

```json
{
  "ok": true,
  "data": {
    "name": "brisecom/ovh",
    "username": "paco",
    "password": "..."
  },
  "error": null
}
```

Now the same program becomes useful to both humans and machines.

For example:

```bash
secrets get brisecom/ovh | jq .data.password
```

The CLI has effectively become a small API over standard output.

This is an important design principle:

> **Machine-readable output should be a first-class interface, not an afterthought.**

For CLI programs, I particularly like the traditional Unix separation:

```text
stdout  -> data
stderr  -> human diagnostics
exit code -> success/failure
```

That gives shell scripts a stable contract without sacrificing usability for humans.

## The Core Should Know Nothing About HTTP

Suppose we implement:

```python
def get_secret(path):
    ...
```

That function should not know whether the caller is:

- a browser,
- curl,
- a Python program,
- a desktop application,
- a shell script,
- or another server.

It should simply perform the operation and return a result.

Bad design:

```python
def get_secret(path):
    print("Looking for secret...")
    return jsonify(...)
```

Now the business operation knows about both the console and HTTP.

A better design is:

```python
def get_secret(path):
    return store.get(path)
```

The HTTP layer converts that result into HTTP.

The CLI layer converts it into terminal output.

The Python library exposes it as a Python object.

The core remains independent.

This is essentially the **Ports and Adapters** idea applied at a very practical scale.

## Files Can Be the Authority

This becomes particularly interesting when the persistent data is deliberately kept outside the service.

Imagine a secret store:

```text
~/.password-store/

+-- github.gpg
+-- google.gpg
+-- amazon.gpg
|
+-- brisecom/
    +-- ovh.gpg
    +-- cloudflare.gpg
```

The service does not own a database containing these secrets.

The files are the authority.

GPG provides encryption.

The filesystem provides persistence.

Git can provide versioning.

Syncthing can provide synchronization.

A service can provide an API.

A GUI can provide a graphical interface.

A browser extension can provide browser integration.

The architecture becomes:

```text
                 ENCRYPTED FILES
                       |
        +--------------+--------------+
        |              |              |
       GPG            Git         Syncthing
        |
        v
      SERVICE
        |
   +----+-----+---------+
   |    |     |         |
  CLI  API   GUI    Browser
```

This is a very different philosophy from:

```text
Application
     |
Database
     |
Everything
```

The service becomes replaceable.

The data does not depend on the service.

## A File Does Not Have to Contain Text

This principle also avoids a common mistake: assuming that everything in a secrets system is a string.

Credentials can be text.

But secrets can also be:

```text
private keys
TLS certificates
PKCS#12 files
SSH keys
client certificates
configuration files
binary credentials
```

There is no reason to turn every one of these into a JSON record.

A file-based service can preserve the original object:

```text
certificate.p12.gpg
private-key.pem.gpg
client.key.gpg
```

The encrypted file remains opaque.

When requested, the service decrypts it and returns the original bytes.

This leads to another useful distinction:

```text
Structured secret -> JSON
Binary secret     -> bytes
```

The API does not need to understand every type of secret.

It only needs to understand the contract for storing and retrieving them.

## The API Becomes an Adapter

Once the core operations are defined, an HTTP API becomes relatively boring.

And that is a good thing.

For example:

```http
GET    /v1/secrets
GET    /v1/secrets/{path}
PUT    /v1/secrets/{path}
DELETE /v1/secrets/{path}
```

The HTTP layer does four basic things:

```text
HTTP request
    |
validate input
    |
invoke operation
    |
serialize result
```

It should not contain the actual storage logic.

The CLI does essentially the same:

```text
CLI arguments
    |
validate input
    |
invoke operation
    |
serialize result
```

The difference is only the transport.

This is why designing the contract before designing the interface is so powerful.

## One Core, Many Interfaces

The resulting architecture is surprisingly simple:

```text
                    +------------+
                    |    Core    |
                    | Operations |
                    +------+-----+
                           |
             +-------------+-------------+
             |             |             |
            CLI           HTTP        Library
             |             |             |
          terminal      REST/JSON    Python/Go
```

The interfaces are replaceable.

The core operations are stable.

The persistent data is independent again.

That gives us three particularly useful layers:

```text
DATA
  |
SERVICE
  |
INTERFACE
```

For a Unix-oriented system, this is an extremely natural decomposition.

## This Is Not Microservices

There is an important distinction here.

This architecture does not require dozens of services.

In fact, it often works best with one small program.

For example:

```text
secretsd
```

could be a single Go binary providing:

```text
CLI
Unix socket
HTTP API
```

while the underlying storage remains:

```text
filesystem + GPG
```

There is no need for:

```text
Kubernetes
database cluster
message broker
ORM
service mesh
```

unless the actual problem requires them.

The objective is not distributed architecture.

The objective is **clear boundaries**.

## A Useful Set of Rules

When designing this kind of application, I find the following rules useful.

### 1. Define operations before interfaces

Start with:

```text
get
put
delete
list
generate
```

not:

```text
GET /api/...
POST /api/...
```

### 2. Define input and output explicitly

Every operation should have a recognizable contract.

```text
Input -> Operation -> Result
```

### 3. Keep presentation out of the core

The core should not know about:

```text
HTML
HTTP
terminals
GTK
React
```

### 4. Make machine-readable output first-class

Use structured output where appropriate.

JSON is useful, but not mandatory for binary data.

### 5. Use Unix conventions

For CLI applications:

```text
stdout = data
stderr = diagnostics
exit code = status
```

### 6. Keep persistent data independent

If the filesystem is the authority, the service should not secretly create another database containing the same information.

### 7. Make interfaces replaceable

You should be able to remove the GUI without losing the data.

You should be able to replace the HTTP server without migrating the secrets.

You should be able to access the files directly when necessary.

### 8. Treat errors as part of the contract

Do not make callers parse human error messages.

Prefer:

```text
NOT_FOUND
ACCESS_DENIED
INVALID_INPUT
DECRYPTION_FAILED
```

with human-readable descriptions attached.

## The Deeper Principle

The interesting part is not really REST.

It is not JSON.

It is not even Unix.

The deeper principle is this:

> **Separate what the program does from how somebody talks to it.**

Once that separation exists, adding an interface becomes relatively cheap.

Want a CLI?

Add an adapter.

Want REST?

Add an adapter.

Want a Python library?

Add an adapter.

Want a GUI?

Add an adapter.

Want a browser extension?

Add an adapter.

The underlying operation remains the same.

## From “Application” to “System”

This way of thinking also changes how I understand small Unix programs.

A program does not necessarily need to be a complete application.

It can be a **capability**.

For example:

```text
GPG
```

provides cryptographic capability.

```text
filesystem
```

provides persistent storage.

```text
pass
```

provides a password-management interface.

A new service can provide an API over the same underlying capability.

A GUI can provide another interface.

A browser extension can provide another.

The pieces remain useful independently.

This is very close to the original Unix idea of composing simple tools, but applied to modern APIs and software architecture.

## Conclusion

I do not think the answer to modern software complexity is always another framework.

Sometimes the better approach is to go back to a simpler question:

```text
What does this program actually do?
```

Then define that operation clearly:

```text
Input
  |
Operation
  |
Output / Error
```

Everything else can become an interface.

For systems such as a file-based secrets manager, this produces an architecture that is both traditional and modern:

```text
Encrypted files
      |
   GPG/filesystem
      |
    Service
      |
 +----+-----+-----+
CLI   API   GUI   Browser
```

The data remains portable.

The service remains replaceable.

The interfaces remain independent.

And the API is no longer something that has to be “added” to the application later.

**The API is simply another way of talking to the same program.**
