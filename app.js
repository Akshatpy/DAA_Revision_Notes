const units = [
  {
    id: 'unit1',
    title: 'Unit 1',
    subtitle: 'Introduction, analysis framework, brute force, and basic problem solving',
    topics: [
      {
        title: 'Algorithm Basics and Analysis',
        badge: 'Foundations',
        summary: 'An algorithm is a sequence of unambiguous instructions that takes input, produces output, and finishes in finite time.',
        steps: [
          'Core properties: Input, Definiteness, Finiteness, Effectiveness, Output.',
          'Design flow: understand problem -> choose data structures and algorithm -> prove correctness -> analyze -> code.',
          'Performance measurement is experimental and machine dependent.',
          'Performance analysis is theoretical and machine independent.'
        ],
        facts: [
          'Exact algorithms always give a correct result for legitimate input in finite time.',
          'Approximation algorithms stay within a predefined error limit.',
          'Time and space can be written as fixed cost + instance-dependent cost.'
        ]
      },
      {
        title: 'Asymptotic Notation and Efficiency Classes',
        badge: 'O, Omega, Theta, o',
        summary: 'Use asymptotic notation to compare growth rates while ignoring machine-specific constants.',
        code: `t(n) is in O(g(n)) if there exist c > 0 and n0 such that
for all n >= n0, t(n) <= c * g(n)

Similarly:
Omega(g(n)): lower bound
Theta(g(n)): tight bound
o(g(n)): strictly smaller growth`,
        steps: [
          'Big-O gives an upper bound.',
          'Big-Omega gives a lower bound.',
          'Theta gives both upper and lower bounds.',
          'Typical order: O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(n^3) < O(2^n) < O(n!).'
        ],
        example: 'Example: 3n^2 + 10n + 5 is O(n^2), Omega(n^2), and Theta(n^2).'
      },
      {
        title: 'Selection Sort',
        badge: 'Theta(n^2) | in-place | not stable',
        summary: 'Repeatedly select the minimum element from the unsorted suffix and place it at the front.',
        code: `for i <- 0 to n - 2 do
  min <- i
  for j <- i + 1 to n - 1 do
    if A[j] < A[min] then min <- j
  swap A[i], A[min]`,
        steps: [
          'Pass i finds the minimum in A[i..n-1].',
          'Swap it into position i.',
          'Repeat until the whole array is sorted.'
        ],
        example: 'Example: [64, 25, 12, 22, 11] -> pass 1 places 11 at index 0, pass 2 places 12, and so on.',
        facts: [
          'Comparisons are always n(n-1)/2.',
          'The algorithm is simple but inefficient for large inputs.'
        ]
      },
      {
        title: 'Bubble Sort',
        badge: 'Theta(n^2) | in-place | stable',
        summary: 'Adjacent out-of-order elements are swapped so the largest element bubbles to the end each pass.',
        code: `for i <- 0 to n - 2 do
  for j <- 0 to n - 2 - i do
    if A[j + 1] < A[j] then
      swap A[j], A[j + 1]`,
        steps: [
          'Compare adjacent pairs from left to right.',
          'Swap only when the right item is smaller.',
          'After each pass, the largest item is fixed at the end.'
        ],
        example: 'Stable because equal elements are not swapped unless the right one is strictly smaller.'
      },
      {
        title: 'Sequential Search',
        badge: 'Theta(n)',
        summary: 'Check elements one by one until the key is found or the list ends.',
        code: `i <- 0
while i < n and A[i] != K do
  i <- i + 1
if i < n then return i
else return -1`,
        steps: [
          'Start at index 0.',
          'Stop when A[i] equals the key.',
          'If the array ends first, report failure.'
        ],
        facts: [
          'Works on unsorted data.',
          'Best case is Theta(1) when the key is at the start.'
        ]
      },
      {
        title: 'Brute Force String Matching',
        badge: 'Theta(nm)',
        summary: 'Try every possible alignment of the pattern against the text.',
        code: `for i <- 0 to n - m do
  j <- 0
  while j < m and P[j] = T[i + j] do
    j <- j + 1
  if j = m then return i
return -1`,
        steps: [
          'Align the pattern at each position in the text.',
          'Compare from left to right.',
          'If a mismatch occurs, shift by one and continue.'
        ],
        example: 'Useful as a baseline before Horspool or Boyer-Moore.'
      },
      {
        title: 'Exhaustive Search',
        badge: 'Generate all candidates',
        summary: 'Enumerate every candidate solution and test feasibility or objective value.',
        code: `for each candidate x in the search space do
  if x satisfies all constraints then
    evaluate x
return best feasible x`,
        steps: [
          'Generate subsets, permutations, or combinations.',
          'Test each candidate against the constraints.',
          'Keep the best feasible solution.'
        ],
        example: 'Knapsack can be solved by checking every subset of items.',
        facts: [
          'Useful only when the search space is small or no better method is known.'
        ]
      },
      {
        title: 'Matrix Multiplication',
        badge: 'Theta(n^3)',
        summary: 'The straightforward triple-loop algorithm multiplies two square matrices.',
        code: `for i <- 0 to n - 1 do
  for j <- 0 to n - 1 do
    C[i][j] <- 0
    for k <- 0 to n - 1 do
      C[i][j] <- C[i][j] + A[i][k] * B[k][j]`,
        example: 'For 2x2 matrices, C[0][0] = A[0][0]B[0][0] + A[0][1]B[1][0].',
        facts: [
          'This is the classic brute force matrix multiplication.',
          'Strassen improves the asymptotic multiplication count.'
        ]
      },
      {
        title: 'Tower of Hanoi',
        badge: 'Theta(2^n)',
        summary: 'Move n disks using the auxiliary peg, one disk at a time.',
        code: `TOH(n, source, auxiliary, destination)
  if n = 1 then
    print move disk 1 from source to destination
    return
  TOH(n - 1, source, destination, auxiliary)
  print move disk n from source to destination
  TOH(n - 1, auxiliary, source, destination)`,
        example: 'For n=3, the move count is 7 and the recursive pattern is 2^(3) - 1.',
        steps: [
          'Move the top n-1 disks to the auxiliary peg.',
          'Move the largest disk to the destination.',
          'Move the n-1 disks from auxiliary to destination.'
        ],
        facts: ['Number of moves = 2^n - 1.']
      },
      {
        title: 'Euclid\'s GCD',
        badge: 'Theta(log n)',
        summary: 'Repeatedly replace the larger number by the remainder until the remainder becomes zero.',
        code: `while n != 0 do
  r <- m mod n
  m <- n
  n <- r
return m`,
        steps: [
          'Compute m mod n.',
          'Shift the pair (m, n) to (n, r).',
          'Continue until n becomes 0.'
        ],
        example: 'The final non-zero value is the gcd.'
      },
      {
        title: 'Comparison Counting Sort',
        badge: 'Theta(n^2)',
        summary: 'Count how many elements are smaller than each item to place it directly in the sorted array.',
        code: `for i <- 0 to n - 1 do
  Count[i] <- 0
for i <- 0 to n - 2 do
  for j <- i + 1 to n - 1 do
    if A[i] < A[j] then Count[j] <- Count[j] + 1
    else Count[i] <- Count[i] + 1
for i <- 0 to n - 1 do
  S[Count[i]] <- A[i]
return S`,
        example: 'For A=[4, 1, 3, 2], final Count values are [3,0,2,1], so S=[1,2,3,4].',
        facts: [
          'Count[i] equals the number of elements smaller than A[i].',
          'This is not the same as distribution counting sort.'
        ]
      }
    ]
  },
  {
    id: 'unit2',
    title: 'Unit 2',
    subtitle: 'Decrease-and-conquer, divide-and-conquer, recursion, and classic sorting',
    topics: [
      {
        title: 'Decrease-and-Conquer Overview',
        badge: '3 types',
        summary: 'Solve a problem by reducing it to a smaller instance, solving that, and then extending the answer.',
        steps: [
          'Decrease by a constant: insertion sort, topological sort, permutations.',
          'Decrease by a constant factor: binary search, Russian peasant multiplication, Josephus, fake coin.',
          'Decrease by a variable size: Euclid\'s gcd, quickselect, selection by partition.'
        ],
        facts: [
          'The recurrence often looks like T(n) = T(n - 1) + f(n) or T(n) = T(n / c) + f(n).'
        ]
      },
      {
        title: 'Insertion Sort',
        badge: 'Theta(n^2) worst | Theta(n) best',
        summary: 'Insert each element into the already sorted left prefix.',
        code: `for i <- 1 to n - 1 do
  v <- A[i]
  j <- i - 1
  while j >= 0 and A[j] > v do
    A[j + 1] <- A[j]
    j <- j - 1
  A[j + 1] <- v`,
        example: 'Example: inserting 12 into [11, 13, 15] gives [11, 12, 13, 15].',
        steps: [
          'Take the next element v.',
          'Shift larger sorted elements right.',
          'Insert v into its correct place.'
        ],
        facts: ['Stable and in-place.', 'Best case is Theta(n) when the array is already sorted.']
      },
      {
        title: 'Topological Sort',
        badge: 'O(V + E)',
        summary: 'In a DAG, repeatedly remove a source vertex and append it to the output list.',
        code: `L <- empty list
S <- set of vertices with no incoming edges
while S is not empty do
  remove a vertex v from S
  add v to tail of L
  for each edge (v, m) do
    remove edge (v, m)
    if m has no other incoming edges then
      insert m into S
if graph still has edges then
  report error
else return L`,
        steps: [
          'Start with all source vertices.',
          'Remove one source, add it to the result, and delete its outgoing edges.',
          'If a vertex becomes a source, add it to the set.'
        ],
        example: 'If edges remain at the end, the graph was not a DAG.'
      },
      {
        title: 'Generating Permutations and Gray Code',
        badge: 'Combinatorial objects',
        summary: 'Lexicographic order and Johnson-Trotter generate permutations; Gray code changes only one bit between neighbors.',
        code: `Lexicographic permutation idea:
1. Find the largest i with a[i] < a[i + 1]
2. Find the largest j with a[i] < a[j]
3. Swap a[i] and a[j]
4. Reverse the suffix from i + 1 to n

BRGC(n):
if n = 1 return [0, 1]
L1 <- BRGC(n - 1)
L2 <- reverse(L1)
prepend 0 to L1 and 1 to L2
return L1 + L2`,
  example: 'For n=3, BRGC outputs 000, 001, 011, 010, 110, 111, 101, 100.',
        steps: [
          'Lexicographic order produces the next permutation in dictionary order.',
          'Johnson-Trotter uses mobile elements and direction arrows.',
          'Gray code is useful for subset generation and exhaustive search.'
        ]
      },
      {
        title: 'Binary Search, Russian Peasant, Josephus, Fake Coin',
        badge: 'Decrease by factor',
        summary: 'These are classic examples where the instance shrinks by half or by a constant factor each step.',
        code: `Binary search:
if l > r return -1
m <- floor((l + r) / 2)
if K = A[m] return m
else if K < A[m] recurse left
else recurse right

Russian peasant:
if n is odd add m to result
halve n, double m, repeat

Josephus:
J(1) = 1
J(2k) = 2J(k) - 1
J(2k + 1) = 2J(k) + 1`,
  example: 'Example: binary search for 7 in [1,3,5,7,9] hits the middle element immediately; Russian peasant 13 x 5 gives 65.',
        steps: [
          'Binary search requires a sorted array.',
          'Russian peasant multiplication uses doubling and halving.',
          'Josephus can be solved with the binary left-shift trick.',
          'Fake coin uses balance-weighing to eliminate candidates by a factor of 3.'
        ],
        example: 'Fake coin example: split 9 coins into 3 groups of 3, weigh two groups, then repeat on the surviving group.'
      },
      {
        title: 'Quickselect and Lomuto Partition',
        badge: 'Average O(n)',
        summary: 'Quickselect finds the k-th smallest element using one partition and recursion on only one side.',
        code: `p <- A[l]
s <- l
for i <- l + 1 to r do
  if A[i] < p then
    s <- s + 1
    swap A[s], A[i]
swap A[l], A[s]
return s`,
  example: 'If pivot 5 partitions [8,3,5,7,2], the pivot ends at its rank and only one side is searched next.',
        steps: [
          'Partition around the pivot.',
          'Compute the pivot rank.',
          'Recurse only on the side containing the k-th item.'
        ],
        facts: ['The partition uses n - 1 comparisons for n elements.']
      },
      {
        title: 'Divide-and-Conquer Sum and Power',
        badge: 'Recursion pattern',
        summary: 'Split a problem into smaller independent subproblems and combine their results.',
        code: `Sum(A[0..n - 1]):
if n = 0 return 0
if n = 1 return A[0]
return Sum(left half) + Sum(right half)

Power(a, n):
if n = 0 return 1
if n = 1 return a
return Power(a, floor(n/2)) * Power(a, ceil(n/2))`,
  example: 'Power(2, 10) recursively combines 2^5 * 2^5 to get 1024.',
        facts: ['This is the divide-and-conquer style, not decrease-and-conquer.']
      },
      {
        title: 'Master Theorem',
        badge: 'T(n) = aT(n/b) + f(n)',
        summary: 'Use the dominant term among recursion, work at each level, and tree height.',
        steps: [
          'Compare f(n) with n^(log_b a).',
          'If f(n) is smaller, recursion dominates.',
          'If equal, multiply by log n.',
          'If larger, the combine cost dominates.'
        ],
        example: 'Merge sort: T(n)=2T(n/2)+Theta(n) => Theta(n log n).',
        facts: [
          'Case 1: f(n) = O(n^(log_b a - epsilon)).',
          'Case 2: f(n) = Theta(n^(log_b a) log^k n).',
          'Case 3: f(n) = Omega(n^(log_b a + epsilon)).'
        ]
      },
      {
        title: 'Merge Sort',
        badge: 'Theta(n log n) | stable | not in-place',
        summary: 'Split the array into halves, sort each half recursively, and merge the two sorted halves.',
        code: `MergeSort(A):
if n > 1 then
  split A into B and C
  MergeSort(B)
  MergeSort(C)
  Merge(B, C, A)

Merge(B, C, A):
i <- 0; j <- 0; k <- 0
while i < p and j < q do
  if B[i] <= C[j] then A[k] <- B[i]; i <- i + 1
  else A[k] <- C[j]; j <- j + 1
  k <- k + 1`,
        example: 'Merge [1,4,7] and [2,3,9] -> [1,2,3,4,7,9].',
        facts: ['Needs O(n) extra space.', 'Best choice when stability matters.']
      },
      {
        title: 'Quick Sort and Hoare Partition',
        badge: 'Average O(n log n) | worst O(n^2)',
        summary: 'Choose a pivot, partition the array, and recurse on the two sides.',
        code: `QuickSort(A[l..r]):
if l < r then
  s <- Partition(A[l..r])
  QuickSort(A[l..s - 1])
  QuickSort(A[s + 1..r])

Hoare partition:
p <- A[l]
i <- l
j <- r + 1
repeat
  repeat i <- i + 1 until A[i] >= p
  repeat j <- j - 1 until A[j] <= p
  swap A[i], A[j]
until i >= j`,
        example: 'Example: pivot 4 splits [8,3,1,7,0,10,2] into two recursive sides after partitioning.',
        facts: ['Hoare partition usually uses fewer swaps than Lomuto.']
      },
      {
        title: 'Binary Tree Traversals and Height',
        badge: 'Tree basics',
        summary: 'Traversal order and height computation are common recursive examples.',
        code: `Preorder: root, left, right
Inorder: left, root, right
Postorder: left, right, root

Height(T):
if T = empty return -1
return max(Height(T.left), Height(T.right)) + 1`,
  example: 'For root A with left child B and right child C: preorder A B C, inorder B A C, postorder B C A.',
        steps: [
          'Preorder visits the root first.',
          'Inorder is useful for binary search trees.',
          'Postorder visits the root last.'
        ],
        facts: ['For a tree with n internal nodes, external nodes = n + 1 and total nodes = 2n + 1.']
      },
      {
        title: 'Strassen and Karatsuba',
        badge: 'Fast multiplication',
        summary: 'Strassen reduces matrix multiplication from 8 sub-multiplications to 7; Karatsuba reduces integer multiplication from 4 to 3.',
        code: `Strassen: 7 multiplications + 18 additions/subtractions
T(n) = 7T(n/2) + Theta(n^2)
=> Theta(n^2.807)

Karatsuba:
C2 = a1 * b1
C0 = a0 * b0
C1 = (a1 + a0)(b1 + b0) - (C2 + C0)`,
  example: 'Karatsuba example: 12 x 34 -> split into 1|2 and 3|4, then use 3 products instead of 4.',
        facts: ['Strassen is asymptotically faster than the naive cubic algorithm.', 'Karatsuba uses 3 multiplications instead of 4.']
      }
    ]
  },
  {
    id: 'unit3',
    title: 'Unit 3',
    subtitle: 'Transform-and-conquer, space-time tradeoffs, and greedy algorithms',
    topics: [
      {
        title: 'Transform-and-Conquer Overview',
        badge: 'Instance simplification',
        summary: 'Change the instance, change the representation, or reduce the problem to another one.',
        steps: [
          'Instance simplification: pre-processing or pre-sorting.',
          'Representation change: heaps, balanced trees, B-trees.',
          'Problem reduction: map the task to a known problem.'
        ]
      },
      {
        title: 'Counting Sort',
        badge: 'O(n + range)',
        summary: 'Count how many times each value occurs, then rebuild the sorted output using prefix sums.',
        code: `for j <- 0 to u - l do
  D[j] <- 0
for i <- 0 to n - 1 do
  D[A[i] - l] <- D[A[i] - l] + 1
for j <- 1 to u - l do
  D[j] <- D[j - 1] + D[j]
for i <- n - 1 downto 0 do
  j <- A[i] - l
  S[D[j] - 1] <- A[i]
  D[j] <- D[j] - 1
return S`,
        steps: [
          'Build the frequency array.',
          'Convert it to a cumulative count array.',
          'Place elements into the output from right to left for stability.'
        ],
        example: 'Example: A = [3, 1, 2, 1, 3] with values in [1, 3].',
        facts: ['This is the distribution counting version, not comparison counting.']
      },
      {
        title: 'Heap Sort',
        badge: 'Theta(n log n) | in-place',
        summary: 'First build a max-heap, then repeatedly remove the maximum and heapify the remainder.',
        code: `HeapSort(H[1..n]):
HeapBottomUp(H[1..n])
for i <- n downto 2 do
  swap H[1], H[i]
  Heapify(H[1..i - 1])`,
        example: 'Example: if the max-heap root is 9, swapping it with the last element fixes 9 at the end of the array.',
        steps: [
          'Build the max-heap bottom-up in Theta(n).',
          'Swap the root with the last item.',
          'Heapify the reduced heap after each deletion.'
        ],
        facts: ['Heap sort is not stable.']
      },
      {
        title: 'Red-Black Trees',
        badge: 'Balanced BST',
        summary: 'A red-black tree keeps the search tree height logarithmic using color rules and rotations.',
        steps: [
          'Every node is red or black.',
          'The root is black.',
          'Red nodes cannot have red children.',
          'Every path from a node to NIL leaves has the same number of black nodes.'
        ],
        example: 'Example insert sequence: 10, 20, 30 triggers a rotation and recoloring so the tree stays balanced.',
        facts: [
          'Search, insert, and delete are all O(log n).',
          'Insert and delete may require rotations and recoloring.'
        ]
      },
      {
        title: '2-3 Trees and B-Trees',
        badge: 'Balanced multiway trees',
        summary: 'A 2-3 tree is a balanced search tree where every internal node has 2 or 3 children; a B-tree generalizes this idea.',
        steps: [
          'Search reaches all leaves at the same level.',
          'Insert may split full nodes and push a middle key upward.',
          'Delete may borrow or merge nodes to preserve balance.'
        ],
        example: 'Example: inserting a key into a full 3-node splits it into two 2-nodes and moves the middle key up.',
        facts: [
          'Search, insert, and delete are logarithmic.',
          'B-trees are used when disk access cost matters.'
        ]
      },
      {
        title: 'Horspool and Boyer-Moore',
        badge: 'String matching acceleration',
        summary: 'Horspool uses a bad-shift table; Boyer-Moore uses bad-character and good-suffix shifts.',
        code: `Horspool search:
build shift table t
i <- m - 1
while i <= n - 1 do
  k <- 0
  while k < m - 1 and P[m - 1 - k] = T[i - k] do
    k <- k + 1
  if k = m then return i - m + 1
  else i <- i + t[T[i]]`,
        example: 'Example: pattern BARBER gives shifts B->2, A->4, R->3, E->1, others->6. A mismatch at the right end uses the current text character to shift.',
        steps: [
          'Align the pattern with its right end at T[i].',
          'Compare characters from right to left.',
          'On mismatch, shift using the table for the current text character.'
        ],
        facts: ['Boyer-Moore usually shifts by max(bad-character, good-suffix).']
      },
      {
        title: 'Greedy Technique, Prim, Kruskal, and Union-Find',
        badge: 'MST and sets',
        summary: 'Greedy algorithms build a solution by repeatedly choosing a locally optimal, feasible, and irrevocable choice.',
        code: `Prim:
Vt <- {start vertex}
Et <- empty set
repeat V - 1 times:
  choose the minimum weight edge crossing (Vt, V - Vt)
  add the new vertex and edge to the tree

Kruskal:
sort edges by weight
make set for each vertex
for each edge (u, v) in order:
  if find(u) != find(v) then
    add edge to MST
    union(u, v)`,
        example: 'Example graph: choose the smallest edge, skip any edge that closes a cycle, and stop after V - 1 edges are chosen.',
        steps: [
          'Prim grows one connected tree from a chosen start vertex.',
          'Kruskal processes edges globally in sorted order.',
          'Union-find checks whether adding an edge creates a cycle.'
        ],
        facts: [
          'Array-based union-find: find O(1), union O(n).',
          'Tree-based union-find: find O(n), union O(1).',
          'With path compression and rank, operations are almost constant amortized.'
        ],
        example: 'Example MST steps: sort edges, add the smallest edge that does not create a cycle, stop when you have V - 1 edges.'
      },
      {
        title: 'Dijkstra and Huffman Trees',
        badge: 'Greedy shortest path and encoding',
        summary: 'Dijkstra finds shortest paths with non-negative weights; Huffman builds an optimal prefix-free code tree.',
        code: `Dijkstra:
dist[src] <- 0
all others <- infinity
while some vertices remain unvisited do
  choose unvisited vertex with minimum dist
  relax all outgoing edges

Huffman:
place characters in a min-heap by frequency
repeat extract two smallest nodes
create a parent with summed frequency
insert parent back into the heap`,
  example: 'Dijkstra example: from source A, if A->C is 2 and C->B is 1, then the current best path to B becomes 3 via C. Huffman example: merge the two least frequent symbols first.',
        steps: [
          'Dijkstra repeatedly picks the vertex with the smallest tentative distance.',
          'Huffman repeatedly combines the two least frequent symbols.',
          'In Huffman trees, left edge = 0 and right edge = 1.'
        ],
        facts: [
          'Dijkstra does not work with negative edge weights.',
          'Huffman gives variable-length, prefix-free codes.'
        ]
      }
    ]
  },
  {
    id: 'unit4',
    title: 'Unit 4',
    subtitle: 'Dynamic programming, lower bounds, NP classes, backtracking, and branch and bound',
    topics: [
      {
        title: 'Dynamic Programming Overview',
        badge: 'Overlap + optimal substructure',
        summary: 'Solve each subproblem once and store the result, either top-down with memoization or bottom-up with tabulation.',
        steps: [
          'Break the problem into overlapping subproblems.',
          'Write the recurrence.',
          'Store solved values in a table or cache.',
          'Reconstruct the answer if needed.'
        ]
      },
      {
        title: 'Binomial Coefficient',
        badge: 'Theta(nk)',
        summary: 'Use Pascal\'s identity to fill a table for C(n, k).',
        code: `for i <- 0 to n do
  for j <- 0 to min(i, k) do
    if j = 0 or j = i then
      C[i][j] <- 1
    else
      C[i][j] <- C[i - 1][j] + C[i - 1][j - 1]
return C[n][k]`,
        example: 'Example: C(4,2) = 6 from the row 1,4,6,4,1.',
        facts: ['Pascal identity: C(n, k) = C(n - 1, k) + C(n - 1, k - 1).']
      },
      {
        title: '0/1 Knapsack and Memory Function Technique',
        badge: 'Theta(nW)',
        summary: 'Decide whether to take an item or leave it, using a DP table or memoized recursion.',
        code: `F[i][j] = max value using first i items and capacity j

if weights[i] > j then
  F[i][j] <- F[i - 1][j]
else
  F[i][j] <- max(F[i - 1][j], values[i] + F[i - 1][j - weights[i]])

MFKnapsack(i, j):
if F[i][j] is not computed then
  compute it recursively
return F[i][j]`,
        steps: [
          'If the current item is too heavy, skip it.',
          'Otherwise compare take vs leave.',
          'Memoization stores only the needed states.'
        ],
        example: 'Example: weights [2, 1, 3], values [12, 10, 20], capacity 5 -> best value 30 by taking items 2 and 3.'
      },
      {
        title: 'Warshall and Floyd',
        badge: 'Theta(n^3)',
        summary: 'Warshall computes transitive closure; Floyd computes all-pairs shortest paths.',
        code: `Warshall:
R <- adjacency matrix
for k <- 1 to n do
  for i <- 1 to n do
    for j <- 1 to n do
      R[i][j] <- R[i][j] OR (R[i][k] AND R[k][j])

Floyd:
D <- weight matrix
for k <- 1 to n do
  for i <- 1 to n do
    for j <- 1 to n do
      D[i][j] <- min(D[i][j], D[i][k] + D[k][j])`,
        example: 'Warshall example: if 1->2 and 2->3 exist, then after the k=2 iteration the matrix marks 1->3 reachable. Floyd example: if 1->2=3 and 2->3=4, then 1->3 becomes 7 if that is smaller than the direct edge.',
        facts: ['Floyd works with negative edges but not with negative cycles.']
      },
      {
        title: 'Lower Bounds and Decision Trees',
        badge: 'Limits of computation',
        summary: 'Lower bounds estimate the minimum amount of work needed to solve a problem.',
        steps: [
          'Trivial lower bounds count the items that must be processed.',
          'Decision trees model comparisons and branching outcomes.',
          'Adversary arguments construct the worst-case input adaptively.',
          'Reductions transfer lower bounds from one problem to another.'
        ],
        example: 'Example: any comparison sort on n items needs at least log2(n!) comparisons in the worst case.',
        facts: [
          'Comparison sorting needs Omega(n log n) comparisons.',
          'Binary search needs about log2(n + 1) comparisons in the worst case.'
        ]
      },
      {
        title: 'P, NP, NP-Complete, and NP-Hard',
        badge: 'Complexity classes',
        summary: 'P is polynomial-time solvable, NP is polynomial-time verifiable, NP-complete is both NP and NP-hard, and NP-hard is at least as hard as NP-complete.',
        steps: [
          'SAT is the first NP-complete problem (Cook\'s theorem).',
          'If one NP-complete problem is solved in polynomial time, then every NP problem is.',
          'Typical decision problems: SAT, partition, Hamiltonian cycle, decision TSP, decision knapsack.'
        ],
        example: 'Example: SAT asks whether a CNF formula can be made true by some assignment. The partition decision problem asks whether a set can be split into two equal-sum subsets.',
        facts: [
          'NP-complete problems are the hardest problems inside NP.',
          'Optimization TSP is NP-hard.'
        ]
      },
      {
        title: 'Backtracking, N-Queens, and Branch and Bound',
        badge: 'DFS over state space',
        summary: 'Backtracking explores a state-space tree using depth-first search and prunes non-promising nodes; branch and bound adds bounds for optimization.',
        code: `Backtrack(X[1..i]):
if X[1..i] is a solution then
  output X[1..i]
else
  for each x in S(i + 1) consistent with X[1..i] do
    X[i + 1] <- x
    Backtrack(X[1..i + 1])

NQueens:
Place one queen per row.
Check same column and same diagonal before recursing.`,
        steps: [
          'A promising node can still lead to a valid solution.',
          'A non-promising node is pruned immediately.',
          'Branch and bound keeps the best current solution and prunes any node whose bound cannot beat it.'
        ],
        example: 'In the 4-Queens problem, a sample solution is [2, 4, 1, 3].'
      }
    ]
  }
];

