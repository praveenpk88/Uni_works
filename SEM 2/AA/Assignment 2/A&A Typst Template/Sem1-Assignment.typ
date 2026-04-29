// Typst Template V1
// Based off the LaTeX template for COSC2123 Semester 1 Take-Home Assignment
// Open, Edit and do more at https://typst.app/
// Errare humanum est

#set page(margin: 2cm,
          numbering: "1")
#place(top + left, dx: -1cm, dy: -1cm, image("images/rmit_logo.png", width: 4cm))

#set text(size: 12pt,
          font: "Libertinus Serif Display",
          lang: "en",
          region: "au")
#set par(justify: true)
#set align(center)

#let rmit-red = rgb(228,2,58)

= Algorithms and Analysis Report
== COSC2123/3119
== Graph Algorithms in Action: Modelling a Disease Outbreak

#set text(font: "Libertinus Serif")
== Your Name & Student Number Here
#linebreak()

#table(
  columns: (auto, 2fr),
  inset: 7pt,
  align: left,
  table.header(text(fill: rmit-red)[*Assessment Type*],[ Individual assignment. Submit online via GitHub.]),
  table.header(text(fill: rmit-red)[*Due Date*],[Week 11, Thursday May 21, 13:00 (1pm). A late penalty will apply to assessments submitted after 13:00.]),
  table.header(text(fill: rmit-red)[*Marks*],[30])
)

#set align(left)
= #text(fill: rmit-red)[1 -- Learning Outcomes]

This assessment relates to four learning outcomes of the course which are:

#list(
  indent: 1.5em,
  spacing: 1.25em,
  tight: true,
  [CLO 1: Compare, contrast, and apply the key algorithmic design paradigms: brute force, divide and conquer, decrease and conquer, transform and conquer, greedy, dynamic programming and iterative improvement;],
  [CLO 2: Compare, contrast, and apply key data structures: trees, lists, stacks, queues, hash tables and graph representations;],
  [CLO 3: Define, compare, analyse, and solve general algorithmic problem types: sorting, searching, graphs and geometric;],
  [CLO 4: Theoretically compare and analyse the time complexities of algorithms and data structures; and],
  [CLO 5: Implement, empirically compare, and apply fundamental algorithms and data structures to real-world problems.]
)


= #text(fill: rmit-red)[2 -- Overview]
Across multiple tasks in this assignment, you will model a disease outbreak in the city of Metropolis as a weighted graph to capture residents’ contacts, implement and compare algorithms for estimating infection risk through the population, and design a dynamic programming strategy to allocate scarce antiviral treatment as effectively as possible. Some components ask you to critically assess your solutions through both theoretical analysis and controlled empirical experiments, encouraging reflection on the relationship between algorithm design and real-world performance.

#rect(
  width: 100%,
  stroke: 1pt + black,
  inset: 10pt,
  [
    _I certify that this is all my own original work. If I took any parts from elsewhere, then they were non-essential parts of the assignment, and they are clearly attributed in my submission. I will show I agree to this honor code by typing “Yes”: YOUR ANSWER HERE_
  ]
)

#pagebreak()
= #text(fill: rmit-red)[3 -- Motivation]
#linebreak()
The T-Virus has broken out in the city of Metropolis. As the newly appointed Regional Health Director, you have been handed a dossier containing everything the epidemiologists know: a map of every known contact between residents, the probability that each contact transmits the virus in a single day, and the vulnerability of each resident. The clock is ticking — every day the virus spreads further, and your antiviral stockpile is limited.

Your job has four parts:
#enum(
  indent: 1.5em,
  spacing: 1.25em,
  tight: true,
  [*Build the contact network* (Task A) — represent the city’s contact relationships as a graph, efficiently enough to run algorithms on in real time (implement `graph/adjacency_matrix.py`).],
  [*Estimate infection risk* (Task B) — compute the probability that each resident becomes infected over the coming T days, identifying the most at-risk residents before the outbreak grows (implement `transmission/task_b.py` and write report).],
  [*Analyse your solution* (Task C) — theoretically and empirically compare your algorithm against the provided baseline across different network structures (write report on analysis of task A and B).],
  [*Allocate antiviral treatment* (Task D) — decide who receives the scarce supply of doses, maximising the benefit to the population within the limits of your stockpile (implement `treatment/task_b.py` and write report).]
)

