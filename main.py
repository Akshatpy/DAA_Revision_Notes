from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, KeepTogether, PageBreak)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ── document ──────────────────────────────────────────────────────────────────
output_path = Path(__file__).with_name("algo_cheatsheet.pdf")

doc = SimpleDocTemplate(
    str(output_path),
    pagesize=A4,
    topMargin=1.2*cm, bottomMargin=1.2*cm,
    leftMargin=1.4*cm, rightMargin=1.4*cm,
)
W = A4[0] - 2.8*cm   # usable width

# ── colour palette ─────────────────────────────────────────────────────────
C_UNIT   = colors.HexColor("#1a1a2e")   # unit banner bg
C_SEC    = colors.HexColor("#16213e")   # section header bg
C_SUB    = colors.HexColor("#0f3460")   # sub-header bg
C_CODE   = colors.HexColor("#0d1117")   # code block bg
C_NOTE   = colors.HexColor("#ffd60a")   # highlight / note
C_WHITE  = colors.white
C_LGRAY  = colors.HexColor("#f0f4f8")
C_MGRAY  = colors.HexColor("#d0d8e4")
C_TEAL   = colors.HexColor("#00b4d8")
C_GREEN  = colors.HexColor("#06d6a0")
C_RED    = colors.HexColor("#ef233c")
C_ORANGE = colors.HexColor("#fb8500")

# ── styles ─────────────────────────────────────────────────────────────────
SS = getSampleStyleSheet()

def ps(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=SS[parent], **kw)

sNorm  = ps("norm",  fontSize=7.5, leading=10.5, spaceAfter=2)
sBold  = ps("bold",  fontSize=7.5, leading=10.5, fontName="Helvetica-Bold", spaceAfter=2)
sCode  = ps("code",  fontSize=6.5, leading=9.5, fontName="Courier",
            backColor=C_CODE, textColor=C_TEAL, leftIndent=6, rightIndent=6,
            spaceAfter=2, spaceBefore=2, borderPad=4)
sNote  = ps("note",  fontSize=7,   leading=10, fontName="Helvetica-Oblique",
            textColor=colors.HexColor("#555555"), spaceAfter=1)
sExamp = ps("examp", fontSize=7,   leading=10, fontName="Courier",
            backColor=colors.HexColor("#e8f4f8"), textColor=colors.HexColor("#003366"),
            leftIndent=4, rightIndent=4, spaceAfter=2, borderPad=3)
sBullet= ps("bullet",fontSize=7.5, leading=10.5, leftIndent=10, spaceAfter=1,
            bulletIndent=3)

# ── helper builders ────────────────────────────────────────────────────────
def unit_banner(txt):
    data = [[Paragraph(f'<font color="white"><b>{txt}</b></font>', ps("ub", fontSize=11, leading=14, fontName="Helvetica-Bold"))]]
    t = Table(data, colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), C_UNIT),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    return t

def sec(txt, color=C_SEC):
    data = [[Paragraph(f'<font color="white"><b>{txt}</b></font>', ps("sh", fontSize=8.5, leading=12, fontName="Helvetica-Bold"))]]
    t = Table(data, colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), color),
        ("TOPPADDING", (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING", (0,0),(-1,-1), 6),
    ]))
    return t

def subsec(txt):
    return sec(txt, C_SUB)

def code(*lines):
    txt = "<br/>".join(l.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                        .replace(" ","&nbsp;") for l in lines)
    return Paragraph(txt, sCode)

def note(txt): return Paragraph(f"<i>★ {txt}</i>", sNote)
def norm(txt): return Paragraph(txt, sNorm)
def bold(txt): return Paragraph(f"<b>{txt}</b>", sBold)
def examp(txt):
    txt2 = txt.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>").replace(" ","&nbsp;")
    return Paragraph(txt2, sExamp)
def bullet(txt): return Paragraph(f"• {txt}", sBullet)
def SP(h=4): return Spacer(1, h)
def HR(): return HRFlowable(width="100%", thickness=0.5, color=C_MGRAY, spaceAfter=3, spaceBefore=3)

def two_col(left_items, right_items):
    half = (W - 0.3*cm) / 2
    lp = []; rp = []
    for i in left_items:  lp.append([i])
    for i in right_items: rp.append([i])
    # render as side-by-side table
    rows = max(len(lp), len(rp))
    while len(lp) < rows: lp.append([Spacer(1,1)])
    while len(rp) < rows: rp.append([Spacer(1,1)])
    data = [[lp[i][0], rp[i][0]] for i in range(rows)]
    t = Table(data, colWidths=[half, half])
    t.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),0),
        ("RIGHTPADDING",(0,0),(-1,-1),3),
        ("TOPPADDING",(0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
    ]))
    return t

def info_table(headers, rows, col_widths=None):
    if col_widths is None:
        col_widths = [W/len(headers)]*len(headers)
    data = [[Paragraph(f"<b>{h}</b>", ps("th", fontSize=7, fontName="Helvetica-Bold",
                        textColor=C_WHITE)) for h in headers]] + \
           [[Paragraph(str(c), ps("td", fontSize=7, leading=9.5)) for c in r] for r in rows]
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0), C_SUB),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_LGRAY, C_WHITE]),
        ("GRID",(0,0),(-1,-1),0.3, C_MGRAY),
        ("TOPPADDING",(0,0),(-1,-1),3),
        ("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("LEFTPADDING",(0,0),(-1,-1),4),
    ]))
    return t

# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── TITLE ──────────────────────────────────────────────────────────────────
title_style = ps("title", fontSize=18, leading=22, fontName="Helvetica-Bold",
                  textColor=C_UNIT, alignment=TA_CENTER, spaceAfter=4)
story.append(Paragraph("Design and Analysis of Algorithms", title_style))
story.append(Paragraph("Complete Exam Cheat Sheet", ps("sub_title", fontSize=10,
              alignment=TA_CENTER, textColor=colors.HexColor("#555"), fontName="Helvetica-Oblique")))
story.append(HR())
story.append(SP(4))

# ══════════════════════════════════════════════════════════════════════════════
# UNIT 1
# ══════════════════════════════════════════════════════════════════════════════
story.append(unit_banner("UNIT 1 — Introduction, Analysis Framework & Brute Force"))
story.append(SP(4))

story.append(sec("Algorithm Properties & Problem Solving Steps"))
story.append(norm("<b>Algorithm Properties:</b> Input, Definiteness, Finiteness, Effectiveness, Output"))
story.append(norm("<b>Problem Solving Steps:</b> Understand problem → Decide computational means (DS+Algo) → Design algo → Prove correctness → Analyze algo → Code algo"))
story.append(SP(3))

story.append(sec("Algorithm Types"))
story.append(two_col(
    [norm("<b>Exact algorithms:</b> Always return a correct answer for every legitimate input in finite time."),
     norm("<b>Approximation algorithms:</b> Return a near-optimal answer with a bounded error."),
     SP(2),
     norm("<b>Analysis of algorithms:</b>"),
     bullet("Non-recursive: count basic operations / frequency of execution"),
     bullet("Recursive: write a recurrence and solve it"),
     bullet("Use asymptotic notation to ignore machine-dependent constants")],
    [norm("<b>Important problem types:</b> Sorting, searching, string matching, graph problems, combinatorial generation, optimization, and decision problems."),
     norm("<b>Design mindset:</b> Choose the paradigm that matches the structure of the problem: brute force, divide-and-conquer, greedy, DP, backtracking, or branch-and-bound.")]
))
story.append(SP(3))