const quickRef = [
  {
    title: 'Complexity Snapshot',
    columns: ['Algorithm', 'Best', 'Average', 'Worst', 'Space', 'Stable', 'In-place'],
    rows: [
      ['Selection Sort', 'Θ(n^2)', 'Θ(n^2)', 'Θ(n^2)', 'O(1)', 'No', 'Yes'],
      ['Insertion Sort', 'Θ(n)', 'Θ(n^2)', 'Θ(n^2)', 'O(1)', 'Yes', 'Yes'],
      ['Merge Sort', 'Θ(n log n)', 'Θ(n log n)', 'Θ(n log n)', 'O(n)', 'Yes', 'No'],
      ['Quick Sort', 'Θ(n log n)', 'Θ(n log n)', 'Θ(n^2)', 'O(log n)', 'No', 'Yes'],
      ['Heap Sort', 'Θ(n log n)', 'Θ(n log n)', 'Θ(n log n)', 'O(1)', 'No', 'Yes'],
      ['Dijkstra (array)', '-', '-', 'O(V^2)', 'O(V)', '-', '-'],
      ['Dijkstra (heap)', '-', '-', 'O(E log V)', 'O(V)', '-', '-'],
      ['Prim', '-', '-', 'O(V^2)', 'O(V)', '-', '-'],
      ['Kruskal', '-', '-', 'O(E log E)', 'O(V)', '-', '-'],
      ['Huffman', '-', '-', 'O(n log n)', 'O(n)', '-', '-']
    ]
  },
  {
    title: 'Must Remember Formulas',
    columns: ['Topic', 'Formula'],
    rows: [
      ['Master theorem', 'T(n) = aT(n/b) + f(n)'],
      ['Binary tree nodes', 'external = internal + 1'],
      ['Binary tree total nodes', '2n + 1'],
      ['Comparison sort lower bound', 'Omega(n log n)'],
      ['Binary search worst case', 'ceil(log2(n + 1))'],
      ['Strassen', '7T(n/2) + Theta(n^2) => Theta(n^2.807)'],
      ['Huffman', 'left edge = 0, right edge = 1']
    ]
  },
  {
    title: 'Recurrence Relations',
    columns: ['Algorithm', 'Recurrence', 'Base / Notes', 'Result'],
    rows: [
      ['Tower of Hanoi', 'M(n) = 2M(n-1) + 1', 'M(1) = 1', 'M(n) = 2^n - 1'],
      ['Selection Sort', 'T(n) = T(n-1) + Theta(n)', 'T(1) = Theta(1)', 'Theta(n^2)'],
      ['Bubble Sort', 'T(n) = T(n-1) + Theta(n)', 'T(1) = Theta(1)', 'Theta(n^2)'],
      ['Insertion Sort', 'T(n) = T(n-1) + Theta(n)', 'T(1) = Theta(1)', 'Theta(n^2)'],
      ['Binary Search', 'T(n) = T(n/2) + Theta(1)', 'T(1) = Theta(1)', 'Theta(log n)'],
      ['Merge Sort', 'T(n) = 2T(n/2) + Theta(n)', 'T(1) = Theta(1)', 'Theta(n log n)'],
      ['Quick Sort', 'T(n) = T(k) + T(n-k-1) + Theta(n)', 'Worst case: T(n) = T(n-1) + Theta(n)', 'Avg Theta(n log n), worst Theta(n^2)'],
      ['Heap Sort', 'T(n) = T(n-1) + Theta(log n)', 'Build-heap is Theta(n)', 'Theta(n log n)'],
      ['Strassen', 'T(n) = 7T(n/2) + Theta(n^2)', 'T(1) = Theta(1)', 'Theta(n^2.807)'],
      ['Karatsuba', 'T(n) = 3T(n/2) + Theta(n)', 'T(1) = Theta(1)', 'Theta(n^log2 3)']
    ]
  }
];

