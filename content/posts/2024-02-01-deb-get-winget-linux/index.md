---
title: "deb-get: The \"winget\" for Linux that you need to avoid Snap problems"
date: 2024-02-01T09:00:00+01:00
draft: false
layout: post
image: "og-image.svg"
author: "Francisco Javier"
reviewer: "Enrique Jiménez Gómez"
version: "1.0"
tags:
---
# deb-get: The winget for Linux you need to avoid Snap problems

Author: DeepSeek AI | Reviewed and edited by: Enrique Jiménez Gómez
Published in: jimenezgomez.org | Version: 1.0 | Date: February 2024


## Credits and Creation Process

### Authorship and Participation:

This article is the result of a collaboration between artificial intelligence and real practical experience:

DeepSeek AI (80%):
- Technical research of `deb-get` and alternatives
- Writing structured content
- Code and command examples
- Comparative analysis between package systems
- Documentation of functionalities and features

Enrique Jiménez Gómez (20%):
- Real hands-on experience with Snap issues
- Validation of commands and procedures
- Editorial direction and focus of the article
- Real use cases and documented problems
- Technical review and corrections based on experience

### Development Process:
1. February 2024 - Enrique documents real problems with Snap on his system
2. Research - Search for alternatives to container systems
3. Practical tests - Validation of `deb-get` in real environments
4. Writing - Creation of content structured by DeepSeek
5. Review - Correction and validation by Enrique based on practical experience

### Article Context:
This content arises from actual documented issues that Enrique experienced on his blog jimenezgomez.org, specifically:
- Cryptic Snap errors ("change finished in status \"Hold\"")
- Blocked processes impossible to resolve
- Frustration expressed: "what a nonsense snap..."
- The active search for practical alternatives


## The Problem: Why Snap is not always the solution

If you use Ubuntu or some derived distribution, you have surely encountered this frustrating situation:

```bash
sudo snap remove firefox --revision=7599
error: snap "firefox" has "remove-snap" change in progress
```

Or worse yet:
```bash
error: change finished in status "Hold" with no error message
```

These cryptic errors and blocked processes are common experiences for Snap users. The system introduces unnecessary complexity compared to `.deb` packages.

## The Solution: deb-get, the "winget" for Linux

Imagine having the simplicity of `winget` but for `.deb` applications on Linux. That's `deb-get`.

### What is deb-get?

`deb-get` is a high-level package manager that simplifies the installation of third-party applications in `.deb` format. It acts as a layer on top of `apt` and `dpkg`, providing a unified interface.

### Installation in a single command:

```bash
wget -qO- https://raw.githubusercontent.com/wimpysworld/deb-get/main/deb-get | sudo bash -s install deb-get
```

##Why deb-get is superior to Snap

### 1. Native Performance
Applications installed with `deb-get` are traditional `.deb`: immediate startup, full integration, and no container overhead.

### 2. Simplified Management
```bash
deb-get search firefox
deb-get install google-chrome-stable
deb-get upgrade
deb-get list
```

### 3. No Locks or "Hold" States
Avoid blocked background processes and mysterious states.

### 4. Transparency and Control
You can see exactly what is installed, check GPG signatures, and inspect files.

## Catalog of examples
```bash
deb-get install google-chrome-stable
deb-get install vscode
deb-get install signal-desktop
```

## Integration with your workflow

Examples for casual user, administrator and developer included in the original article.

## Conclusion: Back to simple

`deb-get` is not magic, but it is a practical answer to manage third-party applications without the complications of Snap.

---

Relevant links:
- https://github.com/wimpysworld/deb-get
- https://github.com/wimpysworld/deb-get/wiki