story.append(sec("Algorithm Design Techniques (Overview)"))
story.append(two_col(
    [norm("• Brute Force"), norm("• Decrease &amp; Conquer"), norm("• Transform &amp; Conquer")],
    [norm("• Divide &amp; Conquer"), norm("• Dynamic Programming"), norm("• Greedy Technique")]
))
story.append(SP(3))

story.append(sec("Analysis Framework"))
story.append(two_col(
    [bold("Space Complexity:"),
     norm("S(P) = C (fixed) + Sp(I) (variable)"),
     SP(2),
     bold("Performance Measurement:"),
     norm("• Machine Dependent (Posterior)"),
     norm("• Experimental Study")],
    [bold("Time Complexity:"),
     norm("T(P) = C (compile) + Tp(I) (runtime)"),
     norm("T(n) = Cop × C(n) where C(n) = # basic op executions"),
     SP(2),
     bold("Performance Analysis:"),
     norm("• Machine Independent (Prior)"),
     norm("• Theoretical Analysis")]
))
story.append(SP(3))

story.append(sec("Asymptotic Notations"))
story.append(info_table(
    ["Notation","Name","Definition","Meaning"],
    [
        ["O(g(n))","Big-Oh","∃ c>0, n₀≥0: t(n) ≤ c·g(n) ∀n≥n₀","Upper bound (worst case)"],
        ["Ω(g(n))","Big-Omega","∃ c>0, n₀≥0: t(n) ≥ c·g(n) ∀n≥n₀","Lower bound (best case)"],
        ["Θ(g(n))","Theta","∃ c₁,c₂>0, n₀: c₁g(n)≤t(n)≤c₂g(n) ∀n≥n₀","Tight bound"],
        ["o(g(n))","Little-oh","lim t(n)/g(n)=0 as n→∞","Strictly less than"],
    ],
    [2.2*cm, 2.5*cm, 6.5*cm, 5*cm]
))
story.append(SP(2))
story.append(norm("<b>Efficiency Classes (slowest→fastest):</b> O(1) &lt; O(log n) &lt; O(n) &lt; O(n log n) &lt; O(n²) &lt; O(n³) &lt; O(2ⁿ) &lt; O(n!)"))
story.append(SP(3))

story.append(sec("Brute Force Algorithms"))

story.append(subsec("Exhaustive Search"))
story.append(two_col(
    [code("for each candidate solution x in the search space:",
        "  if x satisfies all constraints:",
        "    evaluate x",
        "return the best feasible x")],
    [norm("<b>Idea:</b> Enumerate every possible candidate and test it."),
     bullet("Often implemented by generating subsets, permutations, or combinations"),
     bullet("Used when the space is small or no better method is known"),
     norm("<b>Example:</b> Knapsack can be solved by checking all subsets." )]
))
story.append(SP(3))

story.append(subsec("Selection Sort — O(n²), In-place, NOT stable"))
story.append(two_col(
    [code("for i ← 0 to n-2 do",
          "  min ← i",
          "  for j ← i+1 to n-1 do",
          "    if A[j] < A[min]: min ← j",
          "  swap(A[i], A[min])")],
    [norm("<b>Idea:</b> Find minimum in unsorted portion, place at front."),
     norm("<b>Steps:</b> Pass i finds min of A[i..n-1], swaps to position i."),
     norm("<b>Comparisons:</b> n(n-1)/2 always. In-place but NOT stable.")]
))
story.append(SP(3))

story.append(subsec("Bubble Sort — O(n²), In-place, Stable"))
story.append(two_col(
    [code("for i ← 0 to n-2 do",
          "  for j ← 0 to n-2-i do",
          "    if A[j+1] < A[j]:",
          "      swap(A[j], A[j+1])")],
    [norm("<b>Idea:</b> Bubble largest element to end each pass."),
     norm("<b>Comparisons:</b> n(n-1)/2 always. Stable (swap only if strictly less).")]
))
story.append(SP(3))

story.append(subsec("Sequential Search — O(n)"))
story.append(code("i ← 0",
                   "while i < n and A[i] ≠ K do: i ← i+1",
                   "if i < n return i  else return -1"))
story.append(SP(3))

story.append(subsec("Brute Force String Matching — O(nm)"))
story.append(code("for i ← 0 to n-m do",
                   "  j ← 0",
                   "  while j < m and P[j] = T[i+j] do: j ← j+1",
                   "  if j = m return i   // match at position i",
                   "return -1"))
story.append(SP(3))

story.append(subsec("Matrix Multiplication — O(n³)"))
story.append(code("for i ← 0 to n-1 do",
                   "  for j ← 0 to n-1 do",
                   "    C[i][j] ← 0",
                   "    for k ← 0 to n-1 do",
                   "      C[i][j] ← C[i][j] + A[i][k] * B[k][j]"))
story.append(SP(3))

story.append(subsec("Tower of Hanoi — O(2ⁿ)"))
story.append(code("TOH(n, src, aux, dst):",
                   "  if n == 1: print 'Move disk 1 from src to dst'; return",
                   "  TOH(n-1, src, dst, aux)",
                   "  print 'Move disk n from src to dst'",
                   "  TOH(n-1, aux, src, dst)"))
story.append(note("Moves = 2ⁿ - 1"))
story.append(SP(3))

story.append(subsec("Euclid's GCD — O(log n)"))
story.append(code("while n ≠ 0 do",
                   "  r ← m mod n",
                   "  m ← n; n ← r",
                   "return m"))
story.append(SP(3))

story.append(subsec("Comparison Counting Sort — O(n²)"))
story.append(code("for i ← 0 to n-1: Count[i] ← 0",
                   "for i ← 0 to n-2:",
                   "  for j ← i+1 to n-1:",
                   "    if A[i] < A[j]: Count[j]++  else Count[i]++",
                   "for i ← 0 to n-1: S[Count[i]] ← A[i]"))
story.append(note("Count[i] = number of elements smaller than A[i] → gives direct position"))
story.append(SP(4))

# ══════════════════════════════════════════════════════════════════════════════
# UNIT 2
# ══════════════════════════════════════════════════════════════════════════════
story.append(unit_banner("UNIT 2 — Decrease-and-Conquer & Divide-and-Conquer"))
story.append(SP(4))

story.append(sec("Decrease-and-Conquer (3 Types)"))
story.append(info_table(
    ["Type","Examples","Strategy"],
    [
        ["Decrease by Constant (−1)","Insertion Sort, Topological Sort, Permutations","Solve for n-1, extend to n"],
        ["Decrease by Constant Factor (÷k)","Binary Search, Russian Peasant Mult, Josephus","Halve (or third) problem each step"],
        ["Variable Size Decrease","Euclid's GCD, Quickselect, Selection Problem","Reduction size varies per step"],
    ],
    [4.5*cm, 6*cm, 5.7*cm]
))
story.append(SP(3))

story.append(subsec("Insertion Sort — Θ(n²) worst/avg, Θ(n) best, Stable, In-place"))
story.append(two_col(
    [code("for i ← 1 to n-1 do",
          "  v ← A[i]; j ← i-1",
          "  while j ≥ 0 and A[j] > v do",
          "    A[j+1] ← A[j]; j ← j-1",
          "  A[j+1] ← v")],
    [norm("<b>Idea:</b> Insert A[i] into its correct position in the already-sorted A[0..i-1]."),
     norm("<b>Best case:</b> Already sorted → Θ(n) (no shifts needed)."),
     norm("<b>Stable:</b> Moves elements only when strictly greater, preserving equal elements order.")]
))
story.append(SP(3))