Figure 1 shows the contact network for sub-population in Metropolis. Each resident is a node, and each contact relationship is an edge labelled with the daily probability of transmission. Patient zero $V_0$ is already infected — the question is how far the virus will spread, and who we should protect first.

#figure(
  image("images/Fig1_AA.svg"),
  caption: [
    The contact network $G = (V, E)$ for Metropolis. $V_0$ is patient zero. Edge labels give the daily transmission probability $w_(i j) ∈ (0, 1]$. Dashed red edges originate from an infected resident.
  ]
)

By vaccinating even a small number of strategically chosen residents, we can sever the most dangerous transmission pathways through the network. Figure 2 shows an example: vaccinating $V_1$ — the single resident through whom all transmission from $V_0$ must pass — protects every downstream resident at once.

#figure(
  image("images/Fig2_AA.svg"),
  caption: [
    Vaccinating $V_1$ — the single bottleneck through whom all transmission from $V_0$ must pass — severs every onward pathway at once, protecting $V_2$ through $V_6$ entirely. This illustrates the core challenge of Task D: identifying which residents to vaccinate in order to maximise protection across the network given a limited supply of doses.
  ]
)

= 3.1 -- Mathematical Background
#linebreak()
We model the city of Metropolis as a weighted undirected graph $G =(V,E)$, where:

#list(
  indent: 1.5em,
  spacing: 1.25em,
  tight: true,
  [each vertex $V_i in V$ represents a resident, with infection state $S_i in {0,1}$ where $S_i = 0$ is healthy and $S_i = 1$ is infected;],
  [each edge $(V_i, V_j ) in E$ represents a contact relationship between two residents; and],
  [each edge carries a weight $w_(i j) in (0, 1]$, the probability that an infected resident $V_i$ transmits the virus to a healthy neighbour $V_j$ in a single day.]
)

Each resident $V_i$ also has two personal attributes relevant to the vaccine allocation in Task D:

#list(
  indent: 1.5em,
  spacing: 1.25em,
  tight: true,
  [a *dosage requirement* $c_i ∈ Z^+$, the number of antiviral doses required to vaccinate resident $V_i$; and],
  [a *vulnerability score* $ϕ_i ∈ (0, 1]$, reflecting how severely resident $V_i$ would be harmed if infected.]
)

Once infected, a resident remains infectious forever. Over a planning horizon of $T$ days, the probability that an infected resident $V_i$ infects neighbour $V_j$ at least once is:

#align(center, $p_(i j) = 1 − (1 − w_(i j) )^T$)

As $T → infinity$, $p_(i j) → 1$ for any $w_(i j) > 0$ --- given enough time, every resident reachable from patient zero will eventually be infected. This makes early intervention critical. The benefit of vaccinating resident $V_i$ is therefore a function of how likely they are to be infected, how severely they would be harmed, and how much onward transmission they would cause — all of which are computed from $G$, $r_(i,T)$, and $ϕ_i$ in Tasks B and D.

#pagebreak()

= #text(fill: rmit-red)[Task B: Estimating Infection Risk Over Time (7 marks, 1 page)]

= Pseudo-code
#linebreak()
The Monte Carlo baseline (Algorithm 1) is provided as a style guide. Write your pseudo-code for the dynamic programming solution below in the same style.

/*
- This is a "format" for pseudocode I wrote myself as a temporary solution as the Algorithmic package was insufficient for our needs.
- Alternatively, the Lovelace format for the pseudocode is available (commented out below) for which there is a decent amount of documentation available online.
- In the near future, we (Nick and Ahmed) will be creating a package that will simplify this format and do it for you, without limitations of Algorithmic & Lovelace.
*/

#let index(n) = h(n * 1.5em)