const state = {
  unit: 'all',
  query: ''
};

const content = document.getElementById('content');
const toc = document.getElementById('toc');
const unitFilters = document.getElementById('unitFilters');
const search = document.getElementById('search');
const stats = document.getElementById('stats');
const quickRefMount = document.getElementById('quickRef');
const expandAllBtn = document.getElementById('expandAll');
const collapseAllBtn = document.getElementById('collapseAll');
const clearFilterBtn = document.getElementById('clearFilter');

function escapeHTML(text) {
  return text
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function normalise(text) {
  return text.toLowerCase().replace(/\s+/g, ' ').trim();
}

function toSearchText(topic, unit) {
  const parts = [
    unit.title,
    unit.subtitle,
    topic.title,
    topic.badge || '',
    topic.summary || '',
    (topic.steps || []).join(' '),
    topic.code || '',
    topic.example || '',
    (topic.facts || []).join(' ')
  ];

  return normalise(parts.join(' '));
}

function buildSummary(topic) {
  const title = document.createElement('div');
  title.className = 'topic-title';

  const strong = document.createElement('strong');
  strong.textContent = topic.title;
  title.appendChild(strong);

  const sub = document.createElement('span');
  sub.textContent = topic.summary || '';
  title.appendChild(sub);

  const badge = document.createElement('span');
  badge.className = 'badge';
  badge.textContent = topic.badge || 'Topic';

  return { title, badge };
}

function createList(items, className = 'step-list') {
  let list = document.createElement('ol');
  if (className !== 'step-list') {
    list = document.createElement('ul');
  }
  list.className = className;
  items.forEach((item) => {
    const li = document.createElement('li');
    li.textContent = item;
    list.appendChild(li);
  });
  return list;
}

function renderTopic(topic, unit) {
  const details = document.createElement('details');
  details.className = 'topic';
  details.dataset.unit = unit.id;
  details.dataset.search = toSearchText(topic, unit);

  const summary = document.createElement('summary');
  const left = buildSummary(topic);
  summary.appendChild(left.title);
  summary.appendChild(left.badge);
  details.appendChild(summary);

  const body = document.createElement('div');
  body.className = 'topic-body';

  if (topic.summary) {
    const p = document.createElement('p');
    p.textContent = topic.summary;
    body.appendChild(p);
  }

  const grid = document.createElement('div');
  grid.className = 'subgrid';

  const leftCol = document.createElement('div');
  if (topic.steps && topic.steps.length) {
    const h3 = document.createElement('h3');
    h3.textContent = 'Steps';
    leftCol.appendChild(h3);
    leftCol.appendChild(createList(topic.steps, 'step-list'));
  }

  if (topic.facts && topic.facts.length) {
    const facts = document.createElement('div');
    facts.className = 'fact-row';
    topic.facts.forEach((fact) => {
      const span = document.createElement('span');
      span.className = 'fact';
      span.textContent = fact;
      facts.appendChild(span);
    });
    leftCol.appendChild(facts);
  }

  if (topic.example) {
    const h3 = document.createElement('h3');
    h3.textContent = 'Example';
    leftCol.appendChild(h3);
    const pre = document.createElement('div');
    pre.className = 'example';
    pre.textContent = topic.example;
    leftCol.appendChild(pre);
  }

  const rightCol = document.createElement('div');
  if (topic.code) {
    const h3 = document.createElement('h3');
    h3.textContent = 'Pseudocode';
    rightCol.appendChild(h3);

    const wrap = document.createElement('div');
    wrap.className = 'code-wrap';

    const bar = document.createElement('div');
    bar.className = 'code-bar';

    const label = document.createElement('span');
    label.textContent = 'Clear pseudocode';
    bar.appendChild(label);

    const copy = document.createElement('button');
    copy.className = 'copy-btn';
    copy.type = 'button';
    copy.textContent = 'Copy';
    copy.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(topic.code);
        copy.textContent = 'Copied';
        window.setTimeout(() => {
          copy.textContent = 'Copy';
        }, 1000);
      } catch {
        copy.textContent = 'Copy failed';
        window.setTimeout(() => {
          copy.textContent = 'Copy';
        }, 1000);
      }
    });
    bar.appendChild(copy);

    const pre = document.createElement('pre');
    const code = document.createElement('code');
    code.textContent = topic.code;
    pre.appendChild(code);

    wrap.appendChild(bar);
    wrap.appendChild(pre);
    rightCol.appendChild(wrap);
  }

  grid.appendChild(leftCol);
  if (rightCol.childNodes.length) {
    grid.appendChild(rightCol);
  }

  body.appendChild(grid);
  details.appendChild(body);
  return details;
}