story.append(subsec("Topological Sort (Source Removal Method)"))
story.append(two_col(
    [code("L ← empty list",
          "S ← all vertices with no incoming edges",
          "while S is non-empty do:",
          "  remove vertex v from S",
          "  add v to tail of L",
          "  for each edge (v→m):",
          "    remove edge (v,m)",
          "    if m has no other incoming: add m to S",
          "if graph has edges: error (not a DAG)",
          "else return L")],
    [norm("<b>Steps:</b>"),
     bullet("Find all nodes with in-degree 0, add to set S"),
     bullet("Remove a node v from S, append to result L"),
     bullet("Remove all edges from v; update in-degrees"),
     bullet("If any node now has in-degree 0, add to S"),
     bullet("Repeat until S empty"),
     norm("<b>O(V+E)</b>. If edges remain at end → cycle (not a DAG)."),
     SP(2),
     norm("<b>Example:</b> A→B, A→C, B→D, C→D"),
     examp("In-degrees: A=0, B=1, C=1, D=2\nS={A} → L=[A] → remove A's edges\nS={B,C} → L=[A,B] → L=[A,B,C] → L=[A,B,C,D)")]
))
story.append(SP(3))

story.append(subsec("Generating Permutations"))
story.append(bold("Lexicographic Order (Johnson-Trotter):"))
story.append(code("Initialize with 1 2 ... n",
                   "while last permutation has two consecutive elements in increasing order:",
                   "  i = largest index such that a[i] < a[i+1]",
                   "  j = largest index such that a[i] < a[j]",
                   "  swap a[i] with a[j]",
                   "  reverse elements from a[i+1] to a[n]"))
story.append(SP(2))
story.append(bold("Johnson-Trotter (Mobile Element Method):"))
story.append(code("while last permutation has a mobile element:",
                   "  find largest mobile element k",
                   "  swap k with adjacent element k's arrow points to",
                   "  reverse direction of all elements larger than k",
                   "  add new permutation to list"))
story.append(note("Mobile = integer whose arrow points to an adjacent smaller integer. Generates all n! permutations."))
story.append(SP(3))

story.append(subsec("Binary Reflected Gray Code (BRGC) — for Subsets"))
story.append(two_col(
    [code("BRGC(n):",
          "  if n=1: return [0, 1]",
          "  L1 ← BRGC(n-1)",
          "  L2 ← reverse(L1)",
          "  prepend 0 to each string in L1",
          "  prepend 1 to each string in L2",
          "  return L1 + L2")],
    [norm("<b>Idea:</b> Consecutive codes differ by exactly 1 bit. Used to enumerate all subsets (Knapsack exhaustive search)."),
     norm("<b>Squashed Order:</b> Any subset involving aⱼ listed only after all subsets involving a₁..aⱼ₋₁."),
     norm("<b>n=2 example:</b> 00→01→11→10"),
     norm("<b>n=3 example:</b> 000→001→011→010→110→111→101→100")]
))
story.append(SP(3))

story.append(subsec("Binary Search (Decrease by Constant Factor) — O(log n)"))
story.append(code("BinarySearchRec(A[l..r], K):",
                   "  if l > r: return -1",
                   "  m ← ⌊(l+r)/2⌋",
                   "  if K = A[m]: return m",
                   "  else if K < A[m]: return BinarySearch(A[l..m-1], K)",
                   "  else: return BinarySearch(A[m+1..r], K)"))
story.append(note("Worst case: ⌈log₂(n+1)⌉ comparisons. Requires sorted array."))
story.append(SP(3))

story.append(subsec("Russian Peasant Multiplication"))
story.append(two_col(
    [bold("Recursive:"),
     code("multiply(n, m):",
          "  if n==1: return m",
          "  if n is odd:",
          "    return m + multiply((n-1)/2, 2*m)",
          "  else:",
          "    return multiply(n/2, 2*m)")],
    [bold("Iterative:"),
     code("multiply(n, m):",
          "  result ← 0",
          "  while n > 0:",
          "    if n is odd: result ← result + m",
          "    m ← 2*m; n ← n/2",
          "  return result"),
     norm("<b>Example:</b> 13×5: n=13(odd)+5, n=6+10, n=3(odd)+20→+20, n=1(odd)+40→+40"),
     norm("result = 5+20+40 = 65 ✓")]
))
story.append(SP(3))

story.append(subsec("Josephus Problem — O(log n)"))
story.append(two_col(
    [code("J(n):",
          "  if n==1: return 1",
          "  if n is odd:  return 2*J((n-1)/2) + 1",
          "  if n is even: return 2*J(n/2) - 1"),
     SP(2),
     norm("<b>Rule:</b> J(2k) = 2J(k)−1 (even), J(2k+1) = 2J(k)+1 (odd)")],
    [norm("<b>Shortcut:</b> If n = 2ᵐ + l (0≤l&lt;2ᵐ), then J(n) = 2l+1"),
     norm("<b>Trick:</b> J(n) = 1-bit cyclic left shift of n's binary representation!"),
     norm("<b>Example:</b> n=6 → binary 110 → shift left → 101 = 5, so J(6)=5"),
     norm("<b>Example:</b> n=5 → binary 101 → shift left → 011 = 3, so J(5)=3")]
))
story.append(SP(3))

story.append(subsec("Fake Coin Problem"))
story.append(two_col(
    [code("FakeCoin(coins):",
          "  divide coins into equal groups",
          "  weigh two groups on a balance",
          "  if equal: fake is in the unweighed group",
          "  else: fake is in the lighter/heavier weighed group",
          "  repeat until one coin remains")],
    [norm("<b>Idea:</b> Each weighing reduces the candidate set by a constant factor."),
     bullet("A balance scale gives 3 outcomes: left heavy, right heavy, or balance"),
     bullet("The fake coin is assumed lighter or heavier depending on the problem statement"),
     norm("<b>Example:</b> 9 coins → split into 3 groups of 3. One weighing identifies which group contains the fake; the next weighing narrows it to 1 coin.")]
))
story.append(SP(3))

story.append(subsec("Quickselect (Variable Size Decrease) — Avg O(n)"))
story.append(two_col(
    [code("Quickselect(A[l..r], k):",
          "  s ← LomutoPartition(A[l..r])",
          "  rank ← s - l + 1",
          "  if rank = k: return A[s]",
          "  else if k < rank:",
          "    return Quickselect(A[l..s-1], k)",
          "  else:",
          "    return Quickselect(A[s+1..r], k-rank)")],
    [bold("Lomuto Partition:"),
     code("p ← A[l]; s ← l",
          "for i ← l+1 to r:",
          "  if A[i] < p:",
          "    s ← s+1; swap(A[s], A[i])",
          "swap(A[l], A[s])",
          "return s"),
     norm("Lomuto: swaps every time smaller found. n-1 comparisons.")]
))
story.append(SP(4))

story.append(sec("Divide-and-Conquer"))
story.append(norm("<b>Master Theorem:</b> For T(n) = aT(n/b) + f(n) where f(n) = Θ(nᵈ):"))
story.append(SP(2))
story.append(info_table(
    ["Condition","Result","Example"],
    [
        ["d < log_b(a)  (a > bᵈ)","T(n) = Θ(n^(log_b a))","Strassen: a=7,b=2,d=2 → log₂7≈2.807 → Θ(n^2.807)"],
        ["d = log_b(a)  (a = bᵈ)","T(n) = Θ(nᵈ log n)","Merge Sort: a=2,b=2,d=1 → Θ(n log n)"],
        ["d > log_b(a)  (a < bᵈ)","T(n) = Θ(nᵈ)","Binary Search: a=1,b=2,d=0 → Θ(log n) [case 2]"],
    ],
    [4.5*cm, 5*cm, 6.7*cm]
))
story.append(SP(3))

