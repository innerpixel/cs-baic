# 22. Mermaid Diagrams

The diagrams below use simple Mermaid syntax and a muted dark gray visual style.

Recommended use:

- Put these in the project README.
- Reuse them in the product website planning docs.
- Keep them updated as the product changes.

---

## 22.1 Product Flow Diagram

```mermaid
flowchart TD

A[Business documents]
B[AI inbox]
C[Classify]
D[Summarize]
E[Extract fields]
F[Suggest action]
G[Draft reply]
H[Human review]
I[Approved action]
J[Audit log]
K[Ask my company]
L[Company knowledge]

A --> B
B --> C
B --> D
B --> E
C --> F
D --> F
E --> F
F --> G
G --> H
H --> I
I --> J
B --> L
L --> K
K --> H

classDef dark fill:#2f3437,stroke:#8a8f93,color:#f2f2f2,stroke-width:1px
classDef core fill:#3d4448,stroke:#a0a6aa,color:#ffffff,stroke-width:2px
classDef action fill:#4b5256,stroke:#b2b8bc,color:#ffffff,stroke-width:2px

class A,L dark
class B,K core
class C,D,E,F,G,H,I,J action
```

---

## 22.2 Project Roadmap Diagram

```mermaid
flowchart TD

P0[Product definition]
P1[Website]
P2[Clickable demo]
P3[Real AI workflow]
P4[Pilot users]
P5[Product version]

P0 --> P1
P1 --> P2
P2 --> P3
P3 --> P4
P4 --> P5

P0a[Name]
P0b[Offer]
P0c[Demo story]
P0d[Synthetic data]

P0 --> P0a
P0 --> P0b
P0 --> P0c
P0 --> P0d

P2a[AI inbox mock]
P2b[Ask company mock]
P2c[Approval mock]

P2 --> P2a
P2 --> P2b
P2 --> P2c

P3a[Upload]
P3b[Classify]
P3c[Extract]
P3d[Answer]

P3 --> P3a
P3 --> P3b
P3 --> P3c
P3 --> P3d

classDef dark fill:#2f3437,stroke:#8a8f93,color:#f2f2f2,stroke-width:1px
classDef phase fill:#3d4448,stroke:#a0a6aa,color:#ffffff,stroke-width:2px
classDef task fill:#4b5256,stroke:#b2b8bc,color:#ffffff,stroke-width:1px

class P0,P1,P2,P3,P4,P5 phase
class P0a,P0b,P0c,P0d,P2a,P2b,P2c,P3a,P3b,P3c,P3d task
```

---

## 22.3 System Architecture Diagram

```mermaid
flowchart TD

U[User]
F[Frontend]
A[Backend API]
W[Workspace service]
D[Document service]
Q[Job queue]
P[Parser]
M[AI service]
V[Vector search]
DB[Database]
S[File storage]
L[Audit log]

U --> F
F --> A
A --> W
A --> D
D --> S
D --> Q
Q --> P
P --> M
M --> DB
M --> V
V --> M
A --> DB
A --> L
M --> L
F --> L

classDef dark fill:#2f3437,stroke:#8a8f93,color:#f2f2f2,stroke-width:1px
classDef front fill:#3d4448,stroke:#a0a6aa,color:#ffffff,stroke-width:2px
classDef core fill:#4b5256,stroke:#b2b8bc,color:#ffffff,stroke-width:2px
classDef data fill:#25292c,stroke:#8a8f93,color:#f2f2f2,stroke-width:1px

class U,F front
class A,W,D,Q,P,M,V core
class DB,S,L data
```

---

## 22.4 Simple MVP Dependency Diagram

```mermaid
flowchart TD

A[Website copy]
B[Demo story]
C[Synthetic data]
D[Mock dashboard]
E[Upload flow]
F[AI classify]
G[AI summarize]
H[AI extract]
I[Ask company]
J[Human approval]
K[Pilot demo]

A --> B
B --> C
C --> D
D --> E
E --> F
E --> G
E --> H
G --> I
H --> I
F --> J
G --> J
H --> J
I --> J
J --> K

classDef dark fill:#2f3437,stroke:#8a8f93,color:#f2f2f2,stroke-width:1px
classDef main fill:#3d4448,stroke:#a0a6aa,color:#ffffff,stroke-width:2px
classDef build fill:#4b5256,stroke:#b2b8bc,color:#ffffff,stroke-width:1px

class A,B,C main
class D,E,F,G,H,I,J,K build
```

---

## 22.5 Notes on Mermaid Style

Keep Mermaid labels simple:

- avoid slashes
- avoid quotes
- avoid parentheses
- avoid long text inside nodes
- avoid special characters where possible
- use short node names
- explain details outside the diagram

Recommended palette:

- background feeling: charcoal gray
- standard node: `#2f3437`
- main node: `#3d4448`
- action node: `#4b5256`
- storage node: `#25292c`
- stroke: `#8a8f93`
- bright stroke: `#b2b8bc`
- text: `#f2f2f2`

This gives the diagrams a darker, grayish style without becoming unreadable.

---