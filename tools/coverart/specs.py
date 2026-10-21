"""Qué portada lleva cada artículo.

`motif`  — el dibujo (ver `motifs.py`)
`palette`— los colores (ver `palettes.py`)
`eyebrow`— serie o categoría, en mono y mayúsculas
`sub`    — una línea de contexto; vacío para portadas más gráficas
`opts`   — ajustes del motivo

Regla: ninguna pareja (motif, palette) se repite. Si dos artículos comparten
tema, comparten motivo pero cambian de paleta y de parámetros, de modo que se
reconocen como familia sin confundirse.
"""

SPECS = {
    # ---------------------------------------------------------------- 2023
    "2023-05-17-internet-of-services": dict(
        motif="mesh", palette="cobalt", eyebrow="Architecture",
        sub="Services as the unit of composition.",
    ),
    "2023-05-17-network-operative-system": dict(
        motif="ring", palette="teal", eyebrow="Systems",
        sub="One machine made of many.",
    ),
    "2023-05-17-why-to-improve": dict(
        motif="steps", palette="amber", eyebrow="Craft",
        sub="Improvement is a direction, not a destination.",
    ),
    "2023-07-01-quotes": dict(
        motif="quote", palette="sepia", eyebrow="Notebook",
        sub="Sentences worth keeping.",
        opts={},
    ),
    "2023-10-13-why-to-improve-2-look-for-base-technologies": dict(
        motif="strata", palette="sand", eyebrow="Craft · II",
        sub="Dig until you reach something that does not move.",
        opts={"bands": 8, "hi": 5},
    ),
    "2023-10-14-why-to-improve-3-base-materials-for-computer-engineers": dict(
        motif="lattice", palette="rust", eyebrow="Craft · III",
        sub="The materials a computer engineer is actually made of.",
    ),
    "2023-10-18-computer-science-base-technologies": dict(
        motif="circuit", palette="moss", eyebrow="Foundations · I",
        sub="Below the framework, the transistor.",
    ),
    "2023-10-19-computer-science-base-technologies-2": dict(
        motif="circuit", palette="copper", eyebrow="Foundations · II",
        sub="Below the transistor, the physics.",
    ),
    "2023-12-24-monoliths-and-microservices": dict(
        motif="bricks", palette="graphite", eyebrow="Architecture",
        sub="Same wall, different grain.",
        opts={"split": 3},
    ),
    # ---------------------------------------------------------------- 2024
    "2024-02-01-deb-get-winget-linux": dict(
        motif="tiles", palette="forest", eyebrow="Tooling",
        sub="Package managers, and the ones that get in the way.",
    ),
    "2024-03-31-layers": dict(
        motif="layers", palette="ice", eyebrow="Architecture",
        sub="Every layer hides the one below.",
        opts={"n": 4, "hi": 1},
    ),
    "2024-03-31-three-layers-abstraction": dict(
        motif="layers", palette="wine", eyebrow="Architecture",
        sub="Three levels, and the discipline of not skipping one.",
        opts={"n": 3, "hi": 1},
    ),
    "2024-03-31-vbd": dict(
        motif="fractal", palette="golds", eyebrow="Architecture",
        sub="View, Business, Data — the same shape at every scale.",
        opts={"levels": 4},
    ),
    "2024-03-31-vbd-fractal-architecture-view-business-and-data-input-and-output": dict(
        motif="fractal", palette="violet", eyebrow="Architecture · Deep dive",
        sub="Fractal architecture, drawn from the inside out.",
        opts={"levels": 6},
    ),
    "2024-05-10-second": dict(
        motif="bars", palette="cobalt", eyebrow="Performance",
        sub="What the browser spends, and what it returns.",
        opts={"n": 13, "hi": 9},
    ),
    "2024-05-14-how-to-improve": dict(
        motif="arrow", palette="ember", eyebrow="Craft",
        sub="A method, not a mood.",
    ),
    # ---------------------------------------------------------------- 2025
    "2025-02-25-ia-development-based": dict(
        motif="neural", palette="plum", eyebrow="LAIA",
        sub="Development with an assistant that remembers.",
    ),
    "2025-03-17-minimal-blog": dict(
        motif="lattice", palette="papercool", eyebrow="Design",
        sub="Remove until it breaks, then add one thing back.",
    ),
    "2025-04-04-vero-architecture": dict(
        motif="blueprint", palette="paperwarm", eyebrow="Architecture",
        sub="VERO: a drawing before a system.",
    ),
    "2025-05-16-apps": dict(
        motif="tiles", palette="indigo", eyebrow="Software",
        sub="Small programs, large consequences.",
    ),
    "2025-12-02-08-54-SPA-blog-in-one-file": dict(
        motif="telescope", palette="ocean", eyebrow="Web",
        sub="A whole blog, in a single file.",
        opts={"n": 6},
    ),
    "2025-12-18-laia-brand-identity": dict(
        motif="star", palette="golds", eyebrow="LAIA · Identity",
        sub="The image of an idea that refuses decoration.",
    ),
    "2025-12-18-laia-intelligent-agent": dict(
        motif="symbols", palette="paper", eyebrow="LAIA",
        sub="Axioms, inferences, and the ∎ that closes a proof.",
        opts={"hi": 2},
    ),
    "2025-12-22-dns-universal-ddnsc": dict(
        motif="orbits", palette="teal", eyebrow="Distributed systems",
        sub="Names that resolve from a planet away.",
    ),
    "2025-12-30-assistant-context-standard": dict(
        motif="telescope", palette="ice", eyebrow="Standard · Proposal",
        sub="Continuity between sessions, written down.",
        opts={"n": 5},
    ),
    "2025-12-30-ia-formal-vs-ml-draft": dict(
        motif="duality", palette="graphite", eyebrow="Draft",
        sub="Formal languages and machine learning, priced honestly.",
    ),
    # ---------------------------------------------------------------- 2026
    "2026-01-02-assistant-context-standard": dict(
        motif="flow", palette="moss", eyebrow="Standard",
        sub="One protocol, many assistants.",
    ),
    "2026-01-03-documento-tecnico-framework-acs": dict(
        motif="blueprint", palette="cobalt", eyebrow="ACS · Technical",
        sub="The framework, dimensioned.",
    ),
    "2026-01-03-domando-el-caos-de-la-ia": dict(
        motif="chaos", palette="burgundy", eyebrow="AI",
        sub="Randomness on the left, a system on the right.",
    ),
    "2026-01-06-smartphone-sin-sim-y-telefono-basico": dict(
        motif="waves", palette="sand", eyebrow="Resilience",
        sub="Two devices that cannot both fail at once.",
    ),
    "2026-01-28-la-fe": dict(
        motif="rays", palette="amber", eyebrow="Essay",
        sub="What remains when the evidence runs out.",
    ),
    "2026-01-30-callbacks-ai-linearize": dict(
        motif="flow", palette="violet", eyebrow="Code",
        sub="Straighten the arrow, keep the meaning.",
    ),
    "2026-01-31-l-encobert-el-encubierto": dict(
        motif="mask", palette="burgundy", eyebrow="Fiction",
        sub="Half of the story is the part that is not lit.",
    ),
    "2026-02-26-el-espejismo-del-open-source-libertad-o-despojo-programado": dict(
        motif="dunes", palette="ember", eyebrow="Essay",
        sub="Freedom, or a dispossession with better marketing.",
    ),
    "2026-08-20-universal-data-container": dict(
        motif="container", palette="copper", eyebrow="Data",
        sub="SQL and JSON, in the same box.",
    ),
    "2026-09-07-contract-first-interface-agnostic-design": dict(
        motif="seal", palette="paperwarm", eyebrow="Architecture",
        sub="Design the agreement; the interface is a detail.",
    ),
    "2026-10-12-desktop-launcher-creator": dict(
        motif="tiles", palette="amber", eyebrow="Tooling",
        sub="A launcher for the apps that ship without one.",
    ),
    "2026-10-16-neptuno-network-collaborative-framework": dict(
        motif="mesh", palette="teal", eyebrow="Neptuno Network",
        sub="People, agents and one accountability line.",
    ),
    "2026-10-21-working-as-equals-ethics-as-infrastructure": dict(
        motif="plinth", palette="midnight", eyebrow="AI ethics · EU AI Act",
        sub="Built before the first commit, not signed after the last audit.",
    ),
}