story.append(subsec("Merge Sort — Θ(n log n) all cases, NOT in-place, Stable"))
story.append(two_col(
    [code("MergeSort(A[0..n-1]):",
          "  if n > 1:",
          "    copy A[0..⌊n/2⌋-1] to B",
          "    copy A[⌊n/2⌋..n-1] to C",
          "    MergeSort(B); MergeSort(C)",
          "    Merge(B, C, A)")],
    [code("Merge(B[0..p-1], C[0..q-1], A):",
          "  i←0; j←0; k←0",
          "  while i<p and j<q:",
          "    if B[i]≤C[j]: A[k]←B[i]; i++",
          "    else: A[k]←C[j]; j++",
          "    k++",
          "  copy remaining B or C into A")]
))
story.append(note("Stable because of ≤ in merge. Needs O(n) extra space. Best for linked lists."))
story.append(SP(3))

story.append(subsec("Quick Sort — Avg O(n log n), Worst O(n²), In-place, NOT stable"))
story.append(two_col(
    [code("QuickSort(A[l..r]):",
          "  if l < r:",
          "    s ← Partition(A[l..r])",
          "    QuickSort(A[l..s-1])",
          "    QuickSort(A[s+1..r])")],
    [bold("Hoare Partition (fewer swaps):"),
     code("p←A[l]; i←l; j←r+1",
          "repeat:",
          "  repeat i++ until A[i]≥p",
          "  repeat j-- until A[j]≤p",
          "  swap(A[i],A[j])",
          "until i≥j",
          "swap(A[i],A[j])  // undo last",
          "swap(A[l],A[j]); return j")]
))
story.append(note("On average, Quicksort makes only 39% more comparisons than best case. Use random pivot to avoid worst case."))
story.append(SP(3))

story.append(subsec("Strassen's Matrix Multiplication — O(n^2.807)"))
story.append(norm("<b>Key idea:</b> Reduce 8 multiplications to 7 multiplications + 18 add/subtractions."))
story.append(norm("M1=(A00+A11)(B00+B11), M2=(A10+A11)B00, M3=A00(B01-B11), M4=A11(B10-B00)"))
story.append(norm("M5=(A00+A01)B11, M6=(A10-A00)(B00+B01), M7=(A01-A11)(B10+B11)"))
story.append(norm("C00=M1+M4-M5+M7, C01=M3+M5, C10=M2+M4, C11=M1-M2+M3+M6"))
story.append(SP(3))

story.append(subsec("Karatsuba Large Integer Multiplication"))
story.append(norm("For two n-digit numbers: split a=a1·10^(n/2)+a0 and b=b1·10^(n/2)+b0"))
story.append(norm("C = C2·10ⁿ + C1·10^(n/2) + C0"))
story.append(info_table(["Term","Formula","Cost"],
    [["C2","a1 × b1","1 mult"],
     ["C0","a0 × b0","1 mult"],
     ["C1","(a1+a0)(b1+b0) − (C2+C0)","1 mult + additions"]],
    [3*cm, 5*cm, 5*cm]))
story.append(note("Only 3 multiplications instead of 4! Multiplications by 10ⁿ are bit shifts (free)."))
story.append(SP(3))

story.append(subsec("Binary Tree Height — O(n)"))
story.append(two_col(
    [code("Height(T):",
          "  if T = ∅: return -1",
          "  return max(Height(T.left),",
          "             Height(T.right)) + 1")],
    [norm("<b>Properties:</b>"),
     norm("• External nodes (leaves) x = n+1 (where n = internal nodes)"),
     norm("• Total nodes = 2n+1 (n internal + n+1 external)"),
     norm("• Height of one-node tree = 0")]
))
story.append(SP(4))

# ══════════════════════════════════════════════════════════════════════════════
# UNIT 3
# ══════════════════════════════════════════════════════════════════════════════
story.append(unit_banner("UNIT 3 — Transform-and-Conquer, Space-Time Tradeoffs & Greedy"))
story.append(SP(4))

story.append(sec("Transform-and-Conquer (3 Variants)"))
story.append(info_table(
    ["Type","Idea","Example"],
    [
        ["Instance Simplification","Transform input to a simpler/more structured instance","Pre-sorting, Gaussian elimination"],
        ["Representation Change","Change data structure/representation","Heaps, AVL trees, 2-3 Trees, B-Trees"],
        ["Problem Reduction","Transform to a different known problem","Reduction to sorting, matrix mult"],
    ],
    [4.5*cm, 6.5*cm, 5.2*cm]
))
story.append(SP(3))

story.append(subsec("Heapsort — O(n log n), In-place, NOT stable"))
story.append(two_col(
    [bold("Phase 1: Build Max-Heap (Bottom-Up):"),
     code("for i ← ⌊n/2⌋ downto 1:",
          "  k←i; v←H[k]; heap←false",
          "  while not heap and 2k≤n:",
          "    j←2k",
          "    if j<n and H[j]<H[j+1]: j←j+1",
          "    if v≥H[j]: heap←true",
          "    else: H[k]←H[j]; k←j",
          "  H[k]←v",
          "",
          "Phase 2: Sort:",
          "for i ← n downto 2:",
          "  swap(H[1], H[i])",
          "  Heapify(H[1..i-1])")],
    [norm("<b>Heap Properties:</b>"),
     norm("• Complete binary tree stored in array"),
     norm("• Parent at i, left child at 2i, right child at 2i+1"),
     norm("• Max-heap: H[parent] ≥ H[children]"),
     SP(2),
     norm("<b>Key Complexities:</b>"),
     norm("• Build heap: O(n) amortized"),
     norm("• Each delete/heapify: O(log n)"),
     norm("• Total: O(n log n)"),
     SP(2),
     norm("<b>Total comparisons per node at level i:</b> 2(h−i)"),
     SP(2),
     norm("<b>Property:</b> Nodes from a node to farthest leaf ≤ 2× nodes to nearest leaf")]
))
story.append(SP(3))

story.append(subsec("Distribution (Frequency) Counting Sort — O(n+u)"))
story.append(two_col(
    [code("// A[i] in range [l, u]",
          "for j←0 to u-l: D[j]←0",
          "for i←0 to n-1: D[A[i]-l]++",
          "for j←1 to u-l: D[j]←D[j-1]+D[j]  //cumulative",
          "for i←n-1 downto 0:",
          "  j←A[i]-l",
          "  S[D[j]-1]←A[i]",
          "  D[j]←D[j]-1",
          "return S")],
    [norm("<b>Steps:</b>"),
     bullet("Step 1: Count frequency of each value"),
     bullet("Step 2: Convert to cumulative counts (prefix sums)"),
     bullet("Step 3: Place elements into output (iterate in reverse for stability)"),
     SP(2),
     norm("<b>Example:</b> A=[3,1,2,1,3], l=1, u=3"),
     examp("D after freq: [2,1,2]\nD after cumul: [2,3,5]\nPlace: S[1]=1,S[2]=1,S[3]=2,S[4]=3,S[5]=3\nResult: [1,1,2,3,3]"),
     norm("<b>Stable</b> and runs in O(n+range). Best when range is small.")]
))
story.append(SP(3))