function renderUnit(unit) {
  const section = document.createElement('section');
  section.className = 'unit';
  section.id = unit.id;

  const header = document.createElement('div');
  header.className = 'unit-header';
  const h2 = document.createElement('h2');
  h2.textContent = `${unit.title} - ${unit.subtitle}`;
  const p = document.createElement('p');
  p.textContent = `${unit.topics.length} revision cards`;
  header.appendChild(h2);
  header.appendChild(p);

  const cards = document.createElement('div');
  cards.className = 'cards';
  unit.topics.forEach((topic) => {
    cards.appendChild(renderTopic(topic, unit));
  });

  section.appendChild(header);
  section.appendChild(cards);
  return section;
}

function renderTOC() {
  toc.innerHTML = '';
  units.forEach((unit) => {
    const a = document.createElement('a');
    a.href = `#${unit.id}`;
    a.textContent = `${unit.title} - ${unit.topics.length} cards`;
    toc.appendChild(a);
  });
}

function renderFilters() {
  const buttons = [
    { label: 'All', value: 'all' },
    ...units.map((unit) => ({ label: unit.title, value: unit.id }))
  ];

  unitFilters.innerHTML = '';
  buttons.forEach((buttonData) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = `chip${state.unit === buttonData.value ? ' active' : ''}`;
    btn.textContent = buttonData.label;
    btn.addEventListener('click', () => {
      state.unit = buttonData.value;
      renderFilters();
      applyFilters();
    });
    unitFilters.appendChild(btn);
  });
}