#block(
  stroke: (top: 0.75pt, bottom: 0.75pt),
  inset: (top: 5pt, bottom: 5pt, left: 0pt, right: 0pt),
  width: 100%,
)[
  #block(
    stroke: (bottom: 0.75pt),
    inset: (bottom: 5pt),
    width: 100%,
  )[*Algorithm 1* MonteCarlo$(G, s, T, X)$]

  #v(-6pt)
  *Require:* Graph $G = (V, E)$; source $s$; horizon $T$; simulations $X$ \
  *Ensure:* Estimated risk table where $mono("table")[t][i] approx r_(i,t)$
  #v(-3pt)

  #set par(leading: 6pt)
  #let loop(w) = text(weight: "bold", w)

  1: #index(0) #loop[for] each day $t = 1$ #loop[to] $T$ #loop[do] \
  2: #index(1) #loop[for] each simulation $x = 1$ #loop[to] $X$ #loop[do] \
  3: #index(2) Restart from scratch — only $s$ is infected \
  4: #index(2) #loop[for] each day $d = 1$ #loop[to] $t$ #loop[do] \
  5: #index(3) #loop[for] each uninfected resident $V_i$ #loop[do] \
  6: #index(4) #loop[for] each infected neighbour $V_j$ of $V_i$ #loop[do] \
  7: #index(5) Infect $V_i$ with probability $w_(i j)$ \
  8: #index(1) $mono("table")[t][i] <- $ fraction of simulations where $V_i$ infected \
  9: #index(0) #loop[return] $mono("table")$
]

/*

#import "@preview/lovelace:0.3.0": *

#figure(
  kind: "algorithm",
  supplement: [Algorithm],
  pseudocode-list(
    booktabs: true,
    numbered-title: [MonteCarlo$(G, s, T, X)$],
  )[
    - *Require:* Graph $G = (V, E)$; source $s$; horizon $T$; simulations $X$
    - *Ensure:* Estimated risk table where $mono("table")[t][i] approx r_(i,t)$
    + *for* each day $t = 1$ *to* $T$ *do*
      + *for* each simulation $x = 1$ *to* $X$ *do*
        + Restart from scratch — only $s$ is infected
        + *for* each day $d = 1$ *to* $t$ *do*
          + *for* each uninfected resident $V_i$ *do*
            + *for* each infected neighbour $V_j$ of $V_i$ *do*
              + Infect $V_i$ with probability $w_(i j)$
    + $mono("table")[t][i] <- $ fraction of simulations where $V_i$ infected
    + *return* $mono("table")$
  ]
)

LOVELACE Pseudocode Sample ENDS HERE, use one or the other :)
*/

= Limitations of the Recurrence
#linebreak()
#enum(
  numbering: "(a)",
  indent: 1.5em,
  spacing: 1.25em,

  [_Your answer to part (a) here._],
  [_Your answer to part (b) here, with reference to Figure 3._
  #align(center)[
      #figure(
        image("images/Fig3_AA.svg"),
        caption: [This is Figure 3]
      )
    ]
  ],
  [_Your answer to part (c) here._],
)

#pagebreak()

= #text(fill: rmit-red)[Task C: Analysis of Infection Risk Algorithms (8 marks, 2 pages)]

= Algorithm Complexity Analysis
#linebreak()
_Your complexity analysis of all four combinations here._

= Empirical Design
#linebreak()
_Describe which variables vary, which you fix, and why._

= Empirical Analysis
#linebreak()
#figure(
  image("images/plot_example.png"),
  caption: [Runtime comparison of the four algorithm and representation combinations. _Replace this with your own plot and caption._]
)

= Reflection
#linebreak()
_Your reflection here, including a recommendation for Metropolis and a discussion of how your answer would change if transmission rates and connections updated daily._

#pagebreak()

= #text(fill: rmit-red)[Task D: Antiviral Allocation (10 marks, 2 pages)]

= Algorithm Design
#linebreak()
_Describe the algorithm you designed_

= Complexity Analysis
#linebreak()
_Justify the time complexity of your solution. Explain where each factor comes from._

= Extension 1: Triage
#linebreak()
_Describe how you would modify your solution to handle $K$ vulnerability tiers. State the complexity of your modified solution. Include a small numerical counterexample showing that ignoring vulnerability can lead to a highly vulnerable resident being passed over._

= Extension 2: Interdependent Vaccinations
#linebreak()
_Explain why the independence assumption $b_i = r_(i,T)$ is necessary for your solution to be valid. Construct a small example showing that ignoring interdependence leads to a sub-optimal outcome. Explain why the true optimal problem under interdependence is significantly harder to_ solve.