story.append(subsec("Horspool String Matching Algorithm"))
story.append(two_col(
    [bold("Step 1: Build Shift Table:"),
     code("for each char c in alphabet:",
          "  t[c] ← m          // default = pattern length",
          "for j ← 0 to m-2:",
          "  t[P[j]] ← m-1-j  // all chars except last"),
     SP(2),
     bold("Step 2: Search:"),
     code("Horspool(P[0..m-1], T[0..n-1]):",
          "  build shift table t",
          "  i ← m-1",
          "  while i ≤ n-1:",
          "    k←0",
          "    while k≤m-1 and P[m-1-k]=T[i-k]: k++",
          "    if k=m: return i-m+1  // match",
          "    else: i ← i + t[T[i]]",
          "  return -1")],
    [norm("<b>Key Insight:</b> Align pattern right end with T[i]. Compare right-to-left. On mismatch, shift by table value of T[i] (the character at current alignment's right end)."),
     SP(2),
     norm("<b>Example:</b> Pattern = BARBER (m=6)"),
     examp("Shift Table:\nB→2, A→4, R→1, E→3, others→6\n(Last B at j=4: shift=6-1-4=1... wait: j=0,B→5; j=1,A→4; j=2,R→3; j=3,B→2; j=4,E→1; j=5(last)=skip)\nDefault=6 for all, then:\nB:6-1-3=2, A:6-1-1=4, R:6-1-2=3, E:6-1-4=1"),
     SP(2),
     norm("<b>Avg case:</b> O(n/m). <b>Worst case:</b> O(nm)")]
))
story.append(SP(3))

story.append(subsec("Boyer-Moore Algorithm (Extension of Horspool)"))
story.append(norm("<b>Uses two shift tables</b> (takes max of both shifts):"))
story.append(info_table(
    ["Shift","Name","Formula","When to use"],
    [
        ["d1","Bad Character Shift","d1 = max(1, t(c)−k)   where t(c)=Horspool shift, k=matched chars","Mismatch char not in pattern or too far right"],
        ["d2","Good Suffix Shift","From second shift table based on matched suffix","When a proper suffix was matched before mismatch"],
    ],
    [1.5*cm, 4.5*cm, 5.5*cm, 4.7*cm]
))
story.append(note("Boyer-Moore shifts = max(d1, d2). Generally faster than Horspool on large alphabets."))
story.append(SP(3))

story.append(sec("Greedy Technique"))
story.append(norm("<b>Three Properties of Greedy Choice:</b> Feasible (satisfies constraints) + Locally Optimal + Irrevocable"))
story.append(SP(3))

story.append(subsec("Prim's Algorithm (MST) — O(V²) with adjacency matrix, O(E log V) with min-heap"))
story.append(two_col(
    [code("Prim(G):",
          "  Vt ← {v0}  // start with any vertex",
          "  Et ← {}",
          "  for i ← 1 to |V|-1:",
          "    find min weight edge e*=(v*,u*)",
          "      where v* ∈ Vt and u* ∉ Vt",
          "    Vt ← Vt ∪ {u*}",
          "    Et ← Et ∪ {e*}",
          "  return Et")],
    [norm("<b>Steps (Manual):</b>"),
     bullet("Start with any vertex, mark as visited"),
     bullet("At each step, find the minimum weight edge crossing the cut (visited ↔ unvisited)"),
     bullet("Add that edge and the new vertex to the MST"),
     bullet("Repeat until all vertices included"),
     SP(2),
     norm("<b>Example:</b> Graph with vertices A,B,C,D,E"),
     examp("Edges: A-B:2, A-C:3, B-D:4, C-D:1, D-E:5\nStart A: Vt={A}\nMin edge from A: A-B:2 → Vt={A,B}\nMin edge from {A,B}: A-C:3 → Vt={A,B,C}\nMin edge from {A,B,C}: C-D:1 → Vt={A,B,C,D}\nMin edge from {A,B,C,D}: D-E:5 → Done!\nMST edges: A-B,A-C,C-D,D-E  Weight=11")]
))
story.append(SP(3))

story.append(subsec("Kruskal's Algorithm (MST) — O(E log E)"))
story.append(two_col(
    [code("Kruskal(G):",
          "  Sort edges E by weight (non-decreasing)",
          "  for each vertex v: makeset(v)",
          "  MST ← {}",
          "  for each edge (u,v) in sorted order:",
          "    if find(u) ≠ find(v):  // diff components",
          "      MST.add((u,v))",
          "      union(u, v)",
          "  return MST")],
    [norm("<b>Steps (Manual):</b>"),
     bullet("Sort ALL edges by weight"),
     bullet("Process edges in order: add edge if it doesn't create a cycle (check via union-find)"),
     bullet("Stop when MST has V-1 edges"),
     SP(2),
     norm("<b>Same example:</b> Sort: C-D:1, A-B:2, A-C:3, B-D:4, D-E:5"),
     examp("C-D:1 → add (no cycle) {C},{D}→{C,D}\nA-B:2 → add {A},{B}→{A,B}\nA-C:3 → add {A,B}∪{C,D}→{A,B,C,D}\nB-D:4 → SKIP (find(B)=find(D)=same)\nD-E:5 → add → {A,B,C,D,E}\nMST: same as Prim ✓")]
))
story.append(SP(3))

story.append(subsec("Union-Find Data Structure"))
story.append(two_col(
    [bold("Array-Based:"),
     norm("id[v] = component ID of v"),
     norm("• makeset(v): id[v] ← v   O(1)"),
     norm("• find(v): return id[v]   O(1)"),
     norm("• union(u,v): change all id[u] to id[v]   O(n)"),
     SP(2),
     bold("Tree-Based (Union by Rank):"),
     norm("parent[v] = parent of v (root = its own parent)"),
     norm("• makeset(v): parent[v]←v, rank[v]←0  O(1)"),
     norm("• find(v): traverse to root   O(n) worst"),
     norm("• union(u,v): attach smaller rank tree under larger  O(1)"),
     note("With path compression: find ≈ O(α(n)) ≈ O(1) amortized")],
    [norm("<b>Example (Array-based):</b>"),
     examp("Vertices: 1,2,3,4,5,6\nmakeset: id=[1,2,3,4,5,6]\nunion(1,2): id=[2,2,3,4,5,6]\nunion(3,4): id=[2,2,4,4,5,6]\nunion(1,3): find(1)=2, find(3)=4\n  change all 2→4: id=[4,4,4,4,5,6]\nfind(2)=4, find(3)=4 → same component"),
     SP(2),
     norm("<b>Tree-based union(u,v):</b>"),
     examp("if rank[u] > rank[v]: parent[v]←u\nif rank[u] < rank[v]: parent[u]←v\nif equal: parent[v]←u; rank[u]++")]
))
story.append(SP(3))

story.append(subsec("Dijkstra's Shortest Path — O(V²) array, O(E log V) min-heap"))
story.append(two_col(
    [code("Dijkstra(G, source):",
          "  dist[source]←0; dist[v]←∞ for all other v",
          "  prev[v]←null for all v",
          "  S ← {} (visited set)",
          "  while S ≠ V:",
          "    u ← vertex not in S with min dist[u]",
          "    add u to S",
          "    for each neighbor v of u:",
          "      if dist[u]+w(u,v) < dist[v]:",
          "        dist[v] ← dist[u]+w(u,v)",
          "        prev[v] ← u",
          "  return dist[], prev[]")],
    [norm("<b>Steps (Manual):</b>"),
     bullet("Initialize: dist[src]=0, all others=∞"),
     bullet("Pick unvisited vertex with minimum distance"),
     bullet("Relax all its neighbors"),
     bullet("Mark as visited; repeat"),
     SP(2),
     norm("<b>Example:</b> A→B:4, A→C:2, B→D:3, C→B:1, C→D:5"),
     examp("Init: A=0, B=∞, C=∞, D=∞\nVisit A: B=4, C=2\nVisit C(min=2): B=min(4,2+1)=3, D=7\nVisit B(min=3): D=min(7,3+3)=6\nVisit D(min=6): done\nShortest: A→C→B→D = 6"),
     note("Does NOT work with negative edge weights! Use Bellman-Ford for those.")]
))
story.append(SP(3))