function renderContent() {
  content.innerHTML = '';
  units.forEach((unit) => {
    content.appendChild(renderUnit(unit));
  });
}

function renderQuickRef() {
  quickRefMount.innerHTML = '';

  const notice = document.createElement('div');
  notice.className = 'notice';
  const h2 = document.createElement('h2');
  h2.textContent = 'Quick Reference';
  const p = document.createElement('p');
  p.textContent = 'Use this section for the last-minute facts that usually decide exam answers.';
  notice.appendChild(h2);
  notice.appendChild(p);

  const grid = document.createElement('div');
  grid.className = 'quick-grid';

  quickRef.forEach((table) => {
    const card = document.createElement('div');
    card.className = 'quick-card';

    const title = document.createElement('h2');
    title.textContent = table.title;
    card.appendChild(title);

    const tableEl = document.createElement('table');
    const thead = document.createElement('thead');
    const hr = document.createElement('tr');
    const headers = table.columns || table.rows[0].map((_, index) => `Col ${index + 1}`);
    headers.forEach((headerText) => {
      const th = document.createElement('th');
      th.textContent = headerText;
      hr.appendChild(th);
    });
    thead.appendChild(hr);
    tableEl.appendChild(thead);

    const tbody = document.createElement('tbody');
    table.rows.forEach((row) => {
      const tr = document.createElement('tr');
      row.forEach((cell) => {
        const td = document.createElement('td');
        td.textContent = cell;
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    tableEl.appendChild(tbody);
    card.appendChild(tableEl);
    grid.appendChild(card);
  });

  quickRefMount.appendChild(notice);
  quickRefMount.appendChild(grid);
}

function applyFilters() {
  const query = normalise(state.query);
  const cards = document.querySelectorAll('.topic');
  let visible = 0;

  cards.forEach((card) => {
    const matchesUnit = state.unit === 'all' || card.dataset.unit === state.unit;
    const matchesQuery = !query || card.dataset.search.includes(query);
    const visibleNow = matchesUnit && matchesQuery;
    card.style.display = visibleNow ? '' : 'none';
    if (visibleNow) visible += 1;
  });

  document.querySelectorAll('.unit').forEach((unitSection) => {
    const unitCards = unitSection.querySelectorAll('.topic');
    const anyVisible = Array.from(unitCards).some((card) => card.style.display !== 'none');
    unitSection.style.display = anyVisible ? '' : 'none';
  });

  const empty = document.getElementById('emptyState') || createEmptyState();
  empty.style.display = visible === 0 ? 'block' : 'none';
  stats.innerHTML = '';
  stats.appendChild(makeStat('Units', String(units.length)));
  stats.appendChild(makeStat('Cards', String(units.reduce((sum, unit) => sum + unit.topics.length, 0))));
  stats.appendChild(makeStat('Visible', String(visible)));
}

function makeStat(label, value) {
  const span = document.createElement('span');
  span.className = 'stat';
  span.innerHTML = `<strong>${escapeHTML(value)}</strong> ${escapeHTML(label)}`;
  return span;
}

function createEmptyState() {
  const empty = document.createElement('div');
  empty.className = 'empty';
  empty.id = 'emptyState';
  empty.textContent = 'No matching topics. Try a shorter search or switch back to All units.';
  content.parentElement.insertBefore(empty, content.nextSibling);
  return empty;
}

function setAllDetails(open) {
  document.querySelectorAll('.topic').forEach((topic) => {
    topic.open = open;
  });
}

search.addEventListener('input', () => {
  state.query = search.value;
  applyFilters();
});

expandAllBtn.addEventListener('click', () => setAllDetails(true));
collapseAllBtn.addEventListener('click', () => setAllDetails(false));
clearFilterBtn.addEventListener('click', () => {
  state.unit = 'all';
  state.query = '';
  search.value = '';
  renderFilters();
  applyFilters();
});

renderTOC();
renderFilters();
renderContent();
renderQuickRef();
applyFilters();