story.append(subsec("Huffman Trees (Greedy Encoding) — O(n log n)"))
story.append(two_col(
    [code("Huffman(C):  // C = set of chars with frequencies",
          "  n ← |C|",
          "  Q ← priority queue (min-heap) of C",
          "  for i ← 1 to n-1:",
          "    z ← new node",
          "    z.left ← x ← Extract-Min(Q)",
          "    z.right ← y ← Extract-Min(Q)",
          "    z.freq ← x.freq + y.freq",
          "    Insert(Q, z)",
          "  return Extract-Min(Q)  // root")],
    [norm("<b>Steps (Manual):</b>"),
     bullet("List all characters with frequencies"),
     bullet("Build min-heap (priority queue)"),
     bullet("Repeatedly extract 2 minimums, combine into parent node with sum frequency"),
     bullet("Insert new node back; repeat until 1 node left"),
     bullet("Left edge = 0, Right edge = 1"),
     SP(2),
     norm("<b>Example:</b> a:5, b:3, c:1, d:1"),
     examp("Step 1: combine c:1+d:1=cd:2\nQ: b:3, cd:2, a:5\nStep 2: combine cd:2+b:3=bcd:5\nQ: a:5, bcd:5\nStep 3: combine a:5+bcd:5=root:10\nCodes: a=0, b=10, c=110, d=111")]
))
story.append(SP(2))
story.append(info_table(
    ["Encoding Type","Description","Property"],
    [
        ["Fixed-Length","Same # bits per char (e.g. ASCII 8-bit)","Simple but wasteful for skewed frequencies"],
        ["Variable-Length","Freq chars get shorter codes","More efficient overall"],
        ["Prefix-Free","No code is prefix of another","Unambiguous decoding (Huffman is prefix-free)"],
    ],
    [4*cm, 6*cm, 6.2*cm]
))
story.append(note("Bits/char = Σ(code_length × frequency). Compression ratio = (h − avg_bits_per_char)/h × 100%"))
story.append(SP(3))

story.append(subsec("Red-Black Trees (Representation Change)"))
story.append(norm("<b>Properties:</b> (1) Every node is RED or BLACK. (2) Root is BLACK. (3) Every leaf (NIL) is BLACK. (4) Red node has BLACK children. (5) All paths from node to leaves have same # of BLACK nodes."))
story.append(norm("<b>Height:</b> At most 2 log(n+1). <b>Search:</b> O(log n). <b>Insert:</b> O(log n) — may need rotations + recoloring. <b>Delete:</b> O(log n)."))
story.append(SP(3))

story.append(subsec("2-3 Trees and B-Trees (Representation Change)"))
story.append(two_col(
    [bold("2-3 Tree:"),
     norm("• Every internal node has 2 or 3 children"),
     norm("• All leaves at same level (perfectly balanced)"),
     norm("• 2-node: 1 key, 2 children. 3-node: 2 keys, 3 children"),
     norm("• Search: O(log n), Insert: O(log n), Delete: O(log n)"),
     SP(2),
     bold("Insert steps:"),
     bullet("Search for correct leaf position"),
     bullet("If node has space (2-node): insert and done"),
     bullet("If node is full (3-node): split into two 2-nodes, push middle key up"),
     bullet("Propagate splits upward as needed")],
    [bold("B-Tree of order m:"),
     norm("• Generalization of 2-3 tree"),
     norm("• Each node has at most m children (m-1 keys)"),
     norm("• Each non-root node: ≥ ⌈m/2⌉ children"),
     norm("• Root: ≥ 2 children (unless it's a leaf)"),
     norm("• All leaves at same level"),
     norm("• Height: O(log_m n)"),
     SP(2),
     norm("<b>B-Tree order 3 = 2-3 Tree</b>"),
     norm("<b>Used in databases/filesystems</b> where disk access is expensive — minimize tree height")]
))
story.append(SP(4))

# ══════════════════════════════════════════════════════════════════════════════
# UNIT 4
# ══════════════════════════════════════════════════════════════════════════════
story.append(unit_banner("UNIT 4 — Dynamic Programming, Lower Bounds, NP & Backtracking"))
story.append(SP(4))

story.append(sec("Dynamic Programming"))
story.append(norm("<b>Key Idea:</b> Break into overlapping subproblems, solve each once, store results (memoization/tabulation). Optimal substructure must hold."))
story.append(SP(3))

story.append(subsec("Warshall's Algorithm (Transitive Closure) — O(n³)"))
story.append(two_col(
    [code("R ← adjacency matrix  // R(0)",
          "for k ← 1 to n:",
          "  for i ← 1 to n:",
          "    for j ← 1 to n:",
          "      R[i][j] = R[i][j] OR",
          "               (R[i][k] AND R[k][j])",
          "return R",
          "",
          "// R(k)[i][j] = 1 iff there is a path",
          "// from i to j using vertices {1..k}",
          "// as intermediates")],
    [norm("<b>Recurrence:</b> R<sup>k</sup>[i][j] = R<sup>k-1</sup>[i][j] OR (R<sup>k-1</sup>[i][k] AND R<sup>k-1</sup>[k][j])"),
     SP(2),
     norm("<b>Example:</b> 3 vertices: 1→2, 2→3"),
     examp("R(0):      R(1):      R(2):      R(3):\n0 1 0      0 1 0      0 1 1      0 1 1\n0 0 1  →   0 0 1  →   0 0 1  →   0 0 1\n0 0 0      0 0 0      0 0 0      0 0 0\nAfter k=2: R[1][3]=R[1][2]AND R[2][3]=1→path 1→2→3")]
))
story.append(SP(3))

story.append(subsec("Floyd's Algorithm (All-Pairs Shortest Paths) — O(n³)"))
story.append(two_col(
    [code("D ← weight matrix (∞ if no edge, 0 diagonal)",
          "for k ← 1 to n:",
          "  for i ← 1 to n:",
          "    for j ← 1 to n:",
          "      D[i][j] = min(D[i][j],",
          "                    D[i][k] + D[k][j])",
          "return D",
          "",
          "// Same structure as Warshall!",
          "// Replace OR with min, AND with +")],
    [norm("<b>Key Difference from Warshall:</b> Instead of reachability, finds actual shortest distances."),
     SP(2),
     norm("<b>Works with:</b> Negative weights ✓"),
     norm("<b>Fails with:</b> Negative cycles ✗ (Dijkstra also fails with negative weights)"),
     SP(2),
     norm("<b>Recurrence:</b> D<sup>k</sup>[i][j] = min(D<sup>k-1</sup>[i][j], D<sup>k-1</sup>[i][k] + D<sup>k-1</sup>[k][j])")]
))
story.append(SP(3))

story.append(subsec("0/1 Knapsack — O(nW) time and space"))
story.append(two_col(
    [code("// F[i][j] = max value with i items, capacity j",
          "// Base: F[0][j]=0 for all j",
          "Knapsack(weights, values, n, W):",
          "  for i ← 1 to n:",
          "    for j ← 0 to W:",
          "      if weights[i] > j:",
          "        F[i][j] ← F[i-1][j]",
          "      else:",
          "        F[i][j] ← max(F[i-1][j],",
          "          values[i]+F[i-1][j-weights[i]])",
          "  return F[n][W]")],
    [norm("<b>Recurrence:</b>"),
     norm("F[i][j] = F[i-1][j]  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if w[i] &gt; j"),
     norm("F[i][j] = max(F[i-1][j], v[i]+F[i-1][j-w[i]])  if w[i] ≤ j"),
     SP(2),
     norm("<b>Example:</b> Items: (w=2,v=12),(w=1,v=10),(w=3,v=20), W=5"),
     examp("     j=0  1   2   3   4   5\ni=0:  0   0   0   0   0   0\ni=1:  0   0  12  12  12  12\ni=2:  0  10  12  22  22  22\ni=3:  0  10  12  22  22  30"),
     norm("Answer = F[3][5] = 30 (items 2 and 3)")]
))
story.append(SP(3))

story.append(subsec("Memory Function Knapsack (MF Technique — Top Down DP)"))
story.append(code("// F table initialized to -1; F[0][j]=0, F[i][0]=0",
                   "MFKnapsack(i, j):",
                   "  if F[i][j] < 0:   // -1 means not computed yet",
                   "    if j < weights[i]:",
                   "      value ← MFKnapsack(i-1, j)",
                   "    else:",
                   "      value ← max(MFKnapsack(i-1, j),",
                   "               values[i] + MFKnapsack(i-1, j-weights[i]))",
                   "    F[i][j] ← value",
                   "  return F[i][j]"))
story.append(note("MF avoids computing subproblems not actually needed (unlike bottom-up). Called with MFKnapsack(n, W)."))
story.append(SP(3))

story.append(subsec("Binomial Coefficient — O(nk)"))
story.append(two_col(
    [code("// C(n,k) = n! / (k!(n-k)!)",
          "Binomial(n, k):",
          "  for i ← 0 to n:",
          "    for j ← 0 to min(i, k):",
          "      if j==0 or j==i: C[i][j]←1",
          "      else: C[i][j]←C[i-1][j]+C[i-1][j-1]",
          "  return C[n][k]")],
    [norm("<b>Pascal's Identity:</b> C(n,k) = C(n-1,k) + C(n-1,k-1)"),
     SP(2),
     norm("<b>MF Version:</b> Initialize table to 0 except known base cases. Check if C[n][k] already computed before recursing."),
     SP(2),
     examp("Pascal's triangle for C(4,2):\n  1\n 1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1  →  C(4,2)=6")]
))
story.append(SP(4))

story.append(sec("Lower Bound Arguments"))
story.append(info_table(
    ["Method","Idea","Result/Example"],
    [
        ["Trivial Lower Bound","Count items that must be processed","Searching unsorted: Ω(n) — must look at all"],
        ["Decision Trees","Binary tree of comparisons; height h ≥ ⌈log₂ l⌉ for l outcomes","Comparison sort: Ω(n log n); Binary search: Ω(log n)"],
        ["Adversary Arguments","Adversary constructs worst-case input adaptively","Proving Ω(n log n) for comparison-based sorting"],
        ["Problem Reduction","If Q reduces to P, then lb(Q) is also a lower bound for P","Matrix mult lower bound via transitive closure"],
    ],
    [4.5*cm, 5.5*cm, 6.2*cm]
))
story.append(SP(2))
story.append(norm("<b>Decision Tree for Sorting:</b> Must have ≥ n! leaves. Height h ≥ log₂(n!) ≈ n log₂ n (Stirling's formula). So comparison sort is Ω(n log n)."))
story.append(norm("<b>Decision Tree for Searching (binary):</b> h ≥ log₂(n+1). Worst case comparisons = ⌈log₂(n+1)⌉."))
story.append(norm("<b>Ternary search trees:</b> h ≥ ⌈log₃(2n+1)⌉"))
story.append(SP(3))

story.append(sec("P, NP, NP-Complete, NP-Hard"))
story.append(info_table(
    ["Class","Definition","Examples"],
    [
        ["P","Solvable in polynomial time (deterministic)","Sorting, Dijkstra, Matrix Mult"],
        ["NP","Verifiable in polynomial time (nondeterministic poly solvable)","Subset Sum, Hamilton Circuit, Knapsack (decision)"],
        ["NP-Complete","In NP AND every NP problem reduces to it in poly time","SAT (Cook's Theorem), 3-SAT, Vertex Cover, TSP (decision)"],
        ["NP-Hard","At least as hard as NP-Complete (may not be in NP)","TSP (optimization), Halting Problem"],
        ["co-NP","Complement of NP problems","Tautology check"],
    ],
    [2.5*cm, 6*cm, 7.7*cm]
))
story.append(SP(2))
story.append(two_col(
    [bold("Cook's Theorem (1971):"),
     norm("SAT (Boolean Satisfiability in CNF) is the first NP-Complete problem. Every NP problem can be reduced to SAT in polynomial time."),
     SP(2),
     norm("<b>If P=NP:</b> All NP problems solvable in poly time."),
     norm("<b>Most believe P≠NP</b> but unproven.")],
    [bold("NP Problems (Decision Versions):"),
     bullet("CNF Satisfiability (SAT)"),
     bullet("Partition Problem (2 equal-sum disjoint subsets)"),
     bullet("Hamilton Circuit Existence"),
     bullet("Decision TSP (is there a tour ≤ k?)"),
     bullet("Decision Knapsack (value ≥ V with weight ≤ W?)"),
     bullet("Vertex Cover, Clique, Independent Set")]
))
story.append(SP(2))
story.append(norm("<b>Reduction:</b> If NP problem Q reduces to problem P (Q ≤_p P), and Q is NP-Hard, then P is also NP-Hard."))
story.append(SP(3))

story.append(sec("Backtracking"))
story.append(two_col(
    [code("Backtrack(X[1..i]):",
          "  if X[1..i] is a solution:",
          "    output X[1..i]",
          "  else:",
          "    for each x in S(i+1) consistent",
          "       with X[1..i] and constraints:",
          "      X[i+1] ← x",
          "      Backtrack(X[1..i+1])")],
    [norm("<b>Key Concepts:</b>"),
     norm("• <b>State-space tree:</b> nodes = partial solutions, edges = choices"),
     norm("• <b>DFS traversal</b> of the state-space tree"),
     norm("• <b>Nonpromising nodes:</b> pruned when they cannot lead to valid solution"),
     norm("• <b>Promising:</b> node satisfies all constraints so far")]
))
story.append(SP(3))

story.append(subsec("N-Queens Problem (Backtracking)"))
story.append(two_col(
    [code("Place(k, i):  // can queen go in row k, col i?",
          "  for j ← 1 to k-1:",
          "    if (x[j]=i) or  // same column",
          "       (|x[j]-i|=|j-k|):  // same diagonal",
          "      return false",
          "  return true",
          "",
          "NQueens(k, n):",
          "  for i ← 1 to n:",
          "    if Place(k, i):",
          "      x[k] ← i",
          "      if k=n: print x[1..n]",
          "      else: NQueens(k+1, n)")],
    [norm("<b>Steps:</b>"),
     bullet("Place queens row by row (k = current row)"),
     bullet("Try each column i in current row"),
     bullet("Check: no queen in same column, no queen on same diagonal"),
     bullet("If safe, place queen and recurse to next row"),
     bullet("If no column works, backtrack"),
     SP(2),
     norm("<b>4-Queens example:</b>"),
     examp("Row 1: try col 1 → place\nRow 2: col 1 (same col), col 2 (diag), col 3 → place\nRow 3: all blocked → backtrack\nRow 2: col 4 → place\nRow 3: col 2 → place\nRow 4: col 4 (col), others blocked → backtrack...\nSolution: [2,4,1,3] (queen in row i at col x[i])")]
))
story.append(SP(3))

story.append(sec("Branch and Bound"))
story.append(two_col(
    [norm("<b>Key Idea:</b> Like backtracking but for optimization. Calculate a bound at each node; prune if bound can't beat current best solution."),
     SP(2),
     norm("<b>For Minimization:</b>"),
     bullet("Calculate lower bound at each partial solution"),
     bullet("If lower bound ≥ current best → prune"),
     SP(2),
     norm("<b>For Maximization:</b>"),
     bullet("Calculate upper bound at each partial solution"),
     bullet("If upper bound ≤ current best → prune"),
     SP(2),
     norm("<b>Priority Queue (Best-First Search):</b> Use min-heap of live nodes. Always expand the most promising node first.")],
    [norm("<b>Job Assignment Problem Example:</b>"),
     examp("Cost matrix (4 jobs, 4 workers):\n     J1  J2  J3  J4\nW1 [  9   2   7   8]\nW2 [  6   4   3   7]\nW3 [  5   8   1   8]\nW4 [  7   6   9   4]\n\nLower bound at root: take min of each row\n= min row1 + min row2 + min row3 + min row4\n= 2 + 3 + 1 + 4 = 10\n\nBranch: W1→J1: lb calculation using remaining\nW1→J2: lb=2+3+1+4=10 (promising)\n...\nPrune any node with lb ≥ current_best"),
     SP(2),
     note("BnB explores less than backtracking due to bounds, but worst case still exponential.")]
))
story.append(SP(4))

# ══════════════════════════════════════════════════════════════════════════════
# QUICK REFERENCE
# ══════════════════════════════════════════════════════════════════════════════
story.append(unit_banner("QUICK REFERENCE — Complexities & Comparisons"))
story.append(SP(4))

story.append(sec("Algorithm Complexity Summary"))
story.append(info_table(
    ["Algorithm","Best","Average","Worst","Space","Stable","In-place"],
    [
        ["Selection Sort","Θ(n²)","Θ(n²)","Θ(n²)","O(1)","✗","✓"],
        ["Bubble Sort","Θ(n²)","Θ(n²)","Θ(n²)","O(1)","✓","✓"],
        ["Insertion Sort","Θ(n)","Θ(n²)","Θ(n²)","O(1)","✓","✓"],
        ["Merge Sort","Θ(n log n)","Θ(n log n)","Θ(n log n)","O(n)","✓","✗"],
        ["Quick Sort","Θ(n log n)","Θ(n log n)","Θ(n²)","O(log n)","✗","✓"],
        ["Heap Sort","Θ(n log n)","Θ(n log n)","Θ(n log n)","O(1)","✗","✓"],
        ["Binary Search","O(1)","O(log n)","O(log n)","O(1)","—","—"],
        ["Warshall/Floyd","—","—","O(n³)","O(n²)","—","—"],
        ["Prim's MST","—","—","O(V²)","O(V)","—","—"],
        ["Kruskal's MST","—","—","O(E log E)","O(V)","—","—"],
        ["Dijkstra (array)","—","—","O(V²)","O(V)","—","—"],
        ["Dijkstra (heap)","—","—","O(E log V)","O(V)","—","—"],
        ["Huffman","—","—","O(n log n)","O(n)","—","—"],
        ["Knapsack DP","—","—","O(nW)","O(nW)","—","—"],
    ],
    [4*cm, 2.5*cm, 2.8*cm, 2.8*cm, 2*cm, 1.8*cm, 2*cm]
))
story.append(SP(3))

story.append(sec("Key Formulas & Facts"))
story.append(two_col(
    [bold("Stirling's Formula:"),
     norm("log₂(n!) ≈ n log₂ n"),
     SP(2),
     bold("Binary Tree:"),
     norm("• External nodes = internal nodes + 1 (x = n+1)"),
     norm("• Total nodes = 2n+1"),
     norm("• Height(empty) = -1, Height(one node) = 0"),
     SP(2),
     bold("Josephus:"),
     norm("• J(1) = 1"),
     norm("• J(2k) = 2J(k) - 1"),
     norm("• J(2k+1) = 2J(k) + 1"),
     norm("• = 1-bit cyclic left shift of n in binary"),
     SP(2),
     bold("Decision Trees:"),
     norm("• Sorting: h ≥ log₂(n!) ≈ n log n → Ω(n log n)"),
     norm("• Searching: h ≥ log₂(n+1)"),
     norm("• Ternary search: h ≥ ⌈log₃(2n+1)⌉")],
    [bold("Master Theorem T(n)=aT(n/b)+Θ(nᵈ):"),
     norm("• d &lt; log_b(a) → Θ(n^log_b(a))"),
     norm("• d = log_b(a) → Θ(nᵈ log n)"),
     norm("• d &gt; log_b(a) → Θ(nᵈ)"),
     SP(2),
     bold("Strassen: T(n) = 7T(n/2) + Θ(n²)"),
     norm("a=7, b=2, d=2. log₂7 ≈ 2.807 &gt; 2 → Θ(n^2.807)"),
     SP(2),
     bold("Huffman Compression:"),
     norm("• Bits/char = Σ(length × freq)"),
     norm("• Compression = (h - bits_per_char)/h × 100%"),
     SP(2),
     bold("Lomuto Partition:"),
     norm("• Uses n-1 comparisons for array of n"),
     norm("• Hoare has fewer swaps than Lomuto"),
     SP(2),
     bold("Quicksort Average:"),
     norm("Only 39% more comparisons than best case")]
))
story.append(SP(3))

story.append(sec("Decrease vs Divide: Key Distinction"))
story.append(info_table(
    ["Technique","Reduction","Example","Recurrence"],
    [
        ["Decrease by 1","n → n-1","Insertion Sort","T(n)=T(n-1)+Θ(n) → Θ(n²)"],
        ["Decrease by factor","n → n/2","Binary Search","T(n)=T(n/2)+O(1) → O(log n)"],
        ["Divide & Conquer","n → n/2 + n/2","Merge Sort","T(n)=2T(n/2)+Θ(n) → Θ(n log n)"],
        ["Variable Decrease","n → varies","Euclid's GCD","~O(log n)"],
    ],
    [4.5*cm, 4*cm, 4*cm, 3.7*cm]
))
story.append(SP(3))

story.append(sec("Greedy vs DP vs Backtracking"))
story.append(info_table(
    ["Paradigm","When to use","Gives Optimal?","Example"],
    [
        ["Greedy","Locally optimal = globally optimal (matroid)","Yes (for right problems)","MST, Huffman, Dijkstra (no neg weights)"],
        ["Dynamic Programming","Overlapping subproblems + optimal substructure","Yes (always optimal)","Knapsack, Floyd, Binomial Coefficient"],
        ["Backtracking","Constraint satisfaction, generate all solutions","Yes (finds all/optimal)","N-Queens, Subset Sum, TSP"],
        ["Branch & Bound","Optimization with pruning","Yes (exact optimal)","Job Assignment, TSP optimal"],
    ],
    [3.5*cm, 5.5*cm, 3.5*cm, 5.2*cm]
))
story.append(SP(4))

story.append(HRFlowable(width="100%", thickness=1, color=C_UNIT))
story.append(Paragraph("<i>Good luck on your exam! You've got this! 🎯</i>",
    ps("footer", fontSize=8, alignment=TA_CENTER, textColor=colors.HexColor("#888"), fontName="Helvetica-Oblique")))

# ── BUILD ──────────────────────────────────────────────────────────────────
doc.build(story)
print(f"Done! PDF created at {output_path}